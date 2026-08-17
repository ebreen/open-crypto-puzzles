# Crypto Puzzles 2018: Puzzle #2 (0.05 ETH, [OPEN])

A small YouTube channel called "Crypto Puzzles" ran two video puzzles in July and
August 2018, each locking 0.05 ETH behind a hidden 64-character private key
encoded as glyphs in the footage, no address ever stated by the author. Puzzle #1
was solved within 3 hours of release and its prize was claimed; Puzzle #2, posted
5 days after Puzzle #1's escrow was funded by the same wallet for the same
amount, has sat untouched for 8 years. The transform is certified end to end
using Puzzle #1's own published solution as a known-good vector. What is missing
is a complete visual read of Puzzle #2's two videos. The copies YouTube serves
today are 2023 re-encodes at about 40 kb/s; they keep title cards and a static
decoy `4`, and smear the short seam and column flashes, so the earlier claim that
about 40 to 50 of 64 hex characters are already legible does not hold on those
files.

## At a glance

| | |
|---|---|
| Author | unnamed; YouTube channel "Crypto Puzzles" ([channel](https://www.youtube.com/channel/UCR8-P07nNhxyEr6fwJXvjQQ)) |
| Published | 2018-08-06, YouTube, two videos ([part 1](https://www.youtube.com/watch?v=TRUUTryah70), [part 2](https://www.youtube.com/watch?v=U_0DtYHDPy0)) |
| Prize | 0.05 ETH (about $94 at ETH = $1,880, 2026-08-16) |
| Chain | ethereum |
| Escrow | `0x1fa8Be9De5bBFE047C72dB8E8E3257128F7661ad` ([explorer](https://etherscan.io/address/0x1fa8Be9De5bBFE047C72dB8E8E3257128F7661ad)) |
| Last on-chain check | 2026-08-17: funded and unspent (0.05 ETH), nonce 0, this key has never signed anything |
| Status | OPEN |
| Puzzle type | raw-private-key, image-stego, video-series |
| Target format | 64-character hex private key (32 bytes), secp256k1, Keccak-256 of the uncompressed public key to a 20-byte address, no BIP39, no passphrase, no derivation path |
| Certified oracle | yes: `tools/oracle.py --selftest` (certified against Puzzle #1's own published solution, same series) |
| What remains | a complete visual read from a pre-2023 copy of the two videos; the 2023 YouTube encodes smear the glyphs |
| Series | same channel as the solved Puzzle #1 (different, already-spent address); no separate folder |

## The puzzle as published

The channel posted two videos for each puzzle: a statement and, once solved, a
solution reveal. Puzzle #1's statement videos are
[3l1jFa3Mw0s](https://www.youtube.com/watch?v=3l1jFa3Mw0s) and
[hX-pOBj8VsI](https://www.youtube.com/watch?v=hX-pOBj8VsI); its solution reveal,
["Crypto Puzzle 1 Solved!"](https://www.youtube.com/watch?v=0jJ6XadOAWk), shows a
"THE SOLUTION" screen with 64 hex characters across 3 lines, held stable for the
last 6 seconds of the video, not revealed one character at a time. Puzzle #2's
two videos, [part 1](https://www.youtube.com/watch?v=TRUUTryah70) and
[part 2](https://www.youtube.com/watch?v=U_0DtYHDPy0), posted 2018-08-06, show
composite glyphs instead: part 1 wraps glyphs around the frame edges and reveals
them through two "seam" sequences (one rotated 90 degrees, one upright), with a
static decoy digit mixed in; part 2 is a mirrored scene with a vertical column
alternating between two overlaid layers. The channel has 5 videos total, about
785 combined views, and no public writeup for either puzzle in 8 years. I do not
reproduce any video frames here, since they are the author's copyrighted video
content; both puzzles are linked above by video ID.

## What is understood

### Mechanism

The author never publishes an address for either puzzle: the 64-character hex
string shown in each solution video is the private key itself, and the address
is what it derives to. No BIP39, no passphrase, no intermediate derivation. The
same funder wallet, `0x0a937ec94abc55d92f5740a988a122ebdcab2e15`, sent exactly
0.05 ETH to Puzzle #1's escrow on 2018-07-19 and to Puzzle #2's presumed escrow
on 2018-08-01, 5 days before Puzzle #2's videos went up. That the second address
is Puzzle #2's escrow is a strong inference from the funder and amount matching,
not a fact the author stated directly.

### Derivation and oracle

```
python3 tools/oracle.py --selftest
python3 tools/oracle.py "<64 hex chars>"
```

A 64-character hex candidate is read as a raw secp256k1 private key, its
uncompressed public key is hashed with Keccak-256, and the last 20 bytes of the
digest, checksummed, are compared to the escrow address.

### Certified against

`tools/oracle.py --selftest` reproduces Puzzle #1's own published answer:
`4487FC620AD0C4C67E80BE342B2EA1F5A3DC482BE6FB9C2451007322EA8BE35F`, read off that
puzzle's own solution video, derives to
`0xc99A54EEA6036115f913A13D6606e935bcA47a8f`, the address that received 0.05 ETH
on 2018-07-19 and was spent from by its winner on 2018-07-26. Reproduced
2026-08-16. This confirms both the transform and that the author genuinely pays.

### Established facts

1. Puzzle #2's escrow is funded and unspent as of 2026-08-17 (checked by RPC
   against a public Ethereum node): balance 0.05 ETH, nonce 0, one incoming
   transaction, none outgoing. Puzzle #1's escrow, re-checked the same day,
   holds 0 ETH, consistent with having been spent by its winner on 2018-07-26.
2. Reading Puzzle #1's own solution screen and deriving from it reproduces the
   address Puzzle #1 actually paid out, confirming the 64-hex-to-address
   transform (see Certified against). Its solution screen is stable for its
   last 6 seconds, not an animation revealing characters one at a time.
3. A temporal maximum-projection of the Puzzle #1 statement videos was reported
   on 2026-08-02 as reconstructing that known 64-hex. The copies YouTube serves
   in 2026 are 2023 re-encodes at about 60 to 82 kb/s; max-projection of those
   files does not reconstruct the string.
4. Puzzle #2's current DASH 720p files are also 2023 re-encodes (part 1 encoder
   date 2023-02-27, part 2 2023-06-05), about 37 to 52 kb/s, no 1080p representation.
   On those files the seam and column windows can be timed (part 1 sides about
   20.3-21.7 s, top/bottom about 24.2-25.8 s, with a static decoy `4`; part 2 center
   column about 25.9-27.0 s, two brightness layers, mirrored scene) but they do not
   yield a complete 64-hex. A public comment on part 1 ("I have 16 hex") is
   consistent with 16 characters per video and is not a certified reading.

## What has been tested

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| The 64-hex-to-address transform, applied to Puzzle #1's published solution | 1 known vector | `tools/oracle.py --selftest` | SELFTEST OK | yes: known-good input reproduced | 2026-08-17 |
| Temporal max-projection of the 2023 YouTube DASH copies reconstructs Puzzle #1's 64-hex and most of Puzzle #2's | 2 videos, 1801 frames at 30 fps | per-pixel temporal max plus bright-blob tracking on edges and the center column | does not reconstruct Puzzle #1's known string; Puzzle #2 yields timed seam/column windows and a static decoy `4`, not 40-50 distinct hex characters | yes: oracle selftest still passes; the negative is about these files | 2026-08-17 |
| Template matching of Puzzle #2 2023-encode edge crops against rendered `0-9A-F` | about 40 unique edge clusters times 16 glyphs times 4 orientations | IoU clustering then normalized cross-correlation | correlations too weak to call a digit; no 64-hex assembled | uncertified as a reading (fonts are not the author's letterforms); oracle unused | 2026-08-17 |
| Puzzle #2's key is Puzzle #1's key under a small algebraic transform | 85 | rotate, reverse, nibble/byte invert, small integer add, then oracle | all NO MATCH | yes: same oracle, selftest OK | 2026-08-17 |
| Unique 2023-encode edge and column crops can be read by eye into a 64-hex | about 40 unique clusters plus part-2 even/odd tiles | visual inspection of high-contrast stills | no 64-hex assembled; crops remain blends and partials | uncertified as a reading; oracle unused | 2026-08-17 |

## Open leads, ranked

1. **A copy of the two Puzzle #2 videos from before YouTube re-encoded them in 2023**
   (finding a file, not compute). The current DASH 720p streams are about 40 kb/s
   and smear the seam and column flashes. A 2018 youtube-dl archive, an original
   file, or any media save from before 2023 is the bottleneck. The 2026-08-17 timing
   (part 1 sides about 20.3-21.7 s, top/bottom about 24.2-25.8 s; part 2 column about
   25.9-27.0 s) says where to look first on a clean encode.
2. **Replay Puzzle #1's statement videos on a pre-2023 copy** (minutes, once the
   file exists). The published grammar (horizontal ticker, then upside-down suffix)
   cannot be certified against the 2023 statement encodes; max-projection of those
   files does not reconstruct the known 64-hex. A clean Puzzle #1 copy is the
   analogue for Puzzle #2.
3. **Template matching against Puzzle #1's solution-screen letterforms, on a clean
   encode** (hours after lead 1). A pass against generic Bold fonts on the 2023
   crops did not call digits. The author's own 16 shapes on the solution screen are
   still the right templates once the cells are not smeared.
4. **Bounded 16^k sweep only after a real gap** (minutes, conditional). If a clean
   read leaves 8 or fewer undetermined hex characters, sweeping 16^8 against the
   offline oracle is cheap. The 2023 encode does not leave a gap that small.

## Files in this folder

| Path | What it is |
|---|---|
| `tools/oracle.py` | 64-hex private key to Ethereum address checker, certified against Puzzle #1's own solution |
| `analysis/tested.md` | full ledger behind the tested table |
| `analysis/leads.md` | reasoning behind the ranked leads |

## Sources

- Crypto Puzzle 1, statement part 1: https://www.youtube.com/watch?v=3l1jFa3Mw0s (2018-07-19)
- Crypto Puzzle 1, statement part 2: https://www.youtube.com/watch?v=hX-pOBj8VsI (2018-07-19)
- Crypto Puzzle 1 Solved!: https://www.youtube.com/watch?v=0jJ6XadOAWk (2018-07-19)
- Crypto Puzzle 2, part 1: https://www.youtube.com/watch?v=TRUUTryah70 (2018-08-06)
- Crypto Puzzle 2, part 2: https://www.youtube.com/watch?v=U_0DtYHDPy0 (2018-08-06)
- Channel "Crypto Puzzles": https://www.youtube.com/channel/UCR8-P07nNhxyEr6fwJXvjQQ
