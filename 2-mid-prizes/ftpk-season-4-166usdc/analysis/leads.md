# Open leads, ranked

## 1. Harvest the rest of the author's X posts (needs a person)

- **Cost**: needs a person
- **What it is**: @FTPKgame said extra hints are on X, and that every post since the
  Season 4 launch is a Season 4 clue. The public timeline shows a daily-ish hint cadence
  in mid-August 2026. The window from 2026-07-25 to 2026-08-15 is not readable without
  an X login. Those posts are the cheapest remaining source of constraints.
- **Why it ranks here**: the three posts that are readable already named pick-up sticks,
  the 52-card deck, and Roman numerals for game 11. Earlier posts in the gap likely name
  the other games the same way.
- **What would confirm it**: a complete 2026-07-16 to 2026-08-17 tweet list that assigns
  a reading rule to each remaining game, then a 12-word candidate that matches the escrow.
- **What would kill it**: a complete tweet list that adds no new reading rule, after the
  number-as-index and tag-as-rule leads below have also been run to completion.
- **Status**: open

## 2. Read each game as a number, then as a 1-based BIP39 index (hours)

- **Cost**: hours
- **What it is**: the author's own page names use `md5(N)` where N, read as a 1-based
  BIP39 index, spells the Season 2 hint page. That is this author's established index
  convention. The 2026-08-15 post says the number of cards in a deck is well chosen
  (52). The 2026-08-16 post says game 3 is pick-up sticks and that the author picked
  one point-value table. The 2026-08-17 post says game 11 is a Roman numeral. The
  season hint said the common element sometimes does nothing and sometimes is required:
  hangman and the game 10 phrases already read as words, while dice, darts, sticks,
  cards, and Roman numerals read as numbers.
- **Why it ranks here**: it is the only mechanic that is already proven on this site
  (the page names) and that the later X posts keep pointing at.
- **What would confirm it**: a single, consistent scoring or counting rule that returns
  12 values in 1 to 2048 whose 1-based words match the escrow under `m/44'/60'/0'/0/0`.
- **What would kill it**: every well-defined number extract from all 12 games, under
  both 1-based and 0-based indexing, failing the oracle. Vague thematic words do not
  kill it.
- **Status**: open

## 3. Treat the corner tags as reading rules, especially the shared `5:30` (hours)

- **Cost**: hours
- **What it is**: eight of the twelve games carry a bottom-left (and once bottom-right)
  tag. Games 2 and 9 both say `5:30`. That is too specific to be two copies of one seed
  word. The likely use is a shared reading direction or clock rule (half past five,
  down and slightly right, or "look at 5s and 3s"). `fall` on game 4, `Δ` on game 3,
  `where is` on game 7, and `male` on game 8 look like the same class of instruction.
  The 2026-07-25 hint said the common element is already visible and that it will not
  always help. Tags on a hangman or a motto page can be ignored; tags on a grid cannot.
- **Why it ranks here**: it is visible on the pages themselves and does not need the
  missing tweets, but it is less pinned than the number-as-index reading.
- **What would confirm it**: one tag rule that produces a BIP39 word on two or more
  tagged games, then a full 12-word match.
- **What would kill it**: a systematic pass over the tagged games under the obvious
  readings of each tag (down, difference, clock direction, winner location) with no
  consistent word set.
- **Status**: open

## 4. Game 11 as Roman numerals on the printed names or their dex numbers (hours)

- **Cost**: hours
- **What it is**: the page lists Blastoise, Gimmighoul, Gimmighoul / Pawmo, and
  Gimmighoul / Blastoise. The 2026-08-17 post says "Game 11, Roman numeral". National
  dex numbers 9, 999, and 922 write as IX, CMXCIX, and CMXXII. The English names also
  contain Roman letters (LI, IMMIL, M). The slashes may be pairings, or they may be
  division (999/9 = 111). One number in 1 to 2048, or one BIP39 word spelled only from
  Roman letters, should drop out.
- **Why it ranks here**: the author named the rule, but the page still has several
  legal encodings. It becomes cheap once the other eleven words are held to short lists.
- **What would confirm it**: a single encoding that the author named, producing one
  BIP39 word, in a 12-word phrase that matches the escrow.
- **What would kill it**: exhausting the dex-as-Roman, name-as-Roman, and generation-as-Roman
  encodings (I and IX) with no word that participates in a match.
- **Status**: open

Full ledger: [tested.md](tested.md). Page index: [games.md](games.md).
