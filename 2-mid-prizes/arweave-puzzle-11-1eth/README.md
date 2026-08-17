# Arweave Puzzle #11 (1 ETH, [OPEN])

Tiamat (@arweavep), an Arweave project Discord member and early investor, announced this
puzzle on Twitter on 2020-04-22: a single grayscale PNG sketch of a harbor, uploaded to
Arweave, with 1 ETH locked at an address the author said is "also included somewhere in the
image." Unlike the rest of the series, this puzzle has no password-protected decryption page:
the author's own hint is "MEW: Access by Private Key," meaning the answer is a raw 64-hex
private key read directly out of the image, not a mnemonic or a keystore file. The address
printed in clear text inside the file's metadata is a confirmed decoy. I measured the image's
geometry precisely (12 buildings, 1 large sailboat, 5 small sails) and its metadata (a
create-before-modify timestamp anomaly shared only with a sibling puzzle), and tested close to
1,000 direct encodings of both against the target address, all negative. A witnessed LSB scan
of the grayscale and alpha channels (16,766,064 sliding 32-byte windows plus 3,768 prefix
candidates) is also negative. The hex-to-address transform is now a certified oracle; the
exact pixel-level encoding that turns the drawing into 256 bits is still unknown.

## At a glance

| | |
|---|---|
| Author | Tiamat, [@arweavep on Twitter](https://twitter.com/arweavep) |
| Published | 2020-04-22, Twitter ([original announcement, now deleted](https://twitter.com/arweavep/status/1252961944807641090)) |
| Prize | 1 ETH (about $1,880 at ETH = $1,880, 2026-08-16) |
| Chain | ethereum |
| Escrow | `0xFF2142E98E09b5344994F9bEB9C56C95506B9F17` ([explorer](https://etherscan.io/address/0xFF2142E98E09b5344994F9bEB9C56C95506B9F17)) |
| Last on-chain check | 2026-08-17: funded and unspent (balance exactly 1.000000000000000000 ETH, outgoing transaction count 0) |
| Status | OPEN |
| Puzzle type | image-stego, pixel-code, raw-private-key |
| Target format | raw 32-byte / 64-hex secp256k1 private key, standard ETH address derivation, no mnemonic, no keystore |
| Certified oracle | yes for hex-to-address: `tools/oracle.py --selftest` (private key 1, and Arweave Puzzle #13's published already-spent key). No for image-to-key: no solved sibling image exists. |
| What remains | a visual reading of the drawing that is not consecutive LSB (hatch, skyline, value-band as text) |
| Series | Arweave Puzzles (this folder covers puzzle #11 only) |

## The puzzle as published

The puzzle is a single PNG, `clues/arweave-puzzle-11.png` (1600x1105, 8-bit grayscale with
alpha, published as-is): a pencil-style sketch of a harbor, with a skyline of 12 buildings, one
large sailboat, a jetty carrying 5 small sails, and a watermark reading
`twitter.com/ArweaveP`. The image is stored on Arweave at transaction
`CzITHnEIlkQw9SbaX5futCzFrKk1qe_NwvWnIBmP2fY`
([viewblock](https://viewblock.io/arweave/tx/CzITHnEIlkQw9SbaX5futCzFrKk1qe_NwvWnIBmP2fY)),
uploaded 2020-04-22, and its sha256 (`c6ba4b50fd75181a325f28b620438f740120925a07a23b889dda597546db87e1`)
matches the copy in this folder exactly. The full set of the author's own quotes, each sourced
and dated where a date is recoverable, is in `clues/author-posts.md`.

![Automated silhouette measurements over the published sketch: 12 building bounding boxes and the large sailboat bounding box](images/01-annotated-geometry.png)
*Figure 1. The measured geometry fed into the negative candidate sweep, drawn over the published image (source: data/geometry.json, script tools/fig_geometry.py), 2026-08-16.*

## What is understood

### Mechanism

The expected output is a raw 256-bit ECDSA private key on the secp256k1 curve, which derives
the escrow address directly under the standard Ethereum address scheme
(Keccak-256 of the uncompressed public key, last 20 bytes). The author's "format does not
matter" reply, given when someone asked about the file type, reads as a statement that the
payload survives re-encoding: it lives in the visual pixel content, not in PNG-specific
container structures. The address printed inside a `tEXt` metadata chunk is a confirmed decoy,
not the key: the author separately said the key is "hidden in the image," and a plaintext
address inside the file would defeat the point of a puzzle.

### Derivation and oracle

A candidate is checked by treating it as a 32-byte private key, deriving its Ethereum address,
and comparing the result to the target case-insensitively:

```
python3 tools/oracle.py --selftest
python3 tools/oracle.py "<64 hex chars>"
```

The comparison is standard Ethereum address derivation (Keccak-256 of the uncompressed
public key, last 20 bytes). What is not certified is the step before it, the mapping from
image content to a 32-byte candidate: no known-answer image and key pair exists for this
puzzle to test that mapping against. Geometry and metadata negatives in this folder remain
uncertified for that mapping. The LSB scan carries a synthetic witness on the packer and
slider, documented in `analysis/tested.md`.

### Certified against

`tools/oracle.py --selftest` reproduces two public vectors: secp256k1 private key 1 derives
to `0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf`, and Arweave Puzzle #13's published
already-spent key (write-up 2020-06-10, prize swept 2020-05-23) derives to
`0x0a5C81F5bFb8Ec2f47defF466A1a4e55b8FC9319`. Neither vector is a live secret. Neither
certifies a specific image-to-key scheme for puzzle #11 itself. Puzzle #9's already-spent
address was used only as a positive control on an earlier alpha-channel hypothesis that
failed to reproduce #9's known answer (see `analysis/tested.md`).

### Established facts

1. The escrow holds exactly 1.000000000000000000 ETH and has an outgoing transaction count of
   0, checked via `eth_getBalance` and `eth_getTransactionCount` against a public Ethereum RPC
   endpoint on 2026-08-17.
2. The puzzle image's `tEXt` metadata chunks read `comment 0xFF2142E98E09b5344994F9bEB9C56C95506B9F17`,
   `date:create 2020-03-30T11:38:07+03:00`, and `date:modify 2020-03-30T11:34:44+03:00`: the
   modify timestamp precedes the create timestamp, an anomaly shared only with sibling puzzle
   #9, confirmed by reading the file's own chunks on 2026-08-16.
3. The file is a clean, valid PNG with 0 bytes after the IEND marker: IHDR, gAMA, cHRM, bKGD,
   pHYs, 22 IDAT, 3 tEXt, and IEND chunks, checked with binwalk and direct chunk inspection.
   Community reports of an embedded executable or filesystem are binwalk false positives on
   near-random decompressed pixel bytes, not real container structure.
4. The alpha channel has 434 pixels with a value under 255, clustered on the large sailboat's
   outline with values from 225 to 254 (a deficit of 1 to 30 from 255), consistent with an
   anti-aliasing halo from a copy-paste rather than structured data.
5. Automated silhouette measurement (thresholded at gray value 110) found 12 buildings, 1 large
   sailboat (bounding box x 44 to 359, y 320 to 599), and 5 small sails with widths 27, 53, 79,
   83, and 51 pixels left to right; full coordinates in `data/geometry.json`.
6. No public write-up describes a working encoding scheme for this puzzle: the community repository
   `HomelessPhD/AR_Puzzles` marks its own PZL11 entry as not solved, and a full local archive of
   the community Telegram group (55,002 messages, November 2021 to May 2026) contains no
   message from the author and no later hint beyond the ones quoted in `clues/author-posts.md`.

## What has been tested

Full ledger in [analysis/tested.md](analysis/tested.md). Summary:

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Geometry-derived candidates (building sequences, raw pixel hashes, cHRM bytes, object counts, matrix reshapes, value-band masks) | about 460 candidates | SHA-256, double SHA-256, Keccak-256, address comparison | 0 match, 0 near-miss | uncertified | 2026-06-13 |
| Metadata date anomaly (create/modify timestamps, several encodings and combinations) | dozens of encodings times 6 hash functions | address comparison | 0 match, 0 near-miss | uncertified | 2026-06-13 |
| Sibling-puzzle-#9-calibrated alpha channel carrier hypotheses | several hundred combinations | address comparison, calibrated against #9's real address | 0 match, 0 near-miss, and does not reproduce #9's known answer either | yes, on the #9 positive control only | 2026-06-13 |
| Container-structure myths (embedded executable or filesystem) | full file | binwalk, chunk inspection | refuted: clean valid PNG | yes | 2026-06-13 |
| Consecutive LSB / bit-plane readings of grayscale and alpha | 16,766,064 sliding 32-byte windows plus 3,768 prefix candidates | `tools/lsb_scan.py`, `tools/oracle.py` | 0 match, 0 hex64 string, 0 copy of the escrow address in packed bits | yes: head/middle/tail plants re-found | 2026-08-17 |

Cumulative: on the order of 1,000 geometry and metadata candidates plus 16.8 million LSB
windows, 0 matches, 0 near-misses under the `ff21` address-prefix check.

## Open leads, ranked

1. **A visual hatch or building encoding that is not consecutive LSB** (insight). Consecutive
   LSB of grayscale and alpha is ruled out (16,766,064 windows, 0 match, witnessed). What
   remains is a reading of the drawing: hatch, skyline barcode, or a value-band rendered as
   text. Confirmed if a 64-hex string from that reading derives the target exactly.
2. **Join the community Telegram group and search first-hand for the promised hint** (needs a
   person). I already searched the full archived window (November 2021 to May 2026) and found
   nothing; what remains untested is anything from before the archive starts or outside its
   coverage.
3. **Puzzle #9's real solving method, if it ever surfaces** (needs new information). #9 was
   swept in 2020 by an anonymous solver who never published a method; a future write-up would
   give this folder its first certified, puzzle-specific image-to-key oracle.

Full notes: [analysis/leads.md](analysis/leads.md).

## Files in this folder

| Path | What it is |
|---|---|
| `clues/arweave-puzzle-11.png` | the published puzzle image, byte-exact, sha256 recorded in puzzle.json |
| `clues/author-posts.md` | the author's dated Twitter quotes, as reproduced by the community repository |
| `data/geometry.json` | the 12 building bounding boxes, the sailboat bounding box, and the 5 small sail widths |
| `data/lsb_scan.json` | stream counts, window counts, rate, and witness for the 2026-08-17 LSB scan |
| `analysis/tested.md` | the complete negatives ledger |
| `analysis/leads.md` | full notes behind the ranked leads |
| `images/01-annotated-geometry.png` | the annotated geometry figure |
| `tools/fig_geometry.py` | generates images/01-annotated-geometry.png from data/geometry.json |
| `tools/oracle.py` | 64-hex private key to ETH address; `--selftest` against private key 1 and puzzle #13 |
| `tools/lsb_scan.py` | prefix and sliding-window LSB extraction; `--selftest` plants head/middle/tail witnesses |

## Sources

- Tiamat, original announcement, Twitter, 2020-04-22 (deleted): https://twitter.com/arweavep/status/1252961944807641090
- Tiamat, "Next set of hints when AR reaches $100 :)", Twitter, 2021-08-23: https://twitter.com/arweavep/status/1429846914028158977
- Puzzle image, Arweave transaction CzITHnEIlkQw9SbaX5futCzFrKk1qe_NwvWnIBmP2fY: https://viewblock.io/arweave/tx/CzITHnEIlkQw9SbaX5futCzFrKk1qe_NwvWnIBmP2fY
- HomelessPhD, "AR_Puzzles" community repository, PZL11 entry, checked 2026-08-16: https://github.com/HomelessPhD/AR_Puzzles/tree/main/PZL11
- Zoren Lorenzana, Arweave Puzzle #13 write-up (spent-key certification vector), 2020-06-10: https://zorenx.medium.com/arweave-puzzle-series-puzzle-13-solved-d770655f705b
- Escrow address, Etherscan: https://etherscan.io/address/0xFF2142E98E09b5344994F9bEB9C56C95506B9F17
