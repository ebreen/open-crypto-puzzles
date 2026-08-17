#!/usr/bin/env python3
"""
hatch_hex.py -- hatch-band and column readings as hex digits for Puzzle #11.

The remaining lead is a visual reading that produces 64 hex characters, not a
32-byte pixel window. This tool turns horizontal ink bands (floors of hatching
inside each building, optionally the sail) and per-column silhouette features
into nibble streams, then:

  * checks 64-nibble windows as private keys against the escrow address
  * searches 40-nibble windows for the known escrow address hex (if the
    address is drawn the same way as the key, that mapping is the method)

--selftest plants a 64-bar cover whose bar heights encode a known key and
recovers it, and plants the 40-nibble address hex the same way and re-finds
it. On MATCH the 64-hex key is written to match.hex and is not printed.
"""
from __future__ import annotations

import argparse
import json
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
ADDR_HEX = "ff2142e98e09b5344994f9beb9c56c95506b9f17"
SECP_N = int(SECP256k1.order)


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


def write_match(priv: bytes, source: str) -> None:
    Path("match.hex").write_text(priv.hex() + "\n")
    print(f"MATCH source={source}")


def nibbles_to_key(nibs: list[int]) -> bytes | None:
    if len(nibs) != 64:
        return None
    if any(n < 0 or n > 15 for n in nibs):
        return None
    out = bytes((nibs[i] << 4) | nibs[i + 1] for i in range(0, 64, 2))
    return out


def bands(crop: np.ndarray, thresh: int, min_frac: float, min_h: int) -> list[tuple[int, int, float, float]]:
    """Return (y0, y1, ink_frac, mean_gray) for each horizontal ink band."""
    if crop.size == 0:
        return []
    ink = (crop < thresh).mean(axis=1)
    on = ink > min_frac
    out: list[tuple[int, int, float, float]] = []
    i = 0
    n = len(on)
    while i < n:
        if on[i]:
            j = i
            while j < n and on[j]:
                j += 1
            if j - i >= min_h:
                sl = crop[i:j]
                out.append((i, j, float(ink[i:j].mean()), float(sl.mean())))
            i = j
        else:
            i += 1
    return out


def mappings(vals: list[float]) -> dict[str, list[int]]:
    """Several nibble mappings of a numeric sequence."""
    if not vals:
        return {}
    arr = np.array(vals, dtype=np.float64)
    lo, hi = float(arr.min()), float(arr.max())
    span = hi - lo if hi > lo else 1.0
    scaled = np.clip(np.round((arr - lo) / span * 15), 0, 15).astype(int).tolist()
    clipped = np.clip(np.round(arr), 0, 255).astype(int)
    return {
        "mod16": [int(v) % 16 for v in clipped.tolist()],
        "div16": [(int(v) // 16) % 16 for v in clipped.tolist()],
        "scaled": scaled,
        "inv_scaled": [15 - s for s in scaled],
        "mod16_rev": [int(v) % 16 for v in clipped.tolist()][::-1],
        "scaled_rev": scaled[::-1],
    }


def consider_nibs(nibs: list[int], source: str, seen: set[bytes], stats: dict) -> bool:
    stats["streams"] += 1
    hx = "".join(f"{n:x}" for n in nibs)
    if ADDR_HEX in hx or ADDR_HEX in hx[::-1]:
        stats["address_hits"] += 1
        print(f"ADDRESS HIT source={source} (mapping produces the known escrow hex)")
    key = nibbles_to_key(nibs)
    if key is None:
        # slide 64-nibble windows if longer
        for i in range(0, max(0, len(nibs) - 63)):
            stats["windows"] += 1
            k = nibbles_to_key(nibs[i : i + 64])
            if k is None or k in seen:
                continue
            seen.add(k)
            if eth_tail(k) == TARGET:
                write_match(k, f"{source}@{i}")
                return True
        return False
    stats["windows"] += 1
    if key in seen:
        return False
    seen.add(key)
    if eth_tail(key) == TARGET:
        write_match(key, source)
        return True
    return False


def consider_bytes(priv: bytes, source: str, seen: set[bytes], stats: dict) -> bool:
    stats["windows"] += 1
    if priv in seen:
        return False
    seen.add(priv)
    if eth_tail(priv) == TARGET:
        write_match(priv, source)
        return True
    return False


def load() -> tuple[np.ndarray, dict]:
    gray = np.array(Image.open(IMAGE))[:, :, 0]
    geo = json.loads(GEO.read_text())
    return gray, geo


def building_crops(gray: np.ndarray, geo: dict) -> list[np.ndarray]:
    out = []
    for b in geo["buildings"]:
        out.append(gray[b["roof_y"] : b["bottom_y"], b["x0"] : b["x1"]])
    return out


def selftest() -> None:
    # 64 bars, height = nibble+2, encode priv1 = 00..01
    key = bytes.fromhex("00" * 31 + "01")
    nibs = []
    for b in key:
        nibs.append((b >> 4) & 15)
        nibs.append(b & 15)
    assert len(nibs) == 64
    h, w = 900, 80
    img = np.full((h, w), 255, np.uint8)
    y = 2
    for n in nibs:
        bh = n + 2
        img[y : y + bh, 10:70] = 0
        y += bh + 2
    found = bands(img, thresh=128, min_frac=0.1, min_h=2)
    heights = [j - i for i, j, _, _ in found]
    rec = [hgt - 2 for hgt in heights]
    assert rec == nibs, rec[:8]
    packed = nibbles_to_key(rec)
    assert packed == key
    assert eth_tail(packed) == bytes.fromhex("7e5f4552091a69125d5dfcb7b8c2659029395bdf")
    # address plant: 40 bars
    addr_nibs = [int(c, 16) for c in ADDR_HEX]
    img2 = np.full((900, 80), 255, np.uint8)
    y = 2
    for n in addr_nibs:
        bh = n + 2
        img2[y : y + bh, 10:70] = 0
        y += bh + 2
    found2 = bands(img2, 128, 0.1, 2)
    rec2 = [(j - i) - 2 for i, j, _, _ in found2]
    hx = "".join(f"{n:x}" for n in rec2)
    assert ADDR_HEX in hx, hx
    print("SELFTEST OK")


def run_scan() -> int:
    gray, geo = load()
    crops = building_crops(gray, geo)
    sail = geo["large_sailboat"]
    sail_crop = gray[sail["y0"] : sail["y1"], sail["x0"] : sail["x1"]]
    regions = {
        "buildings": crops,
        "buildings_sail": crops + [sail_crop],
    }
    seen: set[bytes] = set()
    stats = {"streams": 0, "windows": 0, "address_hits": 0}
    t0 = time.time()
    thresholds = list(range(80, 230, 10))
    min_hs = (1, 2, 3, 4)
    min_fracs = (0.08, 0.12, 0.15, 0.2, 0.3)

    for region_name, clist in regions.items():
        for th in thresholds:
            for min_h in min_hs:
                for mf in min_fracs:
                    all_bands: list[tuple[int, int, float, float, np.ndarray]] = []
                    for crop in clist:
                        for y0, y1, frac, mean in bands(crop, th, mf, min_h):
                            all_bands.append((y0, y1, frac, mean, crop))
                    if not all_bands:
                        continue
                    heights = [float(y1 - y0) for y0, y1, _, _, _ in all_bands]
                    fracs = [frac * 255.0 for _, _, frac, _, _ in all_bands]
                    means = [mean for _, _, _, mean, _ in all_bands]
                    widths = []
                    for y0, y1, _, _, crop in all_bands:
                        sl = crop[y0:y1]
                        ink = sl < th
                        cols = np.where(ink.any(axis=0))[0]
                        widths.append(float(cols[-1] - cols[0] + 1) if len(cols) else 0.0)
                    src_base = f"hatch/{region_name}/th{th}/h{min_h}/f{mf}/n{len(all_bands)}"
                    # 32 bands as raw bytes (heights/means clipped)
                    if len(all_bands) == 32:
                        for name, seq in (("height", heights), ("mean", means), ("width", widths), ("frac", fracs)):
                            raw = bytes(int(np.clip(v, 0, 255)) for v in seq)
                            if consider_bytes(raw, src_base + f"/{name}u8", seen, stats):
                                return 0
                            if consider_bytes(bytes(reversed(raw)), src_base + f"/{name}u8rev", seen, stats):
                                return 0
                    for name, seq in (("height", heights), ("mean", means), ("width", widths), ("frac", fracs)):
                        for map_name, nibs in mappings(seq).items():
                            src = f"{src_base}/{name}/{map_name}"
                            if consider_nibs(nibs, src, seen, stats):
                                return 0
                            # if exactly 32 mapped values 0-15, pad to 64 nibbles
                            if len(nibs) == 32:
                                for pad in (nibs + [0] * 32, [0] * 32 + nibs, nibs + nibs):
                                    if consider_nibs(pad, src + "/pad", seen, stats):
                                        return 0

    # per-column nibble streams of the building band
    b0, b11 = geo["buildings"][0], geo["buildings"][-1]
    band = gray[0 : b11["bottom_y"] + 10, b0["x0"] : b11["x1"]]
    h, w = band.shape
    ink110 = (band < 110)
    first = np.zeros(w, dtype=np.int32)
    dark_runs = np.zeros(w, dtype=np.int32)
    inkf = ink110.mean(axis=0)
    means = band.mean(axis=0)
    for x in range(w):
        ys = np.where(ink110[:, x])[0]
        first[x] = int(ys[0]) if len(ys) else h
        col = ink110[:, x]
        padded = np.concatenate([[False], col, [False]])
        dark_runs[x] = int(((~padded[:-1]) & padded[1:]).sum())
    col_feats = {
        "roof": first.astype(np.float64),
        "height": (h - first).astype(np.float64),
        "inkf": inkf * 255.0,
        "mean": means,
        "runs": dark_runs.astype(np.float64),
    }
    for feat_name, feat in col_feats.items():
        # nibble per column via several maps, then slide 64
        clipped = np.clip(np.round(feat), 0, 255).astype(int)
        variants = {
            "mod16": (clipped % 16).tolist(),
            "div16": ((clipped // 16) % 16).tolist(),
        }
        lo, hi = float(feat.min()), float(feat.max())
        span = hi - lo if hi > lo else 1.0
        scaled = np.clip(np.round((feat - lo) / span * 15), 0, 15).astype(int).tolist()
        variants["scaled"] = scaled
        for map_name, nibs in variants.items():
            src = f"cols/{feat_name}/{map_name}"
            if consider_nibs(nibs, src, seen, stats):
                return 0
            # also 64 equal bins of the feature
            for nbins in (32, 40, 64):
                width = w // nbins
                if width < 1:
                    continue
                binned = [float(feat[i * width : (i + 1) * width].mean()) for i in range(nbins)]
                for mn, nn in mappings(binned).items():
                    if consider_nibs(nn, f"cols/{feat_name}/bin{nbins}/{mn}", seen, stats):
                        return 0
                if nbins == 32:
                    raw = bytes(int(np.clip(v, 0, 255)) for v in binned)
                    if consider_bytes(raw, f"cols/{feat_name}/bin32u8", seen, stats):
                        return 0

    # hatch orientation of 12 buildings as bits, not enough alone; combine with
    # 12 heights as nibbles already covered by geometry family. Skip.

    elapsed = time.time() - t0
    print(
        f"NO MATCH unique={len(seen)} windows={stats['windows']} "
        f"streams={stats['streams']} address_hits={stats['address_hits']} "
        f"t={elapsed:.2f}s"
    )
    return 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Hatch/column hex scan for Arweave Puzzle #11")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--scan", action="store_true")
    args = parser.parse_args()
    if args.selftest and not args.scan:
        selftest()
        sys.exit(0)
    if not (args.selftest or args.scan):
        parser.print_help()
        sys.exit(2)
    if args.selftest:
        selftest()
    if args.scan:
        sys.exit(run_scan())
    sys.exit(1)


if __name__ == "__main__":
    main()
