# Tested (full negatives ledger)

The target is a raw 256-bit private key with no intermediate checksum. Every candidate
below was checked by deriving its ETH address (uncompressed secp256k1 public key,
Keccak-256 of the 64-byte XY, last 20 bytes) and comparing it byte-exact against
`0xFF2142E98E09b5344994F9bEB9C56C95506B9F17`. From 2026-08-17 that comparison is
`tools/oracle.py`, certified against private key 1 and against Arweave Puzzle #13's
published already-spent key. I have no known-answer image-to-key pair for this puzzle,
so rows that hash geometry or metadata remain uncertified for the mapping from image
to key. The LSB rows below carry a synthetic witness: a known 32-byte key planted in
LSB of a cover, re-found at head, middle and tail by the same packer and slider. I
also flag near-misses (an ETH address starting with the same 2 bytes, `ff21`); none
occurred in any family below.

## Geometry-derived candidates

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Building height/width/roof-y/x0 sequences (raw, sorted ascending, sorted descending, interleaved), joined with 5 separator styles, padded left/right to 32 bytes, first/last 32 bytes, 2-hex-digit encoding per value | about 460 candidates total across this and the next 3 rows | SHA-256, double SHA-256, Keccak-256, compared to target address | 0 match, 0 near-miss (no derived address even starts with `ff21`) | uncertified (no known-answer vector for this puzzle) | 2026-06-13 |
| Raw pixel hashes: grayscale channel, alpha channel, full PNG file, first/last 32 bytes of the flat grayscale array | included above | SHA-256, Keccak-256 | 0 match, 0 near-miss | uncertified | 2026-06-13 |
| cHRM chunk (32 bytes) and its byte-reversed form, raw and hashed | included above | direct, SHA-256, Keccak-256 | 0 match, 0 near-miss | uncertified | 2026-06-13 |
| Object counts (12 buildings, 1 large sail, 5 small sails, 2 clusters, left/right counts) as a byte sequence | included above | SHA-256 | 0 match, 0 near-miss | uncertified | 2026-06-13 |
| Matrix reshape of the grayscale channel at 7 column widths, first/last row and column strips | 56 strips | first 32 bytes, SHA-256 | 0 match, 0 near-miss | uncertified | 2026-06-13 |
| Value-band pixel masks (bands including 240 to 245, 235 to 254, 248 to 254, 1 to 30) | 4 bands | SHA-256, first 32 bytes | 0 match, 0 near-miss | uncertified | 2026-06-13 |

## Metadata-derived candidates (the date:create / date:modify anomaly)

The PNG's own `tEXt` chunks (confirmed present in `clues/arweave-puzzle-11.png`, reproduced
2026-08-16) read `date:create 2020-03-30T11:38:07+03:00` and
`date:modify 2020-03-30T11:34:44+03:00`: the modify timestamp precedes the create timestamp,
an anomaly present only in this puzzle and its sibling puzzle #9.

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| ISO date strings, digit strings, Unix epochs, and their difference/sum/XOR, in decimal and big/little-endian 4 and 8-byte encodings, alone and concatenated or XORed with the address and the cHRM bytes | dozens of encodings times {SHA-256, double SHA-256, Keccak-256, BLAKE2s, first 32 bytes, last 32 bytes} | direct address comparison | 0 match, 0 near-miss | uncertified | 2026-06-13 |

## Alpha channel and sibling-puzzle-calibrated candidates

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| 260 near-white pixels from the sibling puzzle #9's own 8-level image, tested as a carrier under many bit orders (raster, polar, radial), bit widths (1 to 3 bits per pixel, MSB and LSB first), and symbol mappings, plus several passphrase guesses hashed with SHA-256, double SHA-256, and Keccak-256 | several hundred combinations | address comparison, calibrated against puzzle #9's real (and already spent) address as a positive control | 0 match, 0 near-miss on #9 itself (so the method is confirmed not to reproduce the known #9 answer either) | yes, on the #9 positive control only | 2026-06-13 |
| Container-level myths (embedded executable or filesystem inside the PNG) | full file | binwalk, manual chunk inspection | refuted: file is a clean, valid PNG (IHDR, gAMA, cHRM, bKGD, pHYs, 22 IDAT, 3 tEXt, IEND chunks), 0 bytes after IEND; the "executable" reports from other solvers are binwalk false positives on near-random decompressed pixel bytes | yes (direct chunk inspection) | 2026-06-13 |
| Alpha channel as a data carrier | full channel | direct pixel inspection | 434 pixels have alpha under 255, clustered on the large sailboat's outline (an anti-aliasing halo from a copy-paste), values 225 to 254 (a deficit of 1 to 30 from 255), consistent with a smoothed edge rather than structured data | yes | 2026-06-13 |

## Consecutive LSB and bit-plane readings of the grayscale and alpha channels

The published PNG is 1600x1105, 8-bit grayscale plus alpha. I extracted named pixel
sequences (full raster in row-major, reversed, column-major, boustrophedon, even/odd
pixels; non-white, non-black-or-white, near-white, ink-threshold, sailboat crop,
building band, alpha), then each bit plane 0-7 and the lowest 1-4 bits packed
MSB-first and LSB-first per byte. Counts are in `data/lsb_scan.json`, produced by
`tools/lsb_scan.py`.

| Hypothesis | Space | Method | Result | Witness | Rate | Date |
|---|---|---|---|---|---|---|
| Prefix, skip-leading-0x00/0xFF, 4-byte length header, SHA-256, double SHA-256, Keccak-256 of the first 1 KB, and any 64-hex ASCII, for 324 packed streams | 3,768 unique 32-byte candidates | `tools/lsb_scan.py --prefix` then `tools/oracle.py` | 0 match, 0 near-miss, 0 hex64 string, 0 encoding of the known 20-byte escrow address in the packed bits | yes: synthetic 32-byte key planted in LSB of a 32x32 cover and recovered as the packed prefix; oracle self-test against private key 1 and puzzle #13 | about 650 candidates/s (prefix pass is hash-dominated, 5.82 s total) | 2026-08-17 |
| Every overlapping 32-byte window of bit-plane 0 streams (gray xy plus 7 bit alignments, both packings; yx, reverse, boustrophedon, even/odd, non-white, whiteish, ink, sail, buildings, alpha; gray plane 1 xy) | 10,994,520 windows | `tools/lsb_scan.py --slide` bit0 family, address compare | 0 match | yes: three planted keys re-found at offsets 0, 2000 and 4064 of a 4096-byte synthetic stream | 47,815 windows/s | 2026-08-17 |
| Every overlapping 32-byte window of the lowest 2, 3 and 4 bits of the gray xy, non-white, and ink sequences, both packings | 5,771,544 windows | same slider and oracle | 0 match | yes: same head/middle/tail plants | about 44,000 windows/s | 2026-08-17 |

Cumulative for this family: 16,766,064 sliding windows plus 3,768 prefix candidates, 0 match.
This rules out a raw 32-byte private key stored as consecutive bits in those streams. It
does not rule out a passworded stego container, a non-consecutive bit order, or a visual
encoding that is not LSB.

## Raw gray windows, 2D tiles, and downsampled thumbnails

Raster LSB walks consecutive pixels in scan order. It does not walk raw 8-bit values as
the 32-byte key, and it does not walk 2D tiles (a 16x16 LSB block is 256 bits that are
not consecutive in the flattened raster). `tools/visual_scan.py` covers those, with
counts in `data/visual_scan.json`.

| Hypothesis | Space | Method | Result | Witness | Rate | Date |
|---|---|---|---|---|---|---|
| Downsampled thumbnails of the full image, the building band, and the sail, sizes 16x16 / 32x8 / 8x32 / 64x4 / 4x64 / 8x4 / 4x8 / 32x1 / 1x32, five resample filters, raw 32-byte form when the thumbnail has 32 pixels, otherwise ink/white packed at several thresholds; plus 32 equal-width mean strips | 2,803 unique 32-byte candidates | `tools/visual_scan.py --thumb` | 0 match | yes: `--selftest` recovers an 8x4 raw plant and a 16x16 LSB plant | n/a (small) | 2026-08-17 |
| Every overlapping 32-byte window of raw gray values (xy, yx, reverse, non-white, ink<110, ink<200) and every 2x16 / 4x8 / 8x4 / 16x2 tile of raw gray | 13,508,314 windows | `tools/visual_scan.py --raw` | 0 match | yes: same 8x4 raw plant | 60,707 windows/s | 2026-08-17 |
| Every overlapping 16x16, 32x8, and 8x32 tile of LSB and of ink<110, packed MSB-first with `np.packbits` | 10,322,588 windows | `tools/visual_scan.py --tiles` | 0 match | yes: same 16x16 LSB plant | 53,289 windows/s | 2026-08-17 |

Cumulative for this family: 23,830,902 sliding windows plus 2,803 thumbnail candidates, 0 match.
This rules out a raw 32-byte key stored as consecutive gray values in those streams, as a
32-pixel 2D tile, or as a 256-bit 16x16 / 32x8 / 8x32 LSB or ink tile. It does not rule
out a passworded stego container, a hatch-count cipher that is not a 32-byte window, or
a value-band that renders as hex text.

## Hatch bands and column silhouettes as hex digits

Raster windows pack pixels. This family reads the drawing as a sequence of hex digits:
horizontal ink bands (floors of hatching) and vertical ink bands (strokes) inside each
building, optionally the sail, plus per-column roof height, ink fraction, mean, and dark
runs of the building band. Each sequence is mapped to nibbles (mod 16, div 16, min-max
scaled, and reversed). 64-nibble windows are checked as keys. 40-nibble strings are
searched for the known escrow address hex. Counts in `data/hatch_hex.json`.

| Hypothesis | Space | Method | Result | Witness | Rate | Date |
|---|---|---|---|---|---|---|
| Horizontal floors and vertical strokes of the 12 buildings (and buildings+sail), thresholds 80-220 step 10, min band size 1-4, min ink fraction 0.08-0.3, mapped from band length/mean/width/ink-fraction; 32-band sequences also as raw bytes; column features of the building band, raw and binned to 32/40/64 | 276,674 windows (181,536 unique keys) across 30,453 streams | `tools/hatch_hex.py --scan` then the same eth_tail as `tools/oracle.py` | 0 match, 0 copy of the 40-hex escrow address in any nibble stream | yes: 64 bars encoding private key 1 recovered; 40 bars encoding the escrow hex re-found | about 31,000 windows/s (8.76 s total) | 2026-08-17 |

Value-band 240-245 as rendered glyphs is separately weak: that band has 11,199 connected
components, largest 16 pixels, 0 components matching a digit-like aspect/area cut
(area 30-800, height 8-80, aspect 0.25-1.4). That is a count of blobs, not an OCR
oracle, so it is not a witnessed negative on every possible glyph alphabet.

## What the geometry, metadata, LSB, visual-scan, and hatch-hex sweeps together rule out

The geometry and metadata families together covered on the order of 1,000 candidates, 0
match, 0 near-miss. The LSB family covered 16,766,064 sliding windows plus 3,768 prefix
candidates, 0 match. The visual-scan family covered 23,830,902 sliding windows plus 2,803
thumbnail candidates, 0 match. The hatch-hex family covered 276,674 nibble windows
(181,536 unique keys), 0 match, 0 copy of the known escrow address hex. Together these
rule out every direct single-transform reading of the measured geometry and the metadata
anomaly that I enumerated, a raw 32-byte key stored as consecutive bits or consecutive
gray values in the listed streams, a 16x16-style LSB or ink tile, and hatch-band or
column-silhouette sequences mapped to hex digits by length, mean, width, or ink fraction.
They do not rule out a passworded stego container, a hatch cipher that is not one of
those nibble maps, or a reading that depends on the promised but never-delivered "$100"
hint (see "Open leads, ranked").
