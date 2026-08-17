# Tested hypotheses, full ledger

Summary table is in the README. This file has the detail behind each row.

## The 64-hex reading transform, applied to a known answer

Hypothesis: the same 64-hex-to-address transform used for Puzzle #2 also holds for
Puzzle #1's published solution.

Method: `tools/oracle.py --selftest` derives Puzzle #1's published 64-hex string to
the address that received and later paid out that puzzle's 0.05 ETH.

Result: SELFTEST OK. Space: 1 known vector. Witness: yes, known-good input reproduced.
Date: 2026-08-16, re-run 2026-08-17.

## Temporal max-projection on the copies YouTube serves in 2026

Hypothesis: a temporal maximum-projection across each statement video reconstructs
Puzzle #1's known 64-hex, and applied to Puzzle #2 yields most of the 64 characters.

Method: download the current DASH 720p representations (itag 136, 30 fps, and itag 298,
60 fps). Puzzle #2 part 1 file metadata `creation_time` is 2023-02-27; part 2 is
2023-06-05. Measured bitrate is about 37 to 52 kb/s. Extract every frame, take a
per-pixel temporal max, and also track bright (luma above 160) blobs on each 40 px
frame edge and on the center column.

Result, Puzzle #1 statement videos: the max-projection of the copies served in 2026
does not contain a readable 64-hex string matching the known solution. Those copies
are also 2023 re-encodes (part 1 `creation_time` 2023-05-31, part 2 2023-07-07), about
60 to 82 kb/s. The 2026-08-02 claim that max-projection reproduces Puzzle #1 exactly
does not hold on these files; it may have used a pre-re-encode download.

Result, Puzzle #2: the same method does not yield 40 to 50 distinct hex characters.
What it does yield, with frame-accurate timing:

- Part 1 (`TRUUTryah70`): no bright edge glyphs until late in the video. Right-edge
  mid-frame blob 20.33 s to about 21.1 s; left-edge 20.63 s to about 21.6 s; top-edge
  24.23 s to about 25.3 s; bottom-edge 24.57 s to about 25.5 s. Blob centroids stay
  put (y about 360 on the sides, x about 650 on top and bottom); they do not travel
  around the perimeter. After a short interval of changing shapes, a static `4`
  dominates each pair of edges and then fades. That `4` is the decoy named in the
  published description.
- Part 2 (`U_0DtYHDPy0`): a center-column flash 25.87 s to 27.03 s with three
  brightness classes (about 7400, 9000, and 12700 pixels above luma 170 in a 60 px
  column), consistent with two overlaid layers that sometimes appear together. The
  word MIRROR is visible in the scene. Large `8` and `C` sit left and right of center
  from about 20.4 s to 25.8 s and are scene art, not the column.

IoU of consecutive edge masks often drops below 0.5, then recovers two frames later:
the 2023 encoder is blending or alternating two shapes rather than holding a clean
glyph. Unique-shape clustering therefore returns blends, not a 64-character tape.

Witness: oracle selftest still passes on the same machine; the negative is "these
files do not contain a complete readable 64-hex", not "the transform is wrong".
Count: 900 frames (part 1, 30 fps) plus 901 frames (part 2, 30 fps), plus the 60 fps
DASH files which are the same pictures at a higher frame rate, not a sharper encode.
Date: 2026-08-17.

## Template matching of Puzzle #2 edge crops against rendered hex digits

Hypothesis: correlating each distinct edge crop against the 16 hex-digit letterforms
(normal, mirrored, rotated 90/180/270) resolves the ambiguous cells.

Method: greedy IoU clustering (threshold 0.68) of bright edge crops in the four seam
windows above, then normalized cross-correlation against DejaVu and Liberation Bold
glyphs `0-9A-F`. Puzzle #1's solution-screen letterforms were not used as templates
because the current Puzzle #1 solution DASH was not obtained; the fonts are a stand-in.

Result: best correlations sit around 0.3 to 0.5, too weak to call a digit. No 64-hex
string was assembled, so nothing was submitted to the oracle from this pass. The
planned step is no longer "never run"; it is run and blocked by the encode, not by
missing code. Uncertified as a glyph reading (fonts are not the author's letterforms).
Date: 2026-08-17.

## Puzzle #1 private key under small algebraic transforms

Hypothesis: Puzzle #2's key is Puzzle #1's published key under a small transform
(rotate hex characters, reverse characters, reverse bytes, nibble swap, invert
nibbles, invert bytes, add a small integer).

Method: 85 candidates through `tools/oracle.py`. Space: 85. Rate: instant.

Result: all NO MATCH. Witness: yes, the same oracle reproduces Puzzle #1's known
address from its known key (`--selftest`). Date: 2026-08-17.

I am not listing the 85 strings. They are deterministic from Puzzle #1's already-public
solution and are not a reading of Puzzle #2.

## Visual inspection of unique 2023-encode crops

Hypothesis: looking at the unique edge and column crops one by one (the 40 IoU
clusters plus the part-2 even/odd column tiles) yields a 64-hex string worth
submitting to the oracle.

Method: inspect the clustered crops as high-contrast stills. No 64-hex string was
assembled, so nothing from this pass went to the oracle.

Result: uncertified as a reading. The same crop can be named as several different
hex digits depending on rotation, clipping, and encoder blend; that is not a
witnessed negative on the transform, only a statement that these files do not
give a complete key. Date: 2026-08-17.
