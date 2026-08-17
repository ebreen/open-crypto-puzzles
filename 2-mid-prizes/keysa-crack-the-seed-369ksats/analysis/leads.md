# Open leads, full notes

Ranked summary is in the README. This file has the reasoning behind the ranking.

## 1. Write to the author

Keysa is active (her most recent Nostr event at the time of my last check was
2026-08-01) and has twice invited exactly this kind of contact in her own posts:
"I would love to know if this method is solid" and "Open to comments." Her stated
interest is in an audit of her method, not in protecting a secret. This is a near
zero cost action with the highest plausible payoff, since the selection rule is, by
her own description, short, memorable, and meant to be spoken aloud to a trusted
person, which is exactly the kind of fact that a mechanical sweep cannot recover but
a direct question can.

What would confirm it: a reply describing the selection rule, or enough of it to
narrow the remaining candidates to something `tools/oracle.py` can check directly.
What would kill it: no reply, or a reply that does not narrow anything (she has
stated before that she does not want to spoil the puzzle for others).
Cost: needs a person; no compute cost.

## 2. Submit argued candidate 12-word orderings (the "order, not selection" reading)

Under the original announcement, a reader frames the puzzle's difficulty in terms of
knowing the 12 words but not their order ("620 quintillion guesses even if they knew
the exact 24 words, but not the correct order"). Keysa's own reply engages with
counting permutations for a 12-word case rather than correcting the framing to
"you would first need to know which 12 words." Read together with her stated design
goal (a rule short enough to say out loud), this suggests her own mental model may
treat the selection as easier to work out than the order.

The practical consequence: for any well-argued candidate set of 12 tokens, checking
every one of its 12! = 479,001,600 orderings costs about 38 seconds on a rented GPU
(measured at about 0.79 million derivations per second), against 36.8 minutes on a
CPU for the one set already tried in full (L-001, `analysis/tested.md`). On a 4-core
CPU at about 930 PBKDF2 per second per core, one set is a little over two hours, so
I did not run a new 12! sweep here. The bottleneck for this lead is still producing
a well-reasoned candidate set of 12 tokens, not the derivation.

The best remaining set for this lead, if the 12 words are meant to be obvious from
the six typed rows, is still the first and last token of each row. Card order,
firsts-then-lasts, and lasts-then-firsts are all checksum-invalid (L-007). Every
6! times 2^6 grouping of those six pairs (any line order, any pair flip) is now
a negative too (L-010), so if this is the set, the order mixes across rows and
needs a full 12! on a GPU. I would put less weight on this set than I did
before L-010.

What would confirm it: any 12-token candidate set whose full 12! ordering sweep,
run through `tools/oracle.py --stdin`, returns a MATCH.
What would kill it: exhausting every argued candidate set without a match; this
lead does not have a natural end state the way a bounded space does, since new
candidate sets can always be proposed.
Cost: minutes per candidate set on a rented GPU; the cost driver is generating
candidates, not derivation.

## 3. The "two tokens per row" bounded sweep

The 6 rows are confirmed to be typed line breaks rather than a display artifact
(see the row-structure measurement in `analysis/tested.md`), which makes any rule
defined per row a legitimate candidate family. Speakable same-column picks of
exactly 2 tokens per row, including every pair of columns on all six rows in
card order and in 6! times 2^6 pair-grouped orders, are now negatives (L-009,
L-010). What remains of this lead is the independent-per-row case: pick exactly
2 of the tokens from each row, not necessarily the same columns, in some order.
The space is C(12,2)^4 times C(11,2)^2, about 5.7e10 raw combinations of token
pairs (rows of 12 tokens each contribute 66 ways to choose 2, rows of 11
contribute 55), narrowing to about 3.6e9 after the BIP39 checksum filter (1 in
16). At the measured rate of about 790,000 derivations per second on one GPU,
checking the checksum-valid subset costs about 76 minutes. That is no longer a
spoken cipher; it is a brute-force of "two per line, any two."

What would confirm it: a MATCH from `tools/oracle.py` on any candidate drawn from
this independent-per-row space.
What would kill it: running the full checksum-filtered space to completion with 0
matches, with a witness planted at the head, middle, and tail of the search order.
Cost: about 76 minutes on one rented GPU; same-column speakable orders are already
spent, so this is brute force of "any two per line."

## 4. The double-width gap after "mad", and the "369 clock" theme

Two weaker, unresolved observations. I now know more than when I ranked them, and I
would put less weight on both.

- The gap after the first token, `mad`, is still the only typographic anomaly on the
  card. Treating `mad` as a header and running the 69-token remainder through the
  same spoken rules as the full card is a negative (L-007). Using `mad` as a letter
  key (keep words whose first letter is in `{m,a,d}`) yields exactly 12 tokens, but
  that set is a bad fit for a one-shot BlueWallet seed, and the obvious orders are
  negative.
- The 2024 notes-app screenshot titles the card **369369 Sats Guessing Game**, so
  369369 is not just the prize amount; it is the name she gave the game. The most
  natural spoken readings of that name as a selector - take 3 skip 6 take 9, every
  3rd token starting at 3, two columns from `{3,6,9,12}`, cycling 3-6-9 two per row,
  3-6-9 of the four long rows, 3-6-9-12 of three-row windows, and the reward-epoch
  skip 6-3 from her own 369-clock chapter - are now negatives in card order
  (L-007, L-009, L-010). What remains of this lead is a 369-shaped rule I have
  not yet stated, not the ones above.

What would confirm either: a specific selection rule derived from one of these
observations that `tools/oracle.py` confirms.
What would kill either: this is not a bounded space to exhaust; both stay open until
a rule is proposed and tested, or until new information (most likely from lead 1)
explains them.
Cost: needs a new insight; the obvious 369 and drop-`mad` spoken rules are already
spent.
