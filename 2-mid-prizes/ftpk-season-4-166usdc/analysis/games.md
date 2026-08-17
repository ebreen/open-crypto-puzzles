# Season 4 game map

Live hub: `https://findtheprivatekeys4.vercel.app/home.html`.
Each game URL is `md5(N).html` for a decimal integer `N` at most 2200.
Those N values, read as 1-based BIP39 indices and concatenated in game order, name the
Season 2 hint page. They are not the Season 4 seed (see [tested.md](tested.md)).

Unauthenticated HTTP clients often receive HTTP 429 with `x-vercel-mitigated: challenge`.
A real browser session that has passed the checkpoint can load the pages below.

| Game | N | md5 filename | Page type | Corner tag |
|---|---|---|---|---|
| 1 | 1570 | `7949e456002b28988d38185bd30e77fd.html` | hangman, pattern `_ _ O _` | `dance` (bottom left), `1st` (bottom right) |
| 2 | 412 | `b9228e0962a78b84f3d5d92f4faa000b.html` | 5x5 dice | `5:30` |
| 3 | 796 | `35cf8659cfcb13224cbd47863a34fc58.html` | two rows of red / yellow / blue dots, minus, bar | `Δ` |
| 4 | 117 | `eb160de1de89d9058fcb0b968dbbbd68.html` | 8x8 letters | `fall` |
| 5 | 1744 | `418ef6127e44214882c61e372e866691.html` | darts notation `D12 T20 T17` | none |
| 6 | 968 | `8f468c873a32bb0619eaeb2050ba45d1.html` | 15x15 letters | none |
| 7 | 76 | `fbd7939d674997cdb4692d34de8633c4.html` | Texas Hold'em | `where is` |
| 8 | 552 | `94c7bb58efc3b337800875b5d382a072.html` | eight tic-tac-toe boards | `male` |
| 9 | 1388 | `0c0a7566915f4f24853fc4192689aa7e.html` | 11x11 letters and digits | `5:30` |
| 10 | 1377 | `f52378e14237225a6f6c7d802dc6abbd.html` | two short phrases | `again and again` (bottom left) |
| 11 | 505 | `e8c0653fea13f91bf3c48159f7c24f78.html` | four-line character list | none |
| 12 | 1508 | `ebd6d2f5d60ff9afaeda1a81fc53e2d0.html` | 15x15 Ludo-style cross | none |

Check page (paid yes/no, not required): `https://findtheprivatekeys4.vercel.app/check.html`.

Season 2 hint page (not the Season 4 order helper):
`https://findtheprivatekeys4.vercel.app/servicecricketgloomattendsupremejumpannualeagerpulpprojectdiseaseround.html`.

## Readings that are in the page source

Game 2 dice, row-major pip counts:

```
6 6 6 6 6
1 5 5 2 3
1 2 3 6 2
5 5 5 5 6
4 3 3 3 3
```

Game 5: `D12 T20 T17` sums to 135 if D means double and T means triple.

Game 7 hole cards and board, from the HTML (the 8 of hearts is an 8, not a 5):

```
6d 6h
9d 2d 2h 4h 8h
2c As
```

Game 10 center text is the Season 1 motto `simplicity must be rewarded`.
The bottom-left tag is `again and again`.

Game 11 list, exact lines:

```
Blastoise
Gimmighoul
Gimmighoul / Pawmo
Gimmighoul / Blastoise
```

Game 8: three of the eight boards have an X three-in-a-row; none have an O three-in-a-row.
The tag `male` is not a BIP39 word.

Game 12 colors in the page script: `#c0c0c0`, `#fffff0`, `#fff700`, `#f0e68c`
(silver, ivory, yellow, khaki). The playable cells form a 3-wide plus; the four 6x6
corners are empty. Game 6 is the same 15x15 size.
