#!/usr/bin/env python3
"""
visual_scan.py -- JPEG-surviving and 2D readings of Arweave Puzzle #11.

The consecutive raster LSB scan in lsb_scan.py does not cover:
  * raw 8-bit gray values as the 32-byte key (not packed bits)
  * 2D tiles (16x16 / 32x8 / 8x32 of LSB or ink/white)
  * downsampled thumbnails packed as 256 bits
  * equal-width column/row strips as 32 bytes

--selftest plants a known key in an 8x4 raw block and a 16x16 LSB tile
and recovers both. On MATCH the 64-hex key is written to match.hex and
is not printed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
from Crypto.Hash import keccak
from ecdsa import SECP256k1, SigningKey
from PIL import Image

try:
    from coincurve import PrivateKey as CPrivateKey
except ImportError:
    CPrivateKey = None

ROOT = Path(__file__).resolve().parent.parent
IMAGE = ROOT / "clues" / "arweave-puzzle-11.png"
GEO = ROOT / "data" / "geometry.json"
TARGET = bytes.fromhex("ff2142e98e09b5344994f9beb9c56c95506b9f17")
SECP_N = int(SECP256k1.order)
W_MSB = np.array([128, 64, 32, 16, 8, 4, 2, 1], dtype=np.uint16)


def eth_tail(priv: bytes) -> bytes | None:
    if len(priv) != 32:
        return None
    n = int.from_bytes(priv, "big")
    if n == 0 or n >= SECP_N:
        return None
    if CPrivateKey is not None:
        try:
            pub = CPrivateKey(priv).public_key.format(compressed=False)[1:]
        except Exception:
            return None
    else:
        try:
            pub = SigningKey.from_string(priv, curve=SECP256k1).get_verifying_key().to_string()
        except Exception:
            return None
    h = keccak.new(digest_bits=256)
    h.update(pub)
    return h.digest()[-20:]


def pack_msb(bits: np.ndarray) -> bytes:
    n = (len(bits) // 8) * 8
    if n == 0:
        return b""
    bits = bits[:n].astype(np.uint8)
    packed = (bits.reshape(-1, 8).astype(np.uint16) * W_MSB).sum(axis=1)
    return packed.astype(np.uint8).tobytes()


def write_match(priv: bytes, source: str) -> None:
    Path("match.hex").write_text(priv.hex() + "\n")
    print(f"MATCH source={source}")


def consider(priv: bytes, source: str, seen: set[bytes]) -> bool:
    if len(priv) != 32 or priv in seen:
        return False
    seen.add(priv)
    if eth_tail(priv) == TARGET:
        write_match(priv, source)
        return True
    return False


def load_gray() -> np.ndarray:
    return np.array(Image.open(IMAGE))[:, :, 0]


def measure_rate(n: int = 400) -> float:
    keys = []
    while len(keys) < n:
        k = os.urandom(32)
        if 0 < int.from_bytes(k, "big") < SECP_N:
            keys.append(k)
    t0 = time.time()
    for k in keys:
        eth_tail(k)
    return n / (time.time() - t0)


def selftest() -> None:
    rng = np.random.default_rng(3)
    secret = os.urandom(32)
    cover = rng.integers(0, 256, size=(64, 64), dtype=np.uint8)
    cover[10:18, 20:24] = np.frombuffer(secret, dtype=np.uint8).reshape(8, 4)
    got = cover[10:18, 20:24].reshape(-1).tobytes()
    assert got == secret
    bits = np.unpackbits(np.frombuffer(secret, dtype=np.uint8))
    tile = rng.integers(0, 256, size=(16, 16), dtype=np.uint8)
    tile = (tile & 0xFE) | bits.reshape(16, 16)
    rec = pack_msb((tile & 1).reshape(-1))
    assert rec == secret
    print("SELFTEST OK")


def slide_stream(data: bytes, source: str, seen: set[bytes]) -> bool:
    for i in range(0, max(0, len(data) - 31)):
        if consider(data[i : i + 32], f"{source}@{i}", seen):
            return True
    return False


def hashes_of(data: bytes, source: str, seen: set[bytes]) -> bool:
    for blob, tag in ((data, "all"), (data[:32], "head"), (data[-32:], "tail")):
        if not blob:
            continue
        if consider(hashlib.sha256(blob).digest(), f"{source} {tag} sha256", seen):
            return True
        k = keccak.new(digest_bits=256)
        k.update(blob)
        if consider(k.digest(), f"{source} {tag} keccak", seen):
            return True
    return False


def run_thumb() -> int:
    gray = load_gray()
    geo = json.loads(GEO.read_text())
    seen: set[bytes] = set()
    im = Image.fromarray(gray)
    crops = {"full": im}
    b0, b11 = geo["buildings"][0], geo["buildings"][-1]
    crops["buildings"] = Image.fromarray(gray[b0["roof_y"] : b11["bottom_y"], b0["x0"] : b11["x1"]])
    sail = geo["large_sailboat"]
    crops["sail"] = Image.fromarray(gray[sail["y0"] : sail["y1"], sail["x0"] : sail["x1"]])
    sizes = [(16, 16), (32, 8), (8, 32), (64, 4), (4, 64), (32, 1), (1, 32), (8, 4), (4, 8)]
    filters = [
        Image.Resampling.NEAREST,
        Image.Resampling.BOX,
        Image.Resampling.BILINEAR,
        Image.Resampling.BICUBIC,
        Image.Resampling.LANCZOS,
    ]
    for crop_name, crop in crops.items():
        for size in sizes:
            for filt in filters:
                small = np.array(crop.resize(size, filt), dtype=np.uint8)
                src = f"thumb/{crop_name}/{size[0]}x{size[1]}/{filt.name}"
                if small.size == 32:
                    if consider(small.tobytes(), src + " raw", seen):
                        return 0
                    if consider((255 - small).tobytes(), src + " inv", seen):
                        return 0
                bits_src = small.reshape(-1)
                for t in list(range(0, 256, 16)) + [110, 128, 180, 200, 240]:
                    bits = (bits_src < t).astype(np.uint8)
                    if bits.size < 256:
                        packed = pack_msb(np.pad(bits, (0, 256 - bits.size)))
                    else:
                        packed = pack_msb(bits[:256])
                    if consider(packed, f"{src} t{t}", seen):
                        return 0
                    if consider(pack_msb(1 - bits[:256]) if bits.size >= 256 else pack_msb(np.pad(1 - bits, (0, 256 - bits.size))), f"{src} t{t}inv", seen):
                        return 0
    # 32 equal strips of means
    h, w = gray.shape
    for name, arr, axis in (("cols", gray, 1), ("rows", gray, 0), ("bldg_cols", np.array(crops["buildings"]), 1)):
        n = arr.shape[axis]
        width = n // 32
        if width < 1:
            continue
        for off in range(n - 32 * width + 1):
            means = []
            for i in range(32):
                sl = slice(off + i * width, off + (i + 1) * width)
                chunk = arr[:, sl] if axis == 1 else arr[sl, :]
                means.append(int(round(float(chunk.mean()))))
            if consider(bytes(means), f"strips/{name}/w{width}/off{off}", seen):
                return 0
            if off > 8 and width > 4:
                break
    print(f"NO MATCH thumb unique={len(seen)}")
    return 1


def run_raw() -> int:
    gray = load_gray()
    D = measure_rate()
    streams = {
        "xy": gray.reshape(-1),
        "yx": gray.T.reshape(-1),
        "xy_rev": gray.reshape(-1)[::-1],
        "nonwhite": gray.reshape(-1)[gray.reshape(-1) != 255],
        "ink110": gray.reshape(-1)[gray.reshape(-1) < 110],
        "ink200": gray.reshape(-1)[gray.reshape(-1) < 200],
    }
    N = sum(max(0, s.size - 31) for s in streams.values())
    print(f"raw N={N} D={D:.0f}/s t={N / D:.1f}s")
    if N / D > 7200:
        print("ABORT: t > 2 hours")
        return 2
    seen: set[bytes] = set()
    t0 = time.time()
    tested = 0
    for name, seq in streams.items():
        data = seq.astype(np.uint8).tobytes()
        nwin = max(0, len(data) - 31)
        for i in range(nwin):
            if consider(data[i : i + 32], f"raw/{name}@{i}", seen):
                return 0
        tested += nwin
        print(f"raw {name} n={nwin} cum={tested} {tested / (time.time() - t0):.0f}/s", flush=True)
    # 2D raw tiles of 32 pixels. Consecutive 1x32 / 32x1 are already in xy / yx.
    shapes = ((2, 16), (4, 8), (8, 4), (16, 2))
    h, w = gray.shape
    for th, tw in shapes:
        nwin = (h - th + 1) * (w - tw + 1)
        print(f"raw tile {th}x{tw} n={nwin}", flush=True)
        for y in range(h - th + 1):
            row = gray[y : y + th]
            for x in range(w - tw + 1):
                priv = row[:, x : x + tw].tobytes()
                tail = eth_tail(priv)
                tested += 1
                if tail == TARGET:
                    write_match(priv, f"rawtile/{th}x{tw}@{y},{x}")
                    return 0
        print(f"  cum={tested} {tested / (time.time() - t0):.0f}/s", flush=True)
    print(f"NO MATCH raw tested={tested} t={time.time() - t0:.1f}s")
    return 1


def run_tiles() -> int:
    gray = load_gray()
    D = measure_rate()
    h, w = gray.shape
    shapes = ((16, 16), (32, 8), (8, 32))
    kinds = ("lsb", "ink110")
    N = 0
    for th, tw in shapes:
        N += (h - th + 1) * (w - tw + 1) * len(kinds)
    print(f"tiles N={N} D={D:.0f}/s t={N / D:.1f}s")
    if N / D > 7200:
        print("ABORT: t > 2 hours")
        return 2
    t0 = time.time()
    tested = 0
    lsb = (gray & 1).astype(np.uint8)
    ink = (gray < 110).astype(np.uint8)
    for kind, bitimg in (("lsb", lsb), ("ink110", ink)):
        for th, tw in shapes:
            print(f"tile {kind} {th}x{tw}", flush=True)
            for y in range(h - th + 1):
                band = bitimg[y : y + th]
                for x in range(w - tw + 1):
                    packed = np.packbits(band[:, x : x + tw].reshape(-1)).tobytes()
                    tested += 1
                    if eth_tail(packed) == TARGET:
                        write_match(packed, f"tile/{kind}/{th}x{tw}@{y},{x}")
                        return 0
            print(f"  cum={tested} {tested / (time.time() - t0):.0f}/s", flush=True)
    print(f"NO MATCH tiles tested={tested} t={time.time() - t0:.1f}s")
    return 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Visual / 2D scan for Arweave Puzzle #11")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--thumb", action="store_true")
    parser.add_argument("--raw", action="store_true")
    parser.add_argument("--tiles", action="store_true")
    args = parser.parse_args()
    if args.selftest and not (args.thumb or args.raw or args.tiles):
        selftest()
        sys.exit(0)
    if not (args.selftest or args.thumb or args.raw or args.tiles):
        parser.print_help()
        sys.exit(2)
    if args.selftest:
        selftest()
    if args.thumb:
        code = run_thumb()
        if code == 0:
            sys.exit(0)
        if not (args.raw or args.tiles):
            sys.exit(code)
    if args.raw:
        code = run_raw()
        if code == 0:
            sys.exit(0)
        if not args.tiles:
            sys.exit(code)
    if args.tiles:
        sys.exit(run_tiles())
    sys.exit(1)


if __name__ == "__main__":
    main()
