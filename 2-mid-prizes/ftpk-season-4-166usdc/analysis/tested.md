# Negatives ledger, FTPK Season 4

Dated 2026-07-26 unless noted otherwise.

## Page-naming scheme

Every game page is named `md5(N).html` for a decimal integer `N`; probing roughly 34,000
URLs (every N from 0 to 2200, a set of thematic word hashes, and a wider sweep up to
36,000) found exactly the 12 known game pages plus 1 further page, the Season 2 hint
page. No other hidden page exists in this range.

The Season 2 hint page is named by concatenating the 12 page-N values as 1-based BIP39
words, in game order, with no spaces. Recomputing `md5(str(N))` for
1570, 412, 796, 117, 1744, 968, 76, 552, 1388, 1377, 505, 1508 reproduces the 12
homepage links. The concatenated filename is live and its own text says the page is
useless for Season 4 and only maps Season 2 X hints to Season 2 game numbers.

1 candidate tested, 0 match. Method: treat those 12 1-based words, in game order, as
the Season 4 mnemonic and run `tools/oracle.py` under `m/44'/60'/0'/0/0`. Result:
checksum valid, derived address is not the escrow. Witness: `tools/oracle.py --selftest`
reproduces the public BIP39/BIP44 vector immediately before the check. Rate: one
derivation. Date: 2026-08-17.

The same 12 words under 0-based indexing (N itself as the wordlist offset) are a
checksum-invalid mnemonic and are reported as NO MATCH without derivation. Date:
2026-08-17.

Testing whether N itself is a direct index into the BIP39 wordlist *for that game's
answer*: game 1's hangman pattern is `??o?`. Game 1's page-naming integer is 1570, which
indexes to "service" (1-based) or "session" (0-based); neither word fits `??o?`.
Refuted as a per-game answer index. The 2026-07-26 write-up also treated `frog` as
fixed by the hangman plus the tags `1st` and `dance`. That lock is not valid: if `dance`
is a set of excluded letters, several BIP39 words still fit `??o?`, and the
alphabetically first survivor is not `frog`. `frog` remains one hangman-shaped
candidate, not an established word.

## Grid puzzles

Games 4 (8x8, corner tag "fall"), 6 (15x15), and 9 (11x11, corner tag "5:30") were
searched in all 8 directions, length 4 or more, against both the full BIP39 wordlist and
a 75,145-word English dictionary. Game 4 returned 2 incidental matches ("time" and
"evans"), neither fitting any established pattern; games 6 and 9 returned 0 matches.
Refuted as classic word-search puzzles.

A 2026-08-17 re-run against the BIP39 list only, including length 3, still finds no
length-4-or-more hit in game 6, one incidental `fox` in game 9, and the same `time` /
`van` / `age` hits in game 4. Uncertified as a full-dictionary re-run; the BIP39-only
pass matches the earlier game 4/6/9 conclusion.

Game 12 (a Ludo-style cross with colored squares) and game 6 are both 15x15, which looked
intentional; overlaying the Ludo board's colored-square mask onto the letter grid in
row-major order produces unreadable sequences (for example the silver squares read
`AVEXRO`, the khaki squares `PVMIJT`). Reading each of the 12 arm-columns and arm-rows
from tip to center, and the four color groups in script order, also produces no BIP39
word of length 4 or more except the incidental `off` / `ask` / `fat` already sitting on
the plus. Refuted for row-major color groups and for tip-to-center arm reads. Other
path orders (a full clockwise Ludo circuit, rotations, reflections) were not exhausted.

Game 3 (a subtraction problem rendered in colored dots): reading the full dot pattern as
a base-3 number under each of 6 color-to-digit assignments, then subtracting as the
puzzle's layout implies, produces 10 or 11-digit results under every assignment, none in
the 1 to 2048 range a BIP39 index would need. Refuted as stated; the puzzle's structure
is confirmed, its encoding is not yet solved. The 2026-08-16 author post names this
game as pick-up sticks and says the point table was a choice. Color-count scoring under
several published Mikado / jonchet tables yields small differences (for example 9, 17,
19, 30) that sit in range; those have not been locked as answers and have not been
run as a 12-word phrase.

## Oracle self-test

`tools/oracle.py --selftest` reproduces the public BIP39/BIP44 test mnemonic (12
repetitions of "abandon" followed by "about") deriving to
`0x9858EfFD232B4033E47d90003D41EC34EcaEda94`, and separately confirms the checksum filter
accepts that vector and rejects a corrupted variant of it. Measured on one CPU core: 956
mnemonic derivations per second, and 1.5 million BIP39 checksum checks per second with a
6.23 percent pass rate, matching the 1-in-16 rate BIP39's checksum design predicts.

None of the grid and page-naming checks above carries a planted witness proving a search
would find a real answer if one were in scope, since most of the 12 words are not yet
established; each row's witness reflects only whether that specific check's own method
was validated (a positive control), not whether the full derivation oracle has been
exercised on a real solution. The 2026-08-17 page-N mnemonic check is the exception:
it uses the certified oracle on one fully specified 12-word phrase.
