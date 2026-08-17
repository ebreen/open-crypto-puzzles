#!/usr/bin/env python3
"""
lsb_scan.py -- bit-plane and LSB extraction for Arweave Puzzle #11.

Purpose:
    Turn the published PNG's grayscale and alpha channels into 32-byte
    candidates and feed them through tools/oracle.py's transform (secp256k1
    uncompressed public key, Keccak-256, last 20 bytes). A match is the
    escrow address 0xFF2142E98E09b5344994F9bEB9C56C95506B9F17.

    This certifies the extraction harness against synthetic witnesses (a
    known 32-byte key planted in LSB of a cover image, re-found at head,
    middle and tail). It does not certify that the author used LSB; that
    is exactly the hypothesis the scan tests.

Usage (from this folder):
    python3 tools/lsb_scan.py --selftest
    python3 tools/lsb_scan.py --prefix
    python3 tools/lsb_scan.py --slide

--prefix tests first/last 32 bytes, skip-run prefixes, 4-byte length
headers, SHA-256 / double SHA-256 / Keccak-256 of the first 1 KB, and any
64-hex ASCII, for each stream. --slide tests every overlapping 32-byte
window of the packed streams listed in data/lsb_scan.json.

On MATCH the 64-hex key is written to match.hex in the current directory
and is not printed. Exit 0 on MATCH, 1 on NO MATCH, 2 on usage error.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
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
TARGET = bytes.fromhex("ff2142e98e09b5344994f9beb9c56c95506b9f17")
SECP_N = int(SECP256k1.order)
HEX64_RE = re.compile(rb"(?:0x)?([0-9a-fA-F]{64})")
W_MSB = np.array([128, 64, 32, 16, 8, 4, 2, 1], dtype=np.uint16)
W_LSB = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint16)

BIT_ALIGN_NAMES = {
    "gray_xy_p0",
    "gray_nonwhite_p0",
    "gray_whiteish_p0",
    "gray_ink_p0",
    "sail_p0",
}


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


def bits_to_bytes(bits: np.ndarray, msb_first: bool = True) -> bytes:
    n = (len(bits) // 8) * 8
    if n == 0:
        return b""
    bits = bits[:n].astype(np.uint8)
    weights = W_MSB if msb_first else W_LSB
    packed = (bits.reshape(-1, 8).astype(np.uint16) * weights).sum(axis=1)
    return packed.astype(np.uint8).tobytes()


def extract_low_bits(seq: np.ndarray, nbits: int) -> np.ndarray:
    stacked = np.stack([(seq >> b) & 1 for b in range(nbits - 1, -1, -1)], axis=1)
    return stacked.reshape(-1).astype(np.uint8)


def write_match(priv: bytes, source: str) -> None:
    Path("match.hex").write_text(priv.hex() + "\n")
    print(f"MATCH source={source}")


def consider(priv: bytes, source: str, seen: set[bytes]) -> bool:
    if priv in seen:
        return False
    seen.add(priv)
    if eth_tail(priv) == TARGET:
        write_match(priv, source)
        return True
    return False


def skip_run_candidates(data: bytes) -> list[bytes]:
    out = []
    if len(data) >= 32:
        out.append(data[:32])
        out.append(data[-32:])
    for fill in (0x00, 0xFF):
        i = 0
        while i < len(data) and data[i] == fill:
            i += 1
        if i + 32 <= len(data):
            out.append(data[i : i + 32])
        if i + 36 <= len(data):
            out.append(data[i + 4 : i + 36])
    if len(data) >= 36:
        for endian in ("big", "little"):
            ln = int.from_bytes(data[:4], endian)
            if ln in (32, 33, 42, 64, 66) and 4 + 32 <= len(data):
                out.append(data[4:36])
    return out


def hashes_of(data: bytes) -> list[bytes]:
    out = []
    for blob in (data[:32], data[:64], data[:256], data[:1024]):
        if not blob:
            continue
        out.append(hashlib.sha256(blob).digest())
        out.append(hashlib.sha256(hashlib.sha256(blob).digest()).digest())
        k = keccak.new(digest_bits=256)
        k.update(blob)
        out.append(k.digest())
    return out


def load_channels() -> tuple[np.ndarray, np.ndarray]:
    la = np.array(Image.open(IMAGE))
    return la[:, :, 0], la[:, :, 1]


def scan_orders(arr2d: np.ndarray) -> dict[str, np.ndarray]:
    tmp = np.empty_like(arr2d)
    tmp[0::2] = arr2d[0::2]
    tmp[1::2] = arr2d[1::2, ::-1]
    flat = arr2d.reshape(-1)
    return {
        "xy": flat,
        "xy_rev": flat[::-1],
        "xy_rtl": arr2d[:, ::-1].reshape(-1),
        "xy_btt": arr2d[::-1, :].reshape(-1),
        "yx": arr2d.T.reshape(-1),
        "yx_rev": arr2d.T.reshape(-1)[::-1],
        "boustrophedon": tmp.reshape(-1),
        "xy_even": flat[0::2],
        "xy_odd": flat[1::2],
    }


def named_sequences(gray: np.ndarray, alpha: np.ndarray) -> dict[str, np.ndarray]:
    seqs: dict[str, np.ndarray] = {}
    for ch_name, ch in (("gray", gray), ("alpha", alpha)):
        for order_name, seq in scan_orders(ch).items():
            seqs[f"{ch_name}_{order_name}"] = seq
    flat = gray.reshape(-1)
    seqs["gray_nonwhite"] = flat[flat != 255]
    seqs["gray_nonbw"] = flat[(flat != 255) & (flat != 0)]
    seqs["gray_whiteish"] = flat[flat >= 254]
    seqs["gray_nearwhite"] = flat[flat >= 250]
    seqs["gray_ink"] = flat[flat < 110]
    seqs["alpha_lt255"] = alpha.reshape(-1)[alpha.reshape(-1) < 255]
    seqs["la_interleaved"] = np.stack([gray, alpha], axis=-1).reshape(-1)
    seqs["sail"] = gray[320:599, 44:359].reshape(-1)
    seqs["buildings"] = gray[20:328, 234:1592].reshape(-1)
    return seqs


def bit_streams(seq: np.ndarray) -> list[tuple[str, np.ndarray]]:
    out = []
    for plane in range(8):
        out.append((f"p{plane}", ((seq >> plane) & 1).astype(np.uint8)))
    for nbits in (1, 2, 3, 4):
        out.append((f"low{nbits}", extract_low_bits(seq, nbits)))
    return out


def slide_streams(gray: np.ndarray, alpha: np.ndarray) -> list[tuple[str, np.ndarray]]:
    flat = gray.reshape(-1)
    tmp = np.empty_like(gray)
    tmp[0::2] = gray[0::2]
    tmp[1::2] = gray[1::2, ::-1]
    named = {
        "gray_xy_p0": (flat, 0),
        "gray_xy_rev_p0": (flat[::-1], 0),
        "gray_yx_p0": (gray.T.reshape(-1), 0),
        "gray_boust_p0": (tmp.reshape(-1), 0),
        "gray_even_p0": (flat[0::2], 0),
        "gray_odd_p0": (flat[1::2], 0),
        "gray_nonwhite_p0": (flat[flat != 255], 0),
        "gray_nonbw_p0": (flat[(flat != 255) & (flat != 0)], 0),
        "gray_whiteish_p0": (flat[flat >= 254], 0),
        "gray_nearwhite_p0": (flat[flat >= 250], 0),
        "gray_ink_p0": (flat[flat < 110], 0),
        "alpha_xy_p0": (alpha.reshape(-1), 0),
        "sail_p0": (gray[320:599, 44:359].reshape(-1), 0),
        "buildings_p0": (gray[20:328, 234:1592].reshape(-1), 0),
        "gray_xy_p1": (flat, 1),
    }
    out = []
    for name, (seq, plane) in named.items():
        out.append((name, ((seq >> plane) & 1).astype(np.uint8)))
    return out


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
    secret = bytes.fromhex("22" * 32)
    bits = np.unpackbits(np.frombuffer(secret, dtype=np.uint8))
    assert bits_to_bytes(bits, True) == secret
    rng = np.random.default_rng(2)
    cover = rng.integers(0, 256, size=4096, dtype=np.uint8)
    head, mid, tail = os.urandom(32), os.urandom(32), os.urandom(32)
    planted = [(0, head), (2000, mid), (4064, tail)]
    buf = bytearray(cover.tobytes())
    for off, key in planted:
        buf[off : off + 32] = key
    found = set()
    for i in range(0, len(buf) - 31):
        w = bytes(buf[i : i + 32])
        if w == head:
            found.add("head")
        if w == mid:
            found.add("mid")
        if w == tail:
            found.add("tail")
    assert found == {"head", "mid", "tail"}, found
    # LSB embed of `head` into a 32x32 cover, recover as prefix.
    img = rng.integers(0, 256, size=32 * 32, dtype=np.uint8)
    hb = np.unpackbits(np.frombuffer(head, dtype=np.uint8))
    img[:256] = (img[:256] & 0xFE) | hb
    rec = bits_to_bytes((img & 1)[:256], True)
    assert rec == head
    print("SELFTEST OK")


def run_prefix() -> int:
    gray, alpha = load_channels()
    seqs = named_sequences(gray, alpha)
    seen: set[bytes] = set()
    streams = 0
    t0 = time.time()
    for seq_name, seq in seqs.items():
        if seq.size == 0:
            continue
        for bit_name, bits in bit_streams(seq):
            streams += 1
            for pack_name, msb in (("msb", True), ("lsb", False)):
                data = bits_to_bytes(bits, msb)
                src = f"{seq_name}/{bit_name}/{pack_name}"
                for cand in skip_run_candidates(data):
                    if consider(cand, src + " prefix", seen):
                        return 0
                for cand in hashes_of(data[:1024]):
                    if consider(cand, src + " hash", seen):
                        return 0
                for m in HEX64_RE.finditer(data[:8192] + data[-8192:]):
                    hx = m.group(1)
                    if consider(bytes.fromhex(hx.decode()), src + " hex64", seen):
                        return 0
    print(
        f"NO MATCH streams={streams} unique={len(seen)} "
        f"t={time.time() - t0:.2f}s"
    )
    return 1


def packed_variants(bits: np.ndarray, name: str) -> list[tuple[str, bytes]]:
    out = []
    for pack_name, msb in (("msb", True), ("lsb", False)):
        out.append((f"{name}/{pack_name}/sh0", bits_to_bytes(bits, msb)))
        if name in BIT_ALIGN_NAMES:
            for sh in range(1, 8):
                out.append((f"{name}/{pack_name}/sh{sh}", bits_to_bytes(bits[sh:], msb)))
    return out


def extra_low_n_variants(gray: np.ndarray) -> list[tuple[str, bytes]]:
    flat = gray.reshape(-1)
    seqs = {
        "xy": flat,
        "nonwhite": flat[flat != 255],
        "ink": flat[flat < 110],
    }
    out = []
    for seq_name, seq in seqs.items():
        for nbits in (2, 3, 4):
            bits = extract_low_bits(seq, nbits)
            for pack_name, msb in (("msb", True), ("lsb", False)):
                out.append((f"{seq_name}/low{nbits}/{pack_name}", bits_to_bytes(bits, msb)))
    return out


def run_slide() -> int:
    gray, alpha = load_channels()
    variants: list[tuple[str, bytes]] = []
    for name, bits in slide_streams(gray, alpha):
        variants.extend(packed_variants(bits, name))
    variants.extend(extra_low_n_variants(gray))
    D = measure_rate()
    N = sum(max(0, len(p) - 31) for _, p in variants)
    t_sec = N / D if D else float("inf")
    print(f"N={N} D={D:.0f}/s t={t_sec:.1f}s variants={len(variants)}")
    if t_sec > 7200:
        print("ABORT: t > 2 hours; install coincurve or shrink the stream list")
        return 2
    t0 = time.time()
    tested = 0
    for i, (label, packed) in enumerate(variants, 1):
        nwin = max(0, len(packed) - 31)
        for off in range(nwin):
            tail = eth_tail(packed[off : off + 32])
            if tail == TARGET:
                write_match(packed[off : off + 32], f"{label} off={off}")
                return 0
        tested += nwin
        elapsed = time.time() - t0
        rate = tested / elapsed if elapsed else 0
        print(f"[{i}/{len(variants)}] {label} n={nwin} cum={tested} {rate:.0f}/s", flush=True)
    print(f"NO MATCH tested={tested} t={time.time() - t0:.1f}s")
    return 1


def main() -> None:
    parser = argparse.ArgumentParser(description="LSB scan for Arweave Puzzle #11")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--prefix", action="store_true")
    parser.add_argument("--slide", action="store_true")
    args = parser.parse_args()
    if args.selftest and not args.prefix and not args.slide:
        selftest()
        sys.exit(0)
    if not (args.selftest or args.prefix or args.slide):
        parser.print_help()
        sys.exit(2)
    if args.selftest:
        selftest()
    if args.prefix:
        code = run_prefix()
        if code == 0:
            sys.exit(0)
        if not args.slide:
            sys.exit(code)
    if args.slide:
        sys.exit(run_slide())
    sys.exit(1)


if __name__ == "__main__":
    main()
