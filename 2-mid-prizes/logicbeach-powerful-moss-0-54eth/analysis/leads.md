# Open leads, ranked

## 1. Turn the sunburst rays into a per-hour word rule (hours)

The 24 sunburst rays have measurably varying red-pixel counts (about 604 to 947 along a
unit-spaced walk from the center). The last red pixel on most rays sits at nearly the same
radius (about 990 px); the 3-o'clock ray is the outlier, ending at 830 px. The red overlay
is also a labeled Cartesian grid: ticks at ±5 and ±10, origin on the word `road` at the
hub. I still do not have a wrap model that maps an (x, y) on this plot to the BIP39 word
under that pixel: a character-width packer fitted to 11 visual anchors only re-found the
two words at twelve o'clock on the plot. Until that readout is certified, ray length
and the ±5/±10 lattice cannot be turned into a 12-word candidate and fed to the oracle.
Confirms: a per-hour selection rule based on ray length or lattice point, fed through the
oracle, matches. Kills: a systematic pass over those rules with no match, after the wrap
or a visual read of all 12 sample points is itself witnessed.

## Closed on 2026-08-17

- **Numeral bottom pixel, plus or minus 1 row, 4 orderings.** 2,125,764 combinations, 0
  match. Re-run on 2026-08-17 through the 9-path neighbor sweep: still 0 match.
- **Outer-rim pixel, plus or minus 1 row, 4 orderings.** Same size, 0 match, including the
  later 9-path residual.
- **Widen one hour at a time** to a 5-to-7-word column window, every other hour held at the
  published pool, all 12 hours, 9-path sweep, 0 match.
- **Overlay / artist-name passphrases** on the published centroid pools (the original 16
  strings, then the spaced `logic beach` / `Logic Beach` / `LOGIC BEACH`), 0 match.
- **`logic` and `beach` as mnemonic words** (prefix, suffix, replace one hour, replace two
  hours), 0 match.
- **One BIP39 token per album track title**, 4 orderings, 0 match.
- **First 12 regular DKC2 level titles**, one BIP39 token each, 4 orderings, 0 match.
- **POAP LSB / bit-planes as a 12-word ASCII BIP39 run.** Extractor recovers a planted
  payload from a copy of the image; the real file has no such run.

Opening several hours at once to plus-or-minus 2 remains untested: 5^9 times 4 orderings is
about 7.8 million combinations and, with the 9-path sweep, sits above the two-hour cap. That
is a compute problem only if a new constraint first cuts the set.

Full ledger: [tested.md](tested.md).
