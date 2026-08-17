#!/usr/bin/env python3
"""Bounded search for Arweave Puzzle Weave #12 piece 2 (the whale string).

Piece 3 is treated as solved: 2111011 (HEXAGON letter-height code). Piece 4 is
the 5-letter anagram of the printed letters A,E,I,L,N. Piece 1 is the flag
colours. Piece 2 is the whale + date 16-03-2020.

The 58-character budget then forces piece 2's length once piece 1 is fixed:

  colour names including Blue  (28) + 18-char whale
  six RRGGBB hex codes         (36) + 10-char date / a16zcrypto / Andreessen
  six #RRGGBB hex codes        (42) + 4-char a16z
  five visible RRGGBB hex      (30) + 16-char a16z interior (ndreessenHorowit)

Every candidate is passed through the certified oracle (first-block reject,
then the same full decrypt as oracle.py). A MATCH is printed and the process
stops. Run from this folder:

  python3 tools/search_whale.py --selftest
  python3 tools/search_whale.py
"""
from __future__ import annotations

import argparse
import base64
import itertools
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import oracle

TARGET_LEN = 58

# Round-trip hex as printed by HomelessPhD from the JPEG (pre-compression "nice"
# values). Blue is the IQ-test completion of the blank/white flag; White is the
# colour as drawn.
HEX = {
    "Red": "C00000",
    "Indigo": "410080",
    "Gray": "808080",
    "Green": "3F8000",
    "Violet": "7F00FF",
    "Blue": "0000FF",
    "White": "FFFFFF",
    "PurpleDark": "410080",
    "PurpleBright": "7F00FF",
}

# 3 vertical pairs, left-to-right, top-then-bottom inside each pair.
PAIRS_COL = ("Red", "Indigo", "Gray", "Green", "Violet", "Blue")
# Top row left-to-right, then bottom row left-to-right.
PAIRS_ROW = ("Red", "Gray", "Violet", "Indigo", "Green", "Blue")
PAIRS_COL_PURPLE = ("Red", "PurpleDark", "Gray", "Green", "PurpleBright", "Blue")
PAIRS_ROW_PURPLE = ("Red", "Gray", "PurpleBright", "PurpleDark", "Green", "Blue")

# Display names for colour-word concatenations. Hex still uses HEX keys.
DISPLAY = {
    "Red": "Red",
    "Indigo": "Indigo",
    "Gray": "Gray",
    "Grey": "Grey",
    "Green": "Green",
    "Violet": "Violet",
    "Blue": "Blue",
    "White": "White",
    "PurpleDark": "Purple",
    "PurpleBright": "Purple",
}

PIECE3 = (
    "2111011",
    # all four shape codes including the hexagon reading (29 digits)
    "10111121111121112110212111011",
)
PIECE4 = ("Alien", "ALIEN", "alien", "Aline", "ALINE")

# All 24 concatenations; published 2x2 order is (0,1,2,3).
ORDERS = tuple(itertools.permutations(range(4)))

_CT_RAW = base64.b64decode(oracle.CIPHERTEXT_B64)
_SALT, _BODY = _CT_RAW[8:16], _CT_RAW[16:]


def _cases(s):
    out = [s]
    if s != s.lower():
        out.append(s.lower())
    if s != s.upper():
        out.append(s.upper())
    return out


def _hex_join(names, hashed, lower):
    parts = []
    for n in names:
        h = HEX[n]
        if lower:
            h = h.lower()
        parts.append(("#" + h) if hashed else h)
    return "".join(parts)


def piece1_strings():
    """Flag readings: colour names and hex concatenations."""
    seen = set()
    names_orders = [
        PAIRS_COL,
        PAIRS_ROW,
        PAIRS_COL_PURPLE,
        PAIRS_ROW_PURPLE,
        tuple(reversed(PAIRS_COL)),
        tuple(reversed(PAIRS_ROW)),
        ("Red", "Gray", "Green", "Indigo", "Violet", "Blue"),
        ("Indigo", "Red", "Green", "Gray", "Blue", "Violet"),
    ]
    for names in names_orders:
        joined = "".join(DISPLAY[n] for n in names)
        for s in _cases(joined):
            seen.add(s)
        # Grey spelling, same length as Gray.
        if "Gray" in names:
            grey = tuple("Grey" if n == "Gray" else n for n in names)
            for s in _cases("".join(DISPLAY[n] for n in grey)):
                seen.add(s)
        # White as drawn instead of Blue.
        if names[-1] == "Blue":
            white = names[:-1] + ("White",)
            for s in _cases("".join(DISPLAY[n] for n in white)):
                seen.add(s)
        for hashed, lower, sixth in itertools.product((False, True), (False, True), ("Blue", "White")):
            seq = names[:-1] + (sixth,)
            seen.add(_hex_join(seq, hashed, lower))
        # Five visible flags only (drop the IQ-test blank, Blue or White).
        visible = tuple(n for n in names if n not in ("Blue", "White"))
        if len(visible) == 5:
            seen.add(_hex_join(visible, False, False))
            seen.add(_hex_join(visible, False, True))
            seen.add(_hex_join(visible, True, False))
            seen.add(_hex_join(visible, True, True))
    # First letters of the six colours (6 chars), for the all-digits piece-3 partition.
    for names in names_orders:
        initials = "".join(DISPLAY[n][0] for n in names)
        for s in _cases(initials):
            seen.add(s)
        if names[-1] == "Blue":
            initials_w = "".join(DISPLAY[n][0] for n in names[:-1] + ("White",))
            for s in _cases(initials_w):
                seen.add(s)
    return sorted(seen)


def piece2_strings():
    """Whale / date / investor readings, including unused 18-char forms."""
    raw = [
        # 4: a16z (the 16 in the date is the nickname)
        "a16z", "A16z", "A16Z", "a16Z",
        # 8-11: the date as printed, and short names
        "16-03-2020", "16/03/2020", "16.03.2020", "16032020",
        "2020-03-16", "20200316", "16-3-2020", "16.3.2020",
        "March162020", "16March2020", "Horowitz", "Permaweb",
        "BlueWhale", "bluewhale", "BLUEWHALE",
        "Andreessen", "SamWilliams", "a16zcrypto", "a16zCrypto",
        "A16zCrypto", "WeiBlocked", "Alexandria",
        "SpermWhale", "BlueWhales",
        # 12-16
        "Balaenoptera", "MichaelHaley", "MarcAndreessen",
        "a16zAndreessen", "a16z16-03-2020",
        "CoinbaseVentures", "SpermWhaleAndOrca", "SpermWhaleOrcaDay",
        "ndreessenHorowit", "PermanentLibrary", "LibraryAlexandria",
        # 18: the length forced by 28-char colour names
        "AndreessenHorowitz", "HorowitzAndreessen",
        "MarcAndreessena16z", "a16zAndreessen2020",
        "MarchSixteenth2020", "SixteenthMarch2020",
        "BlueWhaleMarch2020", "a16zMarchSixteenth",
        "PermanentLibraryOf",
        # 19-20: only combine with a 27/26-char piece 1 if one appears
        "UnionSquareVentures", "LibraryOfAlexandria",
        "MichaelStephenHaley", "BalaenopteraMusculus",
        "Andreessen-Horowitz", "BlueWhale16-03-2020",
        "8.3million", "8300000", "Orca", "whale", "Whale",
        "Tiamat", "Leviathan", "MobyDick",
    ]
    seen = set()
    for s in raw:
        seen.add(s)
        if s[:1].isalpha() and s != s.lower():
            seen.add(s.lower())
            seen.add(s.upper())
    return sorted(seen)


def assemble(p1s, p2s, p3s, p4s):
    out = []
    seen = set()
    for p1, p2, p3, p4 in itertools.product(p1s, p2s, p3s, p4s):
        parts = (p1, p2, p3, p4)
        if sum(len(p) for p in parts) != TARGET_LEN:
            continue
        for order in ORDERS:
            cand = "".join(parts[i] for i in order)
            if cand not in seen:
                seen.add(cand)
                out.append(cand)
    return out


def check_fast(candidate):
    """Same pipeline as oracle.check, skipping the full CBC when the first block cannot be a JWK."""
    key_hex = oracle._stretch(candidate)
    key, iv = oracle._evp_bytes_to_key(key_hex.encode("ascii"), _SALT, 128, 16, 10000)
    w, nr = oracle._key_expansion(key)
    first = bytes(a ^ b for a, b in zip(oracle._decrypt_block(_BODY[:16], w, nr), iv))
    if b'"kty"' not in first and not first.startswith(b"{"):
        return False, None
    return oracle.check(candidate)


def _worker(cands):
    hits = []
    found_w = []
    n = 0
    for c in cands:
        n += 1
        if c.startswith("WITNESS"):
            found_w.append(c)
        ok, addr = check_fast(c)
        if ok:
            hits.append((c, addr))
    return n, hits, found_w


def _chunks(seq, size):
    for i in range(0, len(seq), size):
        yield seq[i:i + size]


def selftest_fastpath():
    if not oracle.selftest():
        return False
    # Fast path must agree with the full oracle on rejects, and must not
    # invent a match on the solved-sibling answer (wrong ciphertext).
    probes = [
        "RedIndigoGrayGreenVioletBlueAndreessenHorowitz2111011Alien",
        "a" * 58,
        oracle.PZL8_ANSWER,
    ]
    for p in probes:
        fast = check_fast(p)
        full = oracle.check(p)
        if fast != full:
            print("SELFTEST FAILED: fast path disagree on %r: %s vs %s" % (p, fast, full))
            return False
    print("SELFTEST OK: fast path agrees with oracle.check on reject probes")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--workers", type=int, default=os.cpu_count() or 1)
    parser.add_argument("--limit", type=int, default=0, help="cap candidates (0 = all)")
    args = parser.parse_args()
    if args.selftest:
        sys.exit(0 if selftest_fastpath() else 1)

    p1 = piece1_strings()
    p2 = piece2_strings()
    cands = assemble(p1, p2, PIECE3, PIECE4)
    cands.sort()
    n_raw = len(cands)
    if args.limit:
        cands = cands[: args.limit]

    # Head / middle / tail pipeline witnesses: three 58-char strings of the
    # same shape, inserted into the stream, re-found by identity after the run.
    # They are not MATCH witnesses (the true answer is unknown); they only
    # prove the worker processed the start, middle, and end of the list.
    witnesses = [
        "WITNESSHEAD" + "x" * (TARGET_LEN - 11),
        "WITNESSMIDD" + "y" * (TARGET_LEN - 11),
        "WITNESSTAIL" + "z" * (TARGET_LEN - 11),
    ]
    if cands:
        mid = len(cands) // 2
        cands = [witnesses[0]] + cands[:mid] + [witnesses[1]] + cands[mid:] + [witnesses[2]]
    else:
        cands = list(witnesses)

    n = len(cands)
    print("piece1=%d piece2=%d assembled_58=%d with_witnesses=%d" % (len(p1), len(p2), n_raw, n))
    # Rate sample
    sample = cands[:8]
    t0 = time.time()
    for c in sample:
        check_fast(c)
    dt = time.time() - t0
    rate = (len(sample) / dt) if dt else 0.0
    # Sequential sample understates wall rate; the last 4-core run on this host
    # held ~100/s. Use 80/s as a conservative parallel projection.
    projected_wall = n / 80.0
    print("measured 1-thread D=%.2f /s, projected wall t=%.0fs at 80/s (N=%d, workers=%d)" % (
        rate, projected_wall, n, args.workers))
    if projected_wall > 2 * 3600:
        print("abort: projected wall time above two hours; shrink N", file=sys.stderr)
        sys.exit(2)

    workers = max(1, args.workers)
    chunk = max(8, n // (workers * 8) or 8)
    t0 = time.time()
    done = 0
    hits = []
    seen_witness = set()
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(_worker, ch) for ch in _chunks(cands, chunk)]
        for fut in as_completed(futs):
            k, h, found_w = fut.result()
            done += k
            hits.extend(h)
            seen_witness.update(found_w)
            if h:
                break
    elapsed = time.time() - t0
    if not hits and seen_witness != set(witnesses):
        print("WITNESS MISS: saw %s" % sorted(seen_witness), file=sys.stderr)
        sys.exit(1)
    for w in sorted(seen_witness):
        ok, _addr = check_fast(w)
        if ok:
            print("WITNESS FALSE POSITIVE %r" % w)
            sys.exit(1)
    print("witnesses re-found in-stream: %s (all NO MATCH, as planted)" % ", ".join(sorted(seen_witness)))
    print("checked=%d hits=%d elapsed=%.1fs rate=%.2f/s" % (
        done, len(hits), elapsed, done / elapsed if elapsed else 0.0))
    for c, addr in hits:
        print("MATCH %s <- %r" % (addr, c))
        sys.exit(0)
    print("NO MATCH")
    sys.exit(1)


if __name__ == "__main__":
    main()
