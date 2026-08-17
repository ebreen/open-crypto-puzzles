# Arweave Puzzle Weave #12 (400.00248121 AR, [OPEN])

Tiamat (@ArweaveP) published this puzzle on the Arweave permaweb on 2020-04-29 and
announced it on Twitter on 2020-05-05: one jigsaw image with 4 pieces feeding a single
free-text field. The author confirmed the answer is exactly 58 characters and
case-sensitive. I certified the decrypt pipeline against a solved sibling and read
piece 3 as `2111011` from the page's own printed numbers. Colour-name and hex flag
readings, the 18-character investor names they force, companies and species named after
a whale, and the printed order of the five letters, went through the certified oracle:
794,659 candidates, 0 match. The open gap is a flag reading that is not English colour
words or RRGGBB, which would give the whale piece a different length.

## At a glance

| | |
|---|---|
| Author | Tiamat, [@ArweaveP on Twitter](https://twitter.com/arweavep) |
| Published | 2020-05-05, Twitter ([announcement](https://twitter.com/arweavep/status/1257613928185675776)), page live since 2020-04-29 |
| Prize | 400.00248121 AR (about $724 at AR = $1.81, 2026-08-16) |
| Chain | arweave |
| Escrow | `XRGEfkMbCMHeTY9mZI9Lh6hf8EmA8RstmBFUjDm40fg` ([explorer](https://viewblock.io/arweave/address/XRGEfkMbCMHeTY9mZI9Lh6hf8EmA8RstmBFUjDm40fg)) |
| Last on-chain check | 2026-08-17: funded and unspent, 400002481210000 winston, 0 outgoing transactions ever |
| Status | OPEN |
| Puzzle type | word-selection, geometry, text-cipher |
| Target format | one 58-character case-sensitive answer, 4 sub-answers concatenated with no separator, SHA-512 x11513, AES-decrypt to an Arweave JWK keyfile |
| Certified oracle | yes: `tools/oracle.py --selftest` (certified against solved sibling Arweave Puzzle Weave #8) |
| What remains | a flag reading other than colour names or hex, which sets the whale string's length |
| Series | Arweave Puzzles (this folder covers puzzle #12 only) |

## The puzzle as published

The live page shows one jigsaw JPEG cut into 4 pieces and a single free-text input field
wired to the decrypt routine. Piece 1 shows 6 flags in 3 vertical pairs; piece 2 shows a
whale beside the handwritten date "16-03-2020"; piece 3 shows geometric shapes each
carrying a printed digit string; piece 4 shows 5 letters rendered in a hatching pattern.
On 2020-05-23, replying to a question about the answer format, the author wrote,
["58 chars CS"](https://twitter.com/arweavep/status/1264211142714499072), confirming an
exact 58-character, case-sensitive answer. On 2020-04-14 he posted a series-wide status
update,
["1,2,4,8 = solved / 3,5,7,9 = not solved yet"](https://twitter.com/arweavep/status/1250036746802298885),
placing puzzle #12 among the unsolved half of the series at that time.

## What is understood

### Mechanism

The page reads the single free-text field verbatim (case-sensitive, no trimming),
stretches it with SHA-512 applied 11,513 times, and uses the resulting 128-character hex
digest as an EvpKDF/AES-OpenSSL password to decrypt an embedded ciphertext. Success is
declared only if the plaintext contains the literal marker `"kty":"RSA"`. This CryptoJS
block is byte-identical, script for script, to the ones in sibling puzzles #3 and #8,
including the same non-standard 1024-bit-key, 38-round Rijndael quirk (crypto-js issue
#293). The 58-character answer is the concatenation, in piece order, of the 4 jigsaw
sub-answers, with no separator between them.

### Derivation and oracle

```
python3 tools/oracle.py --selftest          # reproduces the solved sibling Arweave #8
python3 tools/oracle.py "BlueAndreessenHorowitz2111011Alien"
python3 tools/oracle.py --stdin             # one candidate per line
```

A candidate is passed through exactly as typed (case-sensitive, no trimming).
`MATCH <address>` on a hit, `NO MATCH` otherwise. Since no dependency available to this
repository implements CryptoJS's non-standard Rijndael variant, the oracle reimplements
it in pure Python; the implementation was checked to reproduce a standard AES-256 library
exactly at the standard key size before being trusted at this puzzle's non-standard one.

### Certified against

`tools/oracle.py --selftest` decrypts the real ciphertext of the solved sibling Arweave
Puzzle Weave #8 with its published answer, `RasputinWilhelmAlekhine`, and recovers a JWK
whose derived address matches `ayJQH1S6Fi52OEokLVi2tl5kr_y39LSfhJcNV0z9Ny4` exactly, the
address baked into that puzzle's own success page. Puzzle #8's escrow is already spent
(checked 2026-08-16), so this is historical calibration data, not a live prize. The
oracle's raw decrypt output was also checked byte-for-byte against this puzzle's own
JavaScript decryptor running under Node, on both matching and non-matching passphrases.

### Established facts

1. The escrow is funded and unspent: 400.00248121 AR, checked via
   `arweave.net/wallet/<address>/balance` on 2026-08-17; a GraphQL query for the wallet's
   own transaction history returns 0 outgoing transactions ever.
2. The author confirmed the answer is exactly 58 characters, case-sensitive.
3. Piece 3 is solved with certainty: the shapes read as `2111011` (spelling HEXAGON, one
   digit per letter, 0 for a descender, 1 for x-height, 2 for an ascender), a rule that
   reproduces all 3 printed numbers on the page with no free parameter.
4. Piece 4's hatching direction is not an ordering scheme: all 24 direction-to-digit
   assignments across 6 quadrant reading orders (144 combinations) fail to produce a
   1-to-5 permutation or a valid 5-letter word.
5. No steganography was found in the jigsaw image or the page's favicon (no EXIF or XMP
   data, no trailing bytes, `zsteg -a` returns noise only); the author's wallet history
   shows no companion transaction near the funding or publication window other than a PNG
   image identical to sibling puzzle #11's.

## What has been tested

Full ledger in [analysis/tested.md](analysis/tested.md). Summary:

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Piece 4 hatching as an ordering scheme | 144 combinations | exhaustive structural check | refuted: no valid permutation or word | yes | 2026-07-25 |
| Round-1 bounded assembly (4 sub-answers, 24 orders, 3 cases, length-filtered to 58) | 104,184 | certified oracle | 0 match | uncertified | 2026-07-25 |
| Round-2, 2 surviving length partitions (6 orders, 36 color names, 2 cases) | 46,688 | certified oracle | 0 match | uncertified | 2026-07-25 |
| "BLUE" literal readings (6 bounded runs: orders, spellings, cases, anagrams) | 3,266 | certified oracle | 0 match | uncertified | 2026-07-25 |
| Literal Hexagon / BalaenopteraMusculus / number-reordering partitions | 1,824 | certified oracle | 0 match | uncertified | 2026-07-25 |
| Piece 1 as RGB decimal or hex numbers instead of color words | 768 | certified oracle | 0 match | uncertified | 2026-07-25 |
| Colour names and hex flags x a16z / date / 18-char names, 4 piece orders | 47,343 | certified oracle | 0 match, superseded by the 24-order run | uncertified | 2026-08-17 |
| Same families plus colour initials and the 29-digit shape dump, all 24 piece orders | 368,283 | certified oracle | 0 match | uncertified | 2026-08-17 |
| Named-whale family: Blue as a standalone IQ answer; BlueWhaleCapital, BalaenopteraMusculus, HargreavesLansdown | 205,923 | certified oracle | 0 match | uncertified | 2026-08-17 |
| Printed letter order (IEANL, ILEAN, INEAL, AELIN) instead of the Alien anagram | 63,723 | certified oracle | 0 match | uncertified | 2026-08-17 |

Cumulative: 794,659 assembled 58-character candidates tested against the escrow, 0
matches. The 18-character whale length is an artefact of assuming piece 1 is 28
colour-name characters; that partition, and the hex partitions that replace it, missed.

## Open leads, ranked

1. **Re-read piece 1 as something other than colour names or hex** (hours). The
   58-character budget only forces piece 2 to 18 characters if piece 1 is the six colour
   names including Blue (28) and pieces 3 and 4 stay at 7 and 5. That partition, the hex
   partitions that go with it, and Blue as a standalone IQ-test answer paired with the
   short whale tokens already in the list, all missed. Solved siblings use a proper noun,
   a notation, or a count, not the literal drawn object, so a short IQ token such as
   `Blue` would force a long complementary whale string (42 characters with `2111011` and
   `Alien`) that the earlier list never contained. Confirmed by an oracle MATCH. Killed
   by a new piece-1 rule as tight as the hexagon digit rule that still produces no hit.
2. **Piece 2 is still a proper noun, but not the exhausted a16z / Blue Whale Capital
   list** (hours). The whale plus 16-03-2020 still points at the Forbes Arweave article
   of that date. What has been killed is the specific tokens `AndreessenHorowitz`,
   `a16z`, `16-03-2020`, `BlueWhaleCapital`, `BalaenopteraMusculus`, and
   `HargreavesLansdown` in every 24-order assembly with the piece-1 families above. A
   headline token, a concatenation of the three co-investors, or a string that only
   works once piece 1's length is revised, remains open. Confirmed by an oracle MATCH.
3. **Confirm piece 4 is Alien with an oracle hit** (hours). `Alien` is still the natural
   anagram of the five printed letters. Visual order (`IEANL` and three neighbours) was
   checked against the same piece-1 and piece-2 lists and also missed. Hatching-as-order
   was already refuted structurally.

## Files in this folder

| Path | What it is |
|---|---|
| `clues/puzzle-image.jpg` | the published jigsaw puzzle image, byte-exact |
| `analysis/tested.md` | the complete negatives ledger |
| `analysis/leads.md` | ranked open leads |
| `tools/oracle.py` | candidate checker: 58-character answer to JWK address, certified against the solved sibling #8 |
| `tools/search_whale.py` | bounded assembler: flag, whale, shape, and letter families through the certified oracle |

## Sources

- "Puzzle 12 is here", Twitter, 2020-05-05: https://twitter.com/arweavep/status/1257613928185675776
- Live puzzle page, Arweave permaweb, 2020-04-29: https://arweave.net/gymumAAsxGlzqPL5HzoEB8Xryu61o174j7vHwx21Qoo
- "58 chars CS", Twitter, 2020-05-23: https://twitter.com/arweavep/status/1264211142714499072
- "1,2,4,8 = solved / 3,5,7,9 = not solved yet", Twitter, 2020-04-14: https://twitter.com/arweavep/status/1250036746802298885
- HomelessPhD/AR_Puzzles community repository, PZL12 entry: https://github.com/HomelessPhD/AR_Puzzles/tree/main/PZL12
- Escrow wallet, viewblock.io: https://viewblock.io/arweave/address/XRGEfkMbCMHeTY9mZI9Lh6hf8EmA8RstmBFUjDm40fg
