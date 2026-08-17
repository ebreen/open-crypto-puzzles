# Mechanism, in full

## The site

The puzzle lives on an approximately 70-page Wix site, almost all of it password-protected
page by page. The entry page (`/treasure-hunt`) carries an image whose EXIF metadata encodes
GPS coordinates; entering the latitude and then the longitude as consecutive page passwords
opens a compass page, which displays four branch passwords in clear text: `north64`,
`south64`, `east64`, and `west64`. From there the site forks into four branches.

Everything up to and including the branch fork is solved: I hold every password from the
entry page through the compass page and through every page each branch passes before its
final locked gate, plus the North land chain described below.

The three remaining insight riddles are printed on the open page immediately before each
lock, not on the locked page itself. West: riddle on `g5jpk` (`/west`), lock is `wt1jy`
(`/message`). East: riddle on `pxsqo` (`/weallliveinayellowsubmarine`), lock is `c2ozw`
(`/take-a-big-breath`, titled resurface). South: riddle on `wdnv9` (`/name5`), lock is
`b3vye` (`/havingfunwiththeurl-ilovedthisshowasakid-sosomuch`, titled Name 6).

## The four branches

North is a long narrative that I had marked empty too early. Password `glimmer` opens
`mwfaz` (`/whale-message`). The page prints four tokens in numbered order, hunt / gather /
whale / blood, and a derived page password `huntgathwhalblo` (first four letters of each
token concatenated). That password opens `thmoi` (`/land-ho`), which prints two further
passwords in clear text: `michaelphelps` (swim to shore, `eqyel`) and `seahitchhiker`
(hitch a ride, `chtro`).

The hitch path is a death ending: `nantucketsleighride.png` plus the instruction "Password
is 2 words, but omit the first" yields `sleighride` on `d3zak`, which sends the reader to
Hell with password `666`. The swim path opens `vbk6p` (`/cape-cod`) with `vampire`; that
page is a "Coming Soon... Sep 9, 2022" stub about arriving in a past America with no Apollo
missions. Three of the bottle tokens (`hunt`, `gather`, `blood`) are BIP39 English words;
`whale` is not. I do not treat the four tokens as recovered seed words. They have not opened
West, East, or South.

West, East, and South each still end in one password-gated page I have not opened. I call
these the three insight locks. Opening any of them requires guessing a short, unenumerable
string that answers the riddle text quoted in [clues/author-posts.md](../clues/author-posts.md).

West's lock sits on `g5jpk` before the pirate merge. East and West later share one spine:
`east64` -> bird (`xrd91`) -> pirates (`e3zre`, password `albatross`) -> semaphore
(`hhb0r`) -> litter (`sm18u`, password `youshallpass47`) -> night / iceberg / yellow
submarine -> East lock. The sibling pirate button "I choose to fight" goes to still-closed
`y6cd1`.

The South name chain is Gilligan, Jonas (the Skipper's given name), Thurston, Lovey, Ginger,
then locked Name 6. Spaced `Mary Ann` does not open Name 6. It does open the tropical-island
page `jetkc`, so the island chain is a separate gate, not a Name 6 alias.

## Case sensitivity and format, established by direct test

Passwords on this site are case sensitive. I confirmed this on already-open gates: `Gilligan`
succeeds where `gilligan` and `GILLIGAN` both fail, and `west64` succeeds where `West64`
fails. Combined with the passwords already known for every other open gate, the format of
the three remaining locks is:

- South (`b3vye`): Title Case, matching the naming pattern of the five prior South pages.
  Spaced `Mary Ann` is accepted on `jetkc` and rejected on `b3vye`, so Name 6 is not that
  string.
- West (`wt1jy`) and East (`c2ozw`): lowercase, a single token with no spaces (matches every
  other open West/East page password, e.g. `albatross`, `semaphore`, `20000leagues`,
  `glimmer`, `sleighride`, `vampire`).

No password anywhere on the site I have opened carries a numeric suffix that is not directly
derivable from the page's own content (a number visible in an image on that same page, or a
password printed in clear text on the previous page); no guess should add an arbitrary digit
string.

## The 12-word carrier channels

The site's predecessor, "Born to Be Wild" (2021, Apollo/moon theme), was solved and swept by
an unidentified third party; I used its known solution purely as a template for how this
author hides seed words, not as part of the live puzzle. Its seed was
`fortune all man kind one giant step into digital tomorrow virtual moon` with passphrase
`supernova`, assembled from 7 carrier channels. Mapping the same 7 channels onto this hunt:

| # | words | Hunt #1 channel | Hunt #2 equivalent | status here |
|---|---|---|---|---|
| 1 | word 1 | bytes appended after the cover image's EOF marker | Glimmer cover art | refuted: every Hunt #2 cover image I found (Bandcamp, Apple Music, Deezer, ToneDen, and the site's own PNG) is clean; a collage image that looked like a second Hunt #2 cover turned out to be a Hunt #1 teaser predating this hunt |
| 2-4 | words 2-4 | museum gold frames pictured in the book/site | not located outside a gated page | not found on any open page |
| 5-7 | words 5-7 | a forced cultural quotation naming a BIP39 word | pop-culture reference on the East branch | behind the locked `c2ozw` gate |
| 8-9 | words 8-9 | Morse code in an alternate audio mix | West branch "computer" theme or a hypothetical alternate mix | refuted for the public master: the only public 48kHz/24-bit Glimmer audio matches its own official master with no Morse signal; no alternate mix has been found distributed anywhere |
| 10 | word 10 | binary encoding | not located | the only binary string found anywhere on the site is an EXIF comment reading "nope lol", which does not decode to anything |
| 11-12 | words 11-12 | a "future song" ticket prop | inherited endgame page, already open | present, but this is Hunt #1's own endgame carried over, already read, and not new information |
| passphrase | "in the song" | the closing track's title | the Glimmer track title or lyric | not testable without the 12 words |

The practical conclusion: every carrier channel that is reachable without solving one of the
three insight locks has been checked and is either empty (refuted), inherited scaffolding
from Hunt #1, or North-branch story text whose four printed tokens are not a BIP39-valid
set. All 12 words still sit behind West, East, and South.
