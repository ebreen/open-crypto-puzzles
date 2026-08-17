# Open leads, ranked

## 1. Test the sunburst ray length as an alternative per-hour selector (hours)

The 24 sunburst rays on the plot have measurably varying red-pixel counts (about 604 to 947
along a unit-spaced walk from the center). The last red pixel on most rays sits at nearly the
same radius (about 990 px); the 3-o'clock ray is the outlier, ending at 830 px. Ray length has
still not been turned into a word-selection or ordering rule and fed to the oracle. Confirms: a
per-hour selection rule based on ray length, fed through the oracle, matches. Kills: a
systematic pass over ray-length-based selection rules with no match, though this space is less
bounded than the row-window leads and would need its own scoping before a run.

## Closed on 2026-08-17

- **Numeral bottom pixel, plus or minus 1 row, 4 orderings.** Visual re-read of all 12 glyphs,
  2,125,764 combinations, 0 match, witness planted and re-found. Canonical path only.
- **Outer-rim pixel, plus or minus 1 row, 4 orderings.** Same size, 0 match, same witness
  procedure.
- **Widen one hour at a time** to a 5-to-7-word column window, every other hour held at the
  published pool, all 12 hours, 9-path sweep, 0 match.
- **Overlay / artist-name passphrases** on the published centroid pools (16 strings including
  `lead`, `powerful moss`, `logicbeach`), 0 match.

Opening several hours at once to plus-or-minus 2 remains untested: 5^9 times 4 orderings is
about 7.8 million combinations and, with the 9-path sweep, sits above the two-hour cap. That
is a compute problem only if a new constraint first cuts the set.

Full ledger: [tested.md](tested.md).
