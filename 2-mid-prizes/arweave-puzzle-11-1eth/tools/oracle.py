#!/usr/bin/env python3
"""
oracle.py -- candidate checker for Arweave Puzzle #11 (1 ETH).

The answer is a 64-character hex private key. The escrow address is the
Ethereum address derived from it: secp256k1 uncompressed public key,
Keccak-256 of the 64-byte XY, last 20 bytes. No BIP39, no passphrase,
no derivation path.

Usage (from this folder):
    python3 tools/oracle.py --selftest
    python3 tools/oracle.py "<64 hex chars>"
    python3 tools/oracle.py --stdin

Certified against two public vectors, neither of which is a live secret:
  1. secp256k1 private key 1, a standard test vector.
  2. Arweave Puzzle #13's published, already-spent key from the 2020-06-10
     write-up (same author, same raw-hex-to-ETH-address transform).

This certifies hex-to-address only. It does not certify any image-to-key
mapping for puzzle #11; that mapping has no solved sibling.
"""
from __future__ import annotations

import sys

from Crypto.Hash import keccak
from ecdsa import SECP256k1, SigningKey

TARGET = "0xff2142e98e09b5344994f9beb9c56c95506b9f17"

# Standard vector: private key 1.
PRIV1 = "00" * 31 + "01"
PRIV1_ADDRESS = "0x7e5f4552091a69125d5dfcb7b8c2659029395bdf"

# Puzzle #13, published as solved on 2020-05-23, write-up 2020-06-10.
# Address 0x0a5C81F5bFb8Ec2f47defF466A1a4e55b8FC9319 is spent.
PZL13_KEY = "c79eac48c3334fc967d5aecb37222d9a4307027d0ec2bcd6f914417cf78d3c82"
PZL13_ADDRESS = "0x0a5c81f5bfb8ec2f47deff466a1a4e55b8fc9319"


def eth_address(privkey_hex: str) -> str | None:
    """64-hex private key -> lowercase 0x-prefixed Ethereum address, or None."""
    text = privkey_hex.strip().lower()
    if text.startswith("0x"):
        text = text[2:]
    if len(text) != 64:
        return None
    try:
        key_bytes = bytes.fromhex(text)
    except ValueError:
        return None
    if len(key_bytes) != 32:
        return None
    n = int.from_bytes(key_bytes, "big")
    if n == 0 or n >= SECP256k1.order:
        return None
    try:
        sk = SigningKey.from_string(key_bytes, curve=SECP256k1)
    except Exception:
        return None
    pub = sk.get_verifying_key().to_string()  # 64 bytes, X || Y
    h = keccak.new(digest_bits=256)
    h.update(pub)
    return "0x" + h.digest()[-20:].hex()


def check(candidate: str) -> str | None:
    try:
        return eth_address(candidate)
    except Exception:
        return None


def selftest() -> None:
    addr1 = check(PRIV1)
    assert addr1 == PRIV1_ADDRESS, f"priv1 mismatch: {addr1} != {PRIV1_ADDRESS}"
    addr13 = check(PZL13_KEY)
    assert addr13 == PZL13_ADDRESS, f"pzl13 mismatch: {addr13} != {PZL13_ADDRESS}"
    assert check(PRIV1) != TARGET
    print("SELFTEST OK")


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print('usage: oracle.py --selftest | "<64 hex chars>" | --stdin')
        sys.exit(2)

    if args[0] == "--selftest":
        selftest()
        sys.exit(0)

    if args[0] == "--stdin":
        matched = False
        for line in sys.stdin:
            candidate = line.strip()
            if not candidate:
                continue
            addr = check(candidate)
            if addr == TARGET:
                print("MATCH")
                matched = True
        sys.exit(0 if matched else 1)

    addr = check(args[0])
    if addr == TARGET:
        print("MATCH")
        sys.exit(0)
    print("NO MATCH")
    sys.exit(1)


if __name__ == "__main__":
    main()
