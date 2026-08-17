# Open leads, full notes

Ranked summary is in the README. This file has the reasoning behind the ranking.

## 1. A copy of the two videos from before YouTube re-encoded them in 2023

The copies YouTube serves now (`creation_time` 2023-02-27 and 2023-06-05 on the DASH
720p files) are about 37 to 52 kb/s. At that rate a 30-second, mostly-static video
keeps title cards and a long-held decoy `4`, and smears the short seam and column
flashes into blended shapes. There is no 1080p representation in the current MPD
(itags 160, 134, 136, 298 only).

What would confirm this lead: any file whose encoder date, bitrate, or per-frame
residual shows the 2018 upload, for example a 2018 youtube-dl archive, a Wayback
save of the actual media (the watch-page captures from 2020 are redirects only), or
the author's original. On a clean encode, the seam windows timed on 2026-08-17
(part 1 sides about 20.3-21.7 s, top/bottom about 24.2-25.8 s; part 2 column about
25.9-27.0 s) are where to look first.

What would kill it: a clean encode in which those windows still only show a handful
of blended glyphs. Then the 64 hex is not a simple "read the bright characters" job
on these two videos, and the grammar from Puzzle #1 needs to be rebuilt from scratch.

Cost: finding a file, not compute. I do not have one.

## 2. Replay Puzzle #1's statement videos on a pre-2023 copy

Puzzle #1 part 1 is described as a horizontal hex ticker and part 2 as upside-down
hex whose 180-degree rotation is a suffix of the known key. That grammar is the
strongest analogue for Puzzle #2 (edges plus a mirrored column). The statement
videos YouTube serves now are also 2023 re-encodes (about 60 to 82 kb/s, 20 s).
Max-projection of those copies does not reconstruct the known 64-hex, so the grammar
cannot be certified against them.

What would confirm it: a pre-2023 copy of `3l1jFa3Mw0s` and `hX-pOBj8VsI` from which
max-projection or a ticker spacetime plot reproduces
`4487FC620AD0C4C67E80BE342B2EA1F5A3DC482BE6FB9C2451007322EA8BE35F`. Then apply the
same extraction to Puzzle #2's matching windows.

What would kill it: even a clean Puzzle #1 copy where the published description
(ticker, upside-down suffix) does not match the pixels. Then the written grammar is
wrong and Puzzle #2 needs a fresh reading model.

Cost: the same missing file as lead 1, plus minutes of extraction once it exists.

## 3. Template matching against Puzzle #1's solution-screen letterforms, on a clean encode

The 16 hex shapes on Puzzle #1's "THE SOLUTION" screen (held for the last about 6 s
of `0jJ6XadOAWk`) are the author's own letterforms. A pass against generic Bold
sans-serif fonts on the 2023 Puzzle #2 crops did not call digits (see tested.md).
Repeating that pass with the solution-screen glyphs as templates, on un-smeared
cells, is still the right classifier once lead 1 supplies those cells.

What would confirm it: a 64-hex string that `tools/oracle.py` reports as MATCH.
What would kill it: clean cells that still do not correlate with those 16 shapes
under rotation and mirroring. Then the Puzzle #2 glyphs are a different alphabet.

Cost: hours after a clean encode exists; minutes of oracle checks.

## 4. Bounded 16^k sweep only after a real gap

If a clean read leaves 8 or fewer undetermined hex characters, sweeping 16^8 against
the offline oracle is cheap. The 2023 encode does not leave a gap that small: it
leaves almost the whole string undetermined. Sweeping 16^12 or larger is the wrong
move; shrink N by reading, do not ask for more compute.

A public comment on part 1 ("I have 16 hex") is consistent with each video
contributing 16 characters, but it is not a reading I can certify and I do not treat
it as 48 characters left to brute-force.

What would confirm it: an actual 8-or-fewer nibble gap from leads 1-3.
What would kill it: a gap larger than 8 after those leads. Then keep reading.
Cost: minutes, conditional.
