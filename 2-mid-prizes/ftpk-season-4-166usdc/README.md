# FTPK Season 4: Something in Common (166.000000 USDC, [OPEN])

FTPKgame (@FTPKgame on X), the same author behind the Season 2 puzzle in this repository,
launched a fourth season on 2026-07-16: 12 mini-games, each one English BIP39 word, for
an Ethereum wallet holding USDC. I re-checked the escrow on 2026-08-17 (166 USDC, funded
and unspent), certified the BIP44 oracle, and mapped every game page on the live site.
The 12 page-naming integers are not the seed. Game 1 is not a unique hangman lock on
`frog`. Later author posts treat scores and Roman numerals as part of the common thread.
The 12 words are still unknown.

## At a glance

| | |
|---|---|
| Author | FTPKgame, [@FTPKgame on X](https://x.com/FTPKgame) |
| Published | 2026-07-16, X ([announcement](https://x.com/FTPKgame/status/2077755138668671313)) |
| Prize | 166.000000 USDC (about $166, stablecoin, 2026-08-16) |
| Chain | ethereum |
| Escrow | `0xa468335485cE853F21A44451755bd88364e9d618` ([explorer](https://etherscan.io/address/0xa468335485cE853F21A44451755bd88364e9d618)) |
| Last on-chain check | 2026-08-17: USDC balance 166.000000, native ETH 0.00053941261264344 (gas preload for the winner), 0 outgoing transactions ever |
| Status | OPEN |
| Puzzle type | bip39-seed, word-selection |
| Target format | 12 English BIP39 words, BIP44 `m/44'/60'/0'/0/0`, no passphrase |
| Certified oracle | yes: `tools/oracle.py --selftest` (certified against the public BIP39/BIP44 test mnemonic; no author-published worked example exists for this season) |
| What remains | solve the 12 mini-games under the common number-or-tag rule; 0 words confirmed via the oracle |
| Series | FTPK (this folder covers Season 4 only) |

## The puzzle as published

The site (`findtheprivatekeys4.vercel.app`) lists 12 games. The hub page for the series
describes this season as simpler than Season 2 and "built around finding a common thread
running through the season." The launch post calls the season "Something in common."
On 2026-07-23 the author confirmed,
["all the words are necessarily part of the BIP-39 list"](https://x.com/FTPKgame/status/2080258068529492034).
On 2026-07-25:
["Here is the first clue for Season 4. I've actually already given it : There is something
that almost all the games have in common. Sometimes it won't really help you, but at other
times, you will absolutely need to keep that common element in mind."](https://x.com/FTPKgame/status/2080976765401387082)
On 2026-07-22:
["In Season 4, there is a hidden page to help you with Season 2. This page is hidden in a
way that's a bit similar to Game 12 from Season 2."](https://x.com/FTPKgame/status/2079947035357102350)
On 2026-08-15:
["the number of cards in a deck is really well chosen"](https://x.com/FTPKgame/status/2088605776470286613).
On 2026-08-16:
["Regarding the game of Pick-up sticks... everyone just makes up their own rules for the
point values. I had to pick one"](https://x.com/FTPKgame/status/2088962735245574568).
On 2026-08-17:
["Game 11, Roman numeral"](https://x.com/FTPKgame/status/2089331422410535207),
and a clarification that
[every clue posted since the Season 4 launch is a Season 4 clue](https://x.com/FTPKgame/status/2089348233541632343).
The home page says the 12 answer words, concatenated with no spaces, name a page that
confirms order. A separate `check.html` page offers a paid $1 yes/no check by email or X
and states that it is not required.

## What is understood

### Mechanism

Twelve mini-games each resolve to one BIP39 word. The 12 words, in game order, form a
standard mnemonic; its BIP44 Ethereum address at `m/44'/60'/0'/0/0` must equal the escrow
exactly. The homepage concat URL is a second, free check of that same 12-word string.
The paid checker is optional. The escrow is the offline oracle.

### Derivation and oracle

```
python3 tools/oracle.py --selftest                              # public BIP39/BIP44 vector
python3 tools/oracle.py "twelve english words in a guessed order"
python3 tools/oracle.py --stdin                                  # one candidate per line
```

`MATCH <address>` on a hit, `NO MATCH` otherwise; a candidate with an invalid BIP39
checksum is reported as a checksum failure rather than derived.

### Certified against

`tools/oracle.py --selftest` reproduces the standard public BIP39 test mnemonic, 12
repetitions of "abandon" followed by "about", deriving to
`0x9858EfFD232B4033E47d90003D41EC34EcaEda94` under `m/44'/60'/0'/0/0`. No worked example
specific to this season has been published by the author, unlike Season 2's Game 11.

### Established facts

1. The escrow holds 166.000000 USDC and a 0.00053941261264344 ETH gas preload, with 0
   outgoing transactions ever, checked via `eth_call` to the USDC contract and
   `eth_getTransactionCount` on 2026-08-17. The launch post said 150 USDC. A 2026-08-16
   author post advertised $167. The on-chain USDC balance that day and the next was 166.
2. The author confirmed all 12 words are drawn from the standard BIP39 English wordlist.
3. Each game page is `md5(N).html` for a decimal integer `N` at most 2200. The 12 values
   of N, read as 1-based BIP39 indices and concatenated in game order, name the live
   Season 2 hint page. That page's own text says it is useless for Season 4. The same
   12 words, used as a mnemonic, have a valid BIP39 checksum and do not derive the
   escrow (certified oracle, 2026-08-17).
4. The homepage concat rule applies to the 12 *answer* words, not to those page-N words.
   The two URLs are different pages.
5. Eight of the twelve games carry a corner tag. Games 2 and 9 both use `5:30`. Game 10
   quotes the Season 1 motto "simplicity must be rewarded" in the center and tags
   "again and again" at the bottom left. Game 3 is the pick-up-sticks page named on X.
   Game 7 is the card page. Game 11 is the four-line list the author later called a
   Roman numeral. The per-page map is in [analysis/games.md](analysis/games.md).
6. Unauthenticated fetches of `findtheprivatekeys4.vercel.app` often receive HTTP 429
   with a Vercel challenge. The hub at `findtheprivatekeys.vercel.app` and the finished
   Season 1 site do not.

## What has been tested

Full ledger in [analysis/tested.md](analysis/tested.md). Summary:

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Page-naming integer N as that game's BIP39 index | 1 candidate per game, checked against game 1's `??o?` pattern | compare index N to the BIP39 word at that position | refuted as a per-game answer index | uncertified | 2026-07-26 |
| The 12 page-N 1-based words, in game order, as the seed | 1 mnemonic | certified oracle under `m/44'/60'/0'/0/0` | checksum valid, 0 match | yes: selftest vector immediately before the check | 2026-08-17 |
| 13th hidden page search (N up to 2200, thematic words, N up to 36,000) | approximately 34,000 URLs | HTTP probe, 200/404 signature | refuted: no extra page beyond the Season 2 hint page | uncertified | 2026-07-26 |
| Letter grids (games 4, 6, 9) as plain word searches | full BIP39 wordlist and a 75,145-word English dictionary, all 8 directions, length 4 or more | grid search | refuted as a classic word search: 2 incidental matches in game 4, 0 in games 6 and 9 | uncertified | 2026-07-26 |
| Game 6 letters under the game 12 color mask, row-major and tip-to-center | 4 color groups plus 12 arms | read the masked strings against BIP39, length 4 or more | 0 usable hit | uncertified | 2026-08-17 |
| Hidden links in the page markup | full site mirror | grep for anchors and `data-*` attributes | refuted: none found | yes | 2026-07-26 |

## Open leads, ranked

1. **Harvest the rest of the author's X posts** (needs a person). Posts since 2026-07-16
   are Season 4 clues. The public timeline is missing 2026-07-25 to 2026-08-15, which is
   where the remaining per-game hints likely sit. Confirmed by a complete tweet list that
   names a reading rule for each unsolved game, then a 12-word match. Killed only after
   that list is in hand and the two leads below have also been run out.
2. **Read each game as a number, then as a 1-based BIP39 index** (hours). The page names
   already use that convention. The later X posts point at 52, pick-up-stick scores, and
   Roman numerals. Hangman and the game 10 phrases can stay words; the scored games
   become indices. Confirmed by 12 in-range numbers whose 1-based words match the
   escrow. Killed by exhausting every well-defined extract under both index bases.
3. **Treat the corner tags as reading rules** (hours), especially the shared `5:30` on
   games 2 and 9. Confirmed by one tag rule that yields BIP39 words on two or more
   tagged games and then a full match. Killed by a systematic pass over the obvious
   readings of each tag with no consistent set.
4. **Game 11 as Roman numerals** (hours) on the printed names or their dex numbers 9,
   999, and 922. Confirmed by one encoding the author named, in a matching 12-word
   phrase. Killed by exhausting dex-as-Roman, name-as-Roman, and generation-as-Roman.

Full notes: [analysis/leads.md](analysis/leads.md).

## Files in this folder

| Path | What it is |
|---|---|
| `analysis/tested.md` | the complete negatives ledger |
| `analysis/leads.md` | full notes behind the ranked leads |
| `analysis/games.md` | per-game URLs, page-N values, tags, and short source readings |
| `tools/oracle.py` | candidate checker: 12-word mnemonic to Ethereum address, certified against a public BIP39/BIP44 test vector |

## Sources

- "A new treasure hunt is live! (Something in common), 12 hidden words, 150 USDC to be won", X, 2026-07-16: https://x.com/FTPKgame/status/2077755138668671313
- "In Season 4, there is a hidden page to help you with Season 2", X, 2026-07-22: https://x.com/FTPKgame/status/2079947035357102350
- "Yes, all the words are necessarily part of the BIP-39 list", X, 2026-07-23: https://x.com/FTPKgame/status/2080258068529492034
- "There is something that almost all the games have in common", X, 2026-07-25: https://x.com/FTPKgame/status/2080976765401387082
- "the number of cards in a deck is really well chosen", X, 2026-08-15: https://x.com/FTPKgame/status/2088605776470286613
- "Regarding the game of Pick-up sticks... I had to pick one", X, 2026-08-16: https://x.com/FTPKgame/status/2088962735245574568
- "Up for a bit of a challenge... aim to win $167", X, 2026-08-16: https://x.com/FTPKgame/status/2088966091330445313
- "Game 11, Roman numeral", X, 2026-08-17: https://x.com/FTPKgame/status/2089331422410535207
- "All the clues posted since the launch of Season 4 relate only to Season 4", X, 2026-08-17: https://x.com/FTPKgame/status/2089348233541632343
- FTPK hub page: https://findtheprivatekeys.vercel.app/
- Season 4 puzzle site: https://findtheprivatekeys4.vercel.app/
- Season 2 hint page hosted on the Season 4 site: https://findtheprivatekeys4.vercel.app/servicecricketgloomattendsupremejumpannualeagerpulpprojectdiseaseround.html
- Escrow wallet, etherscan.io: https://etherscan.io/address/0xa468335485cE853F21A44451755bd88364e9d618
