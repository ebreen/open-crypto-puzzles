# Tested (full negatives ledger)

Every derivation row uses `tools/oracle.py`: a candidate only counts as a match if the derived
ETH address equals the winner wallet `0x635739254BDE27d28301f25aD57c3cAC3C3468f3` exactly,
under any of the 9 swept BIP44 paths (3 accounts times 3 indexes). Witness: the oracle's own
`--selftest` reproduces the public BIP39 KAT address, a positive control that points the oracle
at the KAT's own address, a negative control against the real winner wallet, an invalid-checksum
rejection, and the artist's prior solved "Bifurcations" BIP84 vector, before every run below.

## Audio channel (the toolbox that solved the artist's prior puzzle, "Bifurcations")

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Spectrogram text, Morse (kick/snare as dash/dot), SSTV (including invert-merge), theme-keyed hex offsets, LSB and bit-plane analysis, RIFF/XMP metadata, mid-side decoding, sub-20Hz content, small and medium ASR, demucs vocal isolation plus ASR, run on all 12 lossless masters | 12 tracks times the full toolbox | the same toolbox that solved "Bifurcations" (2020) | negative on all 12 tracks | yes (the toolbox is confirmed to work, since it is what solved the prior puzzle) | 2026-06-17 |

The masters themselves measure at close to 0 percent energy above 13 kHz, which is a property
of the recording, not a playback or re-encoding artifact, so no high band exists to carry
spectrogram text on this album at all. This is why the audio channel is closed for this puzzle
even though the identical toolbox worked on the prior one.

## POAP clock-and-wordlist image (the carrier for this puzzle)

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Word-per-hour read at the numeral centroid plus 1 row (3 candidates per hour), 4 canonical orderings (clockwise, reverse, 12-first clockwise, 12-first counterclockwise) | 1,193,373 combinations tested (132,597 checksum-valid) | BIP44 m/44'/60'/0'/0/0 plus neighbor sweep | 0 match, 131.8 seconds | yes | 2026-07-14 |
| Asymmetric row window (centroid plus or minus 1 row), each of the 4 orderings separately | 531,441 combinations per ordering (about 33,000 checksum-valid each) | same oracle | 0 match | yes | 2026-06-17 |
| Wider asymmetric window refinement (best visual reads with row-aware neighbors) | about 8.6e8 estimated space, sampled rather than exhausted | same oracle | 0 match on the sampled region | yes | 2026-06-17 |
| Distinct-overlay hypothesis (12 words marked by a different color or intensity) | full image histogram | gray-intensity and hue histogram analysis | refuted: exactly 1 gray text population, only 2 non-gray hue families (the red sunburst spokes, the yellow title and signature); no marking of any kind at any of the 12 numeral positions | yes (direct pixel measurement) | 2026-06-17 |
| Higher-resolution or vector source | prize contract tokenURI, POAP asset server, artist website, album video | direct fetch and comparison | refuted: the 2004x2011 raster in this folder is the finest source found anywhere; the album video is 1080p, lower resolution than the plot | yes | 2026-06-17 |
| Calibration against a known-answer "Bifurcations" POAP | POAP GraphQL query for any drop with "bifurcation" in its name | direct API query | refuted: 0 drops match; no known-answer clock image exists for this artist to reverse-engineer the readout rule from | yes | 2026-06-17 |
| Bottom-of-numeral readout: each hour's word taken from the text row under the glyph's lowest pixel, plus or minus 1 row, 4 canonical orderings | 2,125,764 combinations (531,441 per ordering; 132,627 checksum-valid) | visual re-read of all 12 numerals on `clues/powerfulmoss-poap.png`, then BIP44 `m/44'/60'/0'/0/0` only | 0 match, 113.5 seconds, 18,722 combinations/s | yes: a checksum-valid phrase from this generator was derived to its own address and re-found through the same checker | 2026-08-17 |
| Outer-rim readout: each hour's word taken from the text toward the circle edge of that numeral, plus or minus 1 row, 4 canonical orderings | 2,125,764 combinations (133,370 checksum-valid) | same method as the bottom-pixel family | 0 match, 111.2 seconds, 19,112 combinations/s | yes: same planted-witness procedure | 2026-08-17 |
| Widen one hour at a time to a 5-to-7-word column window (centroid plus or minus 2 or 3 rows), keep every other hour at the published pool, 4 canonical orderings, all 12 hours | 2,781,864 combinations across 12 separate runs (hours 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12); checksum-valid about 6.3 percent | `tools/oracle.py` 9-path neighbor sweep | 0 match | yes: each run planted a checksum-valid phrase from its own generator and re-found it | 2026-08-17 |
| Published centroid pools plus a wallet passphrase taken from the yellow overlay and artist name (`lead`, `moss`, `powerful moss`, `logicbeach`, `clock`, `poap`, and case variants; 16 strings) | 1,259,712 combinations (80,304 checksum-valid) | BIP44 `m/44'/60'/0'/0/0` with each passphrase | 0 match, 88.4 seconds | yes: checksum-valid phrase plus passphrase `lead` derived and re-checked | 2026-08-17 |

The first 2026-08-17 bottom-pixel, outer-rim, and 16-string passphrase families compared only the canonical path `m/44'/60'/0'/0/0`. I later re-ran the bottom-pixel and outer-rim pools through the 9-path neighbor sweep (see the residual rows below). The one-hour widen family used the 9-path sweep from the start.

## Artist-name words, track titles, and the DKC2 nod (2026-08-17, second pass)

The yellow overlay on the POAP is the block letters `POWERFUL MOSS` plus a cursive `LOGIC BEACH`. `logic` and `beach` are BIP39 words; `moss` is not. The album page also says the record has 12 tracks and was scored with Donkey Kong Country 2 soundfonts. Those are three bounded ways to pick 12 words that are not "the word under the numeral."

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| One BIP39 token per track title (longest-substring alternatives: era; power; any/man; empty/long/wave; rare; comfort/edit; curve; forest; fall/all; cliff/side; shadow/real; antenna/wave/ten), 4 orderings | 1,152 combinations (66 checksum-valid) | `tools/oracle.py` 9-path neighbor sweep | 0 match, 0.3 seconds | yes: a checksum-valid phrase from this generator was derived to its own address and re-found through the same checker | 2026-08-17 |
| `logic beach` or `beach logic` as the first two words, remaining ten from published hours 3-12 | 4,374 combinations (283 checksum-valid) | 9-path sweep | 0 match, 1.2 seconds | yes: same planted-witness procedure | 2026-08-17 |
| Published hours 1-10, then `logic beach` or `beach logic` as the last two words | 13,122 combinations (832 checksum-valid) | 9-path sweep | 0 match, 2.1 seconds | yes | 2026-08-17 |
| Replace exactly one published hour with `beach`, 4 orderings | 472,392 combinations (29,569 checksum-valid) | 9-path sweep | 0 match, 31.5 seconds, 14,979 combinations/s | yes | 2026-08-17 |
| Replace two published hours with `logic` and `beach` (all ordered pairs), 4 orderings | 2,519,424 combinations (156,771 checksum-valid) | BIP44 `m/44'/60'/0'/0/0` only | 0 match, 141.9 seconds, 17,751 combinations/s | yes | 2026-08-17 |
| Published centroid pools plus the spaced passphrases `logic beach`, `Logic Beach`, and `LOGIC BEACH` (not in the earlier 16-string set) | 78,732 combinations each, 236,196 total (5,019 checksum-valid each) | BIP44 `m/44'/60'/0'/0/0` with each passphrase | 0 match | yes | 2026-08-17 |
| First 12 regular DKC2 levels in published order, one BIP39 token per title (panic/rate, main/race, alley/all, lock, trouble/sail/top, head, aim, lava, ride, shaft, barrel/bar/you, all), 4 orderings | 288 combinations (14 checksum-valid) | 9-path sweep | 0 match | yes | 2026-08-17 |
| Bottom-of-numeral ±1 pools again, 4 orderings, 9-path neighbor sweep (the residual left by the canonical-only run) | 2,125,764 combinations (132,627 checksum-valid) | 9-path sweep | 0 match, 146.9 seconds, 14,474 combinations/s | yes | 2026-08-17 |
| Outer-rim ±1 pools again, 4 orderings, 9-path neighbor sweep | 2,125,764 combinations (133,370 checksum-valid) | 9-path sweep | 0 match, 145.0 seconds, 14,665 combinations/s | yes | 2026-08-17 |
| POAP image LSB and bit-planes as a 12-word ASCII BIP39 run (R/G/B/A LSB, R planes 0-7, R LSB column-major) | 4 channels plus 8 red bit-planes plus one column-major packing | pack bits, split on non-letters, require 12 consecutive BIP39 tokens | 0 runs; none of the probe strings `leisure`, `strategy`, `logic`, `beach`, `stick` appear as raw ASCII either | yes: the same packer recovered a planted `<<leisure strategy stick ...>>` payload from a copy of the image | 2026-08-17 |

## Explicitly not fed to the oracle

Sung lyrics on 2 tracks (DiscomfortMeditation, ShadowRealm) contain several BIP39 wordlist
tokens among their ordinary lyrics. I did not test any permutation of these: no mechanism
selects which 12 of the many lyric tokens would be the seed or in what order, so testing them
would be an unbounded search with no stopping rule, not a bounded hypothesis. This is listed
as untested, not as a negative.

## Summary

Across the POAP-image family, the earlier 1,193,373 plus 531,441 times 4 plus a sampled
8.6e8-sized space, the first 2026-08-17 addition of 8,293,104 combinations (bottom-pixel,
outer-rim, one-hour widen, and overlay passphrases), and the second 2026-08-17 addition of
7,498,476 combinations (track titles, `logic`/`beach` insertions, three spaced passphrases,
the first 12 DKC2 level titles, and the 9-path residual on the bottom-pixel and outer-rim
pools), have been checked, 0 matches, 0 partial hits. The POAP LSB/bit-plane scan is a
separate certified negative: the extractor recovers a planted phrase from a copy of the
image and finds no 12-word BIP39 ASCII run on the real file. Sampling the numeral, swapping
in the artist-name words, reading one token per track or per DKC2 level, and sweeping the
neighbor paths on the earlier rim families is not enough. What remains is a selector that
is not "the word under the clock numeral" and not those name/title substitutions: the
sunburst rays still have no certified word-selection rule, and opening several hours at
once to plus-or-minus 2 still sits above the two-hour cap.
