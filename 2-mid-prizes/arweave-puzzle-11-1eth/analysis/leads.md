# Open leads, ranked

## 1. A hatch cipher that is not band-length or column-nibble maps (insight)

The author's "format does not matter" reply, and the separate remark about storing a
private key as "a weird image in your email account," still point at pixel content
rather than PNG chunks. Consecutive LSB, raw 8-bit windows, 2D tiles, downsampled
thumbnails, and hatch-band / column-nibble maps are now ruled out (see
`analysis/tested.md`): 40,596,966 pixel windows plus 276,674 nibble windows, 0 match,
0 copy of the known escrow address in those nibble streams, witnessed. What remains is
a reading of the drawing that is not "ink-band length, mean, width, or ink fraction
mapped to a nibble": Morse of stroke gaps, a glyph alphabet at a scale the 240-245
value-band does not contain (that band is speckle), or a passworded container. Confirms:
a 64-hex string taken from that reading derives the target exactly. Kills: a complete,
witnessed enumeration of one named encoding with 0 match.

## 2. Join the community Telegram group and search first-hand for the "$100" hint (needs a
person)

I already searched a full local archive of `@arweavep` (55,002 messages, November 2021 to May
2026) and found no later message announcing new hints, plus 47 messages from other members
independently confirming the promised follow-up never arrived. That closes this as a lead
inside the archived window. What remains untested is anything posted before the archive's
start (the announcement itself is from April 2020) or through a channel the archive does not
cover, such as a direct message or a since-deleted post. Confirms: a member with early access
to the group, or Tiamat directly, produces a hint not present in the archive. Kills: nothing
further can kill this lead technically; it depends on information I do not have a channel to.

## 3. Puzzle #9's real solving method, if it ever surfaces (needs new information)

Tiamat described puzzle #9 as "similar" to #11, and #9 was swept by an anonymous solver in
2020 who never published a method; multiple community members describe the last step as
"forced" (brute-forced), not derived from a stated rule. If a #9 write-up ever surfaces, it
would give a real, oracle-certifiable answer to calibrate #11's image-to-key mapping against,
which is exactly what this folder is currently missing. Confirms: a published #9 method that
this folder's harness can reproduce byte-exact, at which point the same method becomes a
certified candidate class for #11. Kills: nothing; this is a standing watch item, not an
active search.

## Killed: systematic consecutive LSB of grayscale and alpha

Killed 2026-08-17. `tools/lsb_scan.py --selftest` plants head/middle/tail witnesses and
recovers them. `--prefix` tested 3,768 unique candidates across 324 streams. `--slide`
tested 16,766,064 overlapping 32-byte windows (bit plane 0 in the listed orders and
alignments, plus the lowest 2, 3 and 4 bits of xy / non-white / ink). 0 match, 0 64-hex
ASCII string, 0 copy of the known escrow address in the packed bits. Counts in
`data/lsb_scan.json`. Remaining LSB-like ideas (a passworded OpenStego-style container, a
non-consecutive permutation of bits) need a constraint that shrinks N before they are worth
running.

## Killed: raw gray windows, 2D LSB/ink tiles, and downsampled thumbnails

Killed 2026-08-17. `tools/visual_scan.py --selftest` recovers an 8x4 raw plant and a
16x16 LSB plant. `--thumb` tested 2,803 unique downsampled and strip candidates.
`--raw` tested 13,508,314 overlapping 32-byte windows of raw gray (xy / yx / reverse /
non-white / ink) and 2x16 / 4x8 / 8x4 / 16x2 tiles. `--tiles` tested 10,322,588
overlapping 16x16, 32x8, and 8x32 tiles of LSB and of ink<110. 0 match. Counts in
`data/visual_scan.json`.

## Killed: hatch bands and column silhouettes as hex digits

Killed 2026-08-17. `tools/hatch_hex.py --selftest` recovers a 64-bar encoding of private
key 1 and a 40-bar encoding of the known escrow address hex. `--scan` tested 276,674
nibble windows (181,536 unique keys) across 30,453 streams of building floors, vertical
strokes, and column silhouette features. 0 match, 0 copy of the 40-hex escrow address.
Counts in `data/hatch_hex.json`.
