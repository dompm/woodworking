# Wine rack — cut list and build notes

Walnut, 12 bottles (2 wide × 6 high), 4" square openings.
Finished size **10-1/4" W × 9" D × 39-1/2" H** with 10" legs
(carcass 29-1/4 high, the legs raise it 10-1/4). The leg length sets the
height — see the table below.

All carcass parts are 3/4" thick and a full 9" wide — the boards are used at
full width, so there is no ripping at all. Every crosscut is 9" wide.

---

## Cut list

### Carcass — 3/4" walnut, 9" wide

| # | Part | Qty | Thickness × Width × Length |
|---|------|-----|----------------------------|
| A | Stile (side) | 2 | 3/4 × 9 × **29-1/4** |
| B | Horizontal (bottom rail, 5 shelves, top rail — all identical) | 7 | 3/4 × 9 × **9-1/4** |
| C | Divider — one continuous piece | 1 | 3/4 × 9 × **28-1/8** |

### Base

| # | Part | Qty | Size |
|---|------|-----|------|
| D | Angled leg top plate, 8° | 4 | steel, 2-3/8" square, hangar-bolt type |
| E | Leg | 4 | turned from 1-3/4 sq × 12" blank |
| F | Brass ferrule / foot cap | 4 | 7/8" ID |

### Material to buy

| | |
|---|---|
| 4/4 walnut, 9" wide, planed to 3/4" | **~18 linear feet** (12-1/2 ft net, ~13 bd ft with waste, plus 2 ft of offcut for test joints) |
| 8/4 walnut for legs | 4 blanks 1-3/4 sq × 12" (~3 bd ft) |
| Brass foot caps | 4, 7/8" ID |
| 8° angled leg plates + hangar bolts | 4 sets |
| #8 × 5/8" screws | 16, to fix the plates |

Part B is the same blank seven times, so cut all seven at one stop-block
setting. They are the parts that set the case width — if they differ, the case
racks.

---

## Joinery

### Stiles (A) — seven housings each

3/4" wide × **1/4" deep**, running through front to back, in the inner face.
Measured from the bottom end of the stile to the **lower edge** of each housing:

```
0        <- runs off the end, so this one is a rabbet
4-3/4
9-1/2
14-1/4
19
23-3/4
28-1/2   <- runs off the end, so this one is a rabbet
```

The two end ones are rabbets, not dadoes — same cut, just open at one end, so
you can saw them out completely instead of chiselling a trench. That is the
whole corner joint: the top and bottom rails sit in a 1/4" rabbet, the stiles
run past them full height, and the outside of the case shows two continuous
uninterrupted vertical lines.

Because the rabbet is 1/4" deep in 3/4" stock, **1/2" of each stile remains at
the top and bottom.** On the top and bottom faces of the finished case that
reads as a 1/2"-wide strip of stile end grain down each side, with the rail
between them. That is inherent to the joint, not a defect — see the note at the
end if you would rather not have it.

### The interior grid — half lapped egg crate

One continuous divider, half lapped into the five shelves where they cross.
At each crossing each member gives up **half its 9" width**: the shelf keeps
the front 4-1/2, the divider keeps the back 4-1/2. Every one of these is an
open-ended slot — two saw cuts and knock the waste out — not a trench.

| Cut | On | Where |
|-----|----|-------|
| Slot 3/4" wide × **4-1/2" deep**, in from the **back** edge, through the thickness | each of the 5 shelves | centred, **4-1/4" to 5"** from either end |
| Slot 3/4" wide × **4-1/2" deep**, in from the **front** edge, through the thickness | the divider | 5 of them, see spacing below |

Divider slot positions, from the bottom end of the 28-1/8" divider to the
**lower** edge of each slot:

```
4-3/16
8-15/16
13-11/16
18-7/16
23-3/16
```

Cut them a whisker fat — about 0.002" of fit clearance in the slot width —
so the parts go together without forcing.

### End rails (B) — divider housings

The two end rails still get a plain housing for the ends of the divider:
3/4" wide × **3/16" deep**, through, centred **4-1/4" to 5"** from either end.
Bottom rail top face only, top rail bottom face only. The five shelves get no
divider housings at all — the lap does that job.

### Legs (E) and plates (D) — buy these

Turning round tapered legs needs a lathe. Don't. Mid-century tapered legs with
brass ferrules and angled mounting plates are a stock item, roughly $12-20 each,
and are almost certainly what is in the reference photo. Buying them removes the
hardest operation in the build and guarantees that part looks right.

What to get: **10" tapered legs, ~1-1/2" dia at the top, with 8° angled top
plates and hangar bolts.** Check the plates are the *angled* kind — plenty of
sellers ship straight 0° plates by default.

**Buy the legs first, then set `LEG_LENGTH` in the model** and read the
resulting overall height off the console. The legs are the bought part, so they
drive the height, not the other way round:

| leg | overall height |
|---|---|
| 8" | 37-1/2" |
| **10"** | **39-1/2"** |
| 12" | 41-1/2" |
| 14" | 43-1/2" |

An 8° or a 10° plate changes the height by less than 1/10", so take whichever
you find. If the legs you get taper differently, set `LEG_TOP_D` and
`LEG_BOT_D` to match.

Trim the feet flat and parallel to the floor, not square to the leg — a splayed
leg with a square-cut foot stands on an edge.

The plates screw flat to the underside of the bottom rail with four #8 × 5/8"
screws, set in 3/8" from the front, back and side edges. Orient each plate so
its angle leans out toward the nearest corner, i.e. rotated 45° in plan.

The bottom rail is 3/4" stock and 5/8" screws do not leave much thread, so glue
a **3/4 × 1-1/2 walnut cleat** along the front and back edges of the bottom
cell floor, on the inside. That doubles the screw purchase to 1-1/4" and is
invisible from outside. A 3" bottle in a 4" cell still clears it.

---

## Notes

**Wood movement.** Every part's 9" dimension runs front-to-back, so the whole
case expands and contracts in the same direction at the same rate. There is no
cross-grain conflict anywhere and you can glue every joint solid.

**What is left to trench.** The egg crate removes most of the chisel work. All
that is still a true housing is the 14 shelf/rail dadoes in the stiles (two of
which are rabbets) and the two divider housings in the end rails. The 10 lap
slots are open-ended: knife the shoulders, two saw cuts, knock the waste out,
pare the bottom flat. For the dadoes that remain, knife the shoulders, saw both
walls to depth against a clamped guide block, chisel the waste, flatten with a
router plane. A trim router with a 3/4" straight bit and a shop-made T-square
jig would still be the biggest time saver if you own one.

**Mitre saw.** Use it for the 9"-wide crosscuts, with a stop block — the seven
B parts have to be identical. A 10" non-sliding saw will not cross 9"; you can
cut from both faces, or use a handsaw and shooting board.

**Bottle fit.** 4" square opening, 9" deep. A 3" bordeaux bottle has room to
spare, a 3-1/2" burgundy still fits. An 11-3/4" bottle projects about 3" past
the front, which is the look in the reference photo.

**Stability.** 39-1/2" tall on a 10-1/4 × 9 footprint, about 32 lb of wine when
full. With 10" legs at 8° the feet land just about under the corners of the case
(10 × 8-3/4 at the floor). 12" legs push them slightly wider. It is
still a tall narrow thing — worth an anchor to the wall if there are kids or
dogs around, and load the bottom rows first.

**Edges.** Ease everything with a block plane or a 1/16" roundover before
assembly, especially the front edges of the openings.

**If you want no end grain on the top face.** Set `END_JOINT = "rails_through"`
in the model: the top and bottom rails become full 10-1/4" boards, the stiles
shorten to 28-1/4", and the rabbets move from the stile ends to the rail ends.
The top becomes one uninterrupted board and the end grain moves to a 3/4" band
at the top and bottom of each side face instead. Same amount of work, different
place to look at end grain.

## Test joints — do these first

Two different risks, two different materials.

**Jig and layout risk** — is the router jig square, is it registering where you
think, is the cut list arithmetic right. Scrap pine or MDF is perfect for this
and costs nothing. Build the T-square jig, cut two dadoes in a pine offcut,
measure them.

**Fit and feel risk** — how tight is too tight, how the wood tears out, how the
router behaves. Pine cannot tell you any of this. It is soft and it crushes, so
a dado that is 0.01" too narrow will still take a pine shelf with a tap; the
same joint in walnut will split the stile or refuse to close. Pine also has a
brutal soft-earlywood / hard-latewood alternation that makes chisels dive, which
walnut simply does not do.

So dial the actual fits on **walnut offcuts**, which is what the extra 2 linear
feet in the materials list is for. Three test pieces:

1. **A through dado plus a shelf end.** Sneak the second router pass up until
   the offcut slides in with hand pressure and no mallet. This is the single
   most valuable half hour in the project — "3/4" planed stock is never exactly
   0.750", and this is where you find out what yours actually is.
2. **A rabbet at the end of a board.** Same setup, run off the end.
3. **One egg-crate lap crossing** — two short pieces, one slot each. It is the
   only joint here you have not done before, and it is worth meeting it once
   before you meet it ten times in the real stock.

If you do want a full-size practice carcass, **poplar beats pine** — it is
diffuse-porous, so it has none of pine's soft-earlywood / hard-latewood
alternation and it behaves predictably under a chisel. But it is only
marginally harder than pine (Janka 540 vs 380 for white pine, against 1010 for
walnut), so it still will not teach you fit tolerance. If you want a stand-in
that actually feels like walnut, use **soft maple** (950) or cherry (950).
Both are cheap and both machine like the real thing.

One thing that should be reassuring: walnut is genuinely pleasant to work. It
is dense enough to pare cleanly, it does not fuzz, and it routs without much
drama. Plenty of people find it easier than construction pine for exactly this
kind of joinery.

## Suggested order of work

1. Mill all stock to 3/4", crosscut A, B and C to length.
2. Cut the lap slots in the five shelves — gang all five, one setup.
3. Cut the five lap slots in the divider C, and the divider housing in each end
   rail.
4. Cut the seven housings in each stile A, including the two end rabbets.
5. Dry assemble the egg crate on the bench — divider plus five shelves — and
   check it is square before it ever meets the stiles.
6. Dry fit the whole carcass, then glue up: egg crate and rails into one stile,
   second stile on top.
7. Glue in the two screw cleats under the bottom cell.
8. Screw on the plates D.
9. Turn the legs E, fit the ferrules F, trim the feet flat to the floor.
10. Finish. Oil or a wiping varnish suits walnut and this style.
