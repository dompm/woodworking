# Build guide

Written for someone whose last project was a picture frame.
Tools assumed: **table saw, router, mitre saw, hand tools.**

There is an [illustrated version of this guide](https://claude.ai/code/artifact/a3f2afa2-34b5-4bcf-a35a-0f884b502578) with the jig drawings
and part layouts inline — easier to follow at the bench.

Read [CUTLIST.md](CUTLIST.md) alongside this — it has every dimension. This
document is the order to do things in and the technique for each step.

Numbers below assume `DEPTH = 9"`. If your boards come narrower, set `DEPTH` in
`lib/casework.scad` to what you actually got and re-read the cut list; only the
depth-related numbers change.

---

## Step 0 — Decisions to lock before you buy anything

Two things drive everything else, and both are outside your control, so settle
them first.

**The legs.** Buy them before you cut wood. You want 10" tapered legs with
brass ferrules and **8° angled mounting plates** plus hangar bolts. Check that
the plates are angled — many sellers ship flat 0° plates by default. A 10" leg
gives 39-1/2" overall. If you end up with 12" legs, the piece is 41-1/2" and
that's fine; just set `LEG_LENGTH` in the model so the drawings match what you
built.

**The board width.** Ask your hardwood dealer what they have surfaced, widest
first. Whatever number you get becomes `DEPTH`. Do not design around 9" and
then discover the yard only stocks 7-1/2".

**Shopping list**

| | |
|---|---|
| 4/4 walnut or cherry, ~18 linear feet at your chosen width, surfaced | the carcass, plus 2 ft for test joints |
| 10" tapered legs + 8° angled plates + hangar bolts | 4 sets |
| Brass ferrules | 4, if not included with the legs |
| #8 × 5/8" screws | 16 |
| Wood glue with long open time | Titebond Extend or liquid hide glue |
| Clamps | **6 × 18"** (12" is the true minimum: 10-1/4 case + 1-1/2 of cauls). Plus a few small ones for holding jigs |
| Sandpaper | 120, 180, 220 |
| Finish | hardwax oil or wiping varnish |
| Plywood scrap | for jigs |

**Safety, briefly and seriously.** Riving knife stays on the table saw; never
rip freehand without the fence; never stand directly behind the workpiece.
Route left-to-right when the bit is between you and the fence. And wear a
respirator — walnut dust is a genuine sensitiser, and you can develop a
reaction to it after months of being fine.

---

## Step 1 — Bring every board to one width

This is the single most important step and it's easy to underrate.

Every part in this design uses the **full width of the board**, and those edges
become the exposed front and back edges of the case. So all your stock must end
up at exactly the same width, with square edges.

1. Straight-line one edge of each board. With no jointer, screw or double-stick
   tape the board to a straight strip of plywood, run the plywood against the
   table saw fence, and the blade cuts a dead-straight edge.
2. Flip that new edge against the fence and rip every board to your chosen
   `DEPTH`, all at one fence setting. Do not move the fence between boards.
3. Check three boards with calipers. They must match.

If one board comes out 1/64" narrow, that shelf sits proud or shy of the front
of the case and you'll see it forever.

---

## Step 2 — Cut the parts to length

Use the mitre saw with a **stop block**, or a table saw crosscut sled. Never
measure each piece individually — set a stop and cut them all.

| Part | Qty | Length |
|---|---|---|
| A — stiles | 2 | 29-1/4" |
| B — horizontals | 7 | 9-1/4" |
| C — divider | 1 | 28-1/8" |

The seven B parts set the case width. If they differ from each other, the case
racks and no amount of clamping fixes it. One stop setting, seven cuts.

Label every part in pencil on a face that will be inside the case. Mark which
edge is the **front** on each one — it matters for the lap slots later.

Cut two extra 12" offcuts for test joints. Don't skip this.

---

## Step 3 — Measure your actual stock thickness

Put calipers on your "3/4 inch" boards. It will read something like 0.72" or
0.74". **Write that number down.** Every dado you cut has to match it, not the
nominal 3/4".

This is the number one reason first projects have sloppy joints.

---

## Step 4 — Build two jigs

**The T-square dado jig.** A strip of 1/2" plywood about 30" long with a
shorter piece screwed across one end at exactly 90°. Clamp it across a board
and run the router base against the long edge. On its first use the router
trims the crossbar, and from then on that trimmed edge sits exactly where the
bit cuts — so you align the jig directly to your layout line. No offset maths.

Use a **1/2" straight bit**, not a 3/4" one, and cut each housing in two passes.
There are two ways to control the width. Both work; the first is better for
fourteen housings.

### Option A — the exact-width jig (recommended)

Capture the router between **two** fences. Rout up one side, back down the
other, and the width is set by the gap — nothing to clamp or unclamp, and both
walls are referenced by the jig.

```
gap between fences = housing width + router base diameter − bit diameter
router's free travel = housing width − bit diameter
```

With a 6" base and a 1/2" bit on 3/4" stock, that's a 6-1/4" gap and 1/4" of
travel. Add a crossbar at 90° so it registers square to the edge, exactly like
the T-square.

**Setting the gap:** make one fence adjustable — slotted holes and two knobs.
Set it roughly, cut a test housing in scrap, try a shelf, nudge the fence, repeat.
Two or three tries. Then lock it and cut all fourteen with no further setup.

**The one gotcha:** you reference *opposite* sides of the router base, so if the
base isn't perfectly concentric with the bit, that error goes straight into the
width. **Mark the base and keep the mark facing the same way for every pass.**
Do that and the eccentricity stays constant, and your test-fit calibration
absorbs it.

### Option B — one fence and a spacer strip

Simpler to build, and immune to the concentricity problem because both passes
reference the *same* side of the base.

1. **Pass 1** — base riding the fence. This cuts the reference wall; it's final.
2. **Clamp a thin spacer strip to the face of the fence.**
3. **Pass 2** — base rides the spacer, widening the housing by exactly the
   spacer's thickness.

Final width = **bit diameter + spacer thickness**. You need about
`stock thickness − 1/2"`, but converge on it rather than measuring: cut a scrap
strip near 3/16", test, and add masking tape (~0.005") or a playing card
(~0.010") until a shelf slides in. Then tape the stack, label it, and use that
one object for all fourteen.

The spacer must be **thinner than the bit** or the passes won't overlap and
you'll leave a ridge. Do both passes at each jig position before moving the jig.

**You are not trying to hit 0.750".** You are matching your own stock. The target
is a feel — slides in with firm hand pressure, no mallet.

**The slot jig.** For the lap notches. Two parallel straightedges clamped
`(bit diameter)` apart won't be needed — just one straightedge plus a stop
block that halts the router at 4-1/2" of travel. Add a sacrificial backer board
underneath, because these cuts go all the way through the thickness.

---

## Step 5 — Test joints, in the real wood

Half an hour here saves the project. On your offcuts:

1. **A dado plus a shelf end.** Rout a dado at your intended depth (1/4"), then
   creep the second pass until an offcut slides in with hand pressure and no
   mallet. Too tight splits the stile during glue-up; too loose shows a gap.
2. **A rabbet at a board end.** Same setup, run off the end.
3. **One lap crossing** — two short pieces, one slot each. It's the only joint
   here you haven't done before.

Do not proceed until the first one fits properly. Write the final jig offset on
the jig in pencil.

---

## Step 6 — The seven dadoes in each stile

Positions, measured from the **bottom end** of the stile to the **lower edge**
of each dado:

```
0        <- runs off the end: this is a rabbet
4-3/4
9-1/2
14-1/4
19
23-3/4
28-1/2   <- runs off the end: this is a rabbet
```

Each is 3/4" wide (your real thickness) × **1/4" deep**, running all the way
through front to back.

**Rout both stiles at the same time.** Lay them side by side on the bench,
inner faces up, bottom ends flush against a common stop, and clamp them
together. Run each pass across both boards. Now the dadoes are at identical
heights by construction rather than by measurement, which is exactly the error
that makes shelves look crooked.

The two at the ends run off the board, so they're rabbets. You can rout them
like the others, or cut them on the table saw.

---

## Step 7 — Divider housings in the two end rails

Only the top and bottom rails get these — the five shelves do not, because the
lap does that job there.

3/4" wide × **3/16" deep**, through, centred **4-1/4" to 5"** from either end of
the 9-1/4" piece. Bottom rail on its top face only; top rail on its bottom face
only.

Shallower than the shelf dadoes on purpose. Set your router depth stop, cut
both, then put it back to 1/4" — or better, do all the 3/16" cuts in one
session so you only change the setting once.

---

## Step 8 — The lap slots

Ten cuts: one in each of the five shelves, five in the divider. All 3/4" wide ×
**4-1/2" deep**, cut in from an edge, all the way through the thickness.

This is where the front/back marking from Step 2 matters:

| Part | Slot cut in from | Position |
|---|---|---|
| The 5 shelves | the **back** edge | centred, 4-1/4" to 5" from either end |
| The divider | the **front** edge | 4-3/16, 8-15/16, 13-11/16, 18-7/16, 23-3/16 from the bottom end |

Get this backwards and the grid won't assemble.

**Technique.** Clamp the board flat over a sacrificial backer, clamp your
straightedge, and rout in from the edge in **three or four depth passes** —
don't try to hog 3/4" of walnut in one go. Stop at 4-1/2". Cut the slot a hair
fat (a few thousandths) so the parts go together without forcing; the joint is
located by the housings anyway.

You can't gang these — each slot sits at a different place on its own board — but
once the jig is set, each takes about three minutes.

*(A table saw can't do these: a 4-1/2" deep notch is beyond a 10" blade's reach,
and stopping a crosscut mid-board leaves the blade's arc cutting far past your
line on the underside.)*

---

## Step 9 — Dry fit, twice

**First, just the egg crate.** Stand the five shelves up in order, line the
divider up behind them with its notches on the shelves, and **push it forward
4-1/2" until everything is flush.** It goes together by hand and stands square
on its own.

The slide is the only motion that works. The two sets of slots open on opposite
edges — shelves from the back, divider from the front — so they can only engage
by travelling along the depth axis. The divider **cannot** drop in from above:
it is full depth everywhere except at its five notches, and a full-depth section
can't pass a shelf, because the shelf's slot only removes the back half.

Check the openings while it's dry. They should all be 4".

**Then the whole carcass.** Egg crate plus both end rails into one stile, then
the second stile on top. Everything dry, no glue.

Measure the diagonals of the front face. They must match. Fix problems now —
once glue is on 14 housings you have minutes, not hours.

---

## Step 10 — Glue up

Have everything within reach before you open the bottle: glue, brush, all
clamps pre-set to roughly the right opening, cauls, damp rag, square.

Do it in **two stages**. Trying to land fourteen housings and ten lap joints in
one go is the most stressful glue-up in the project, and it's avoidable.

**Stage one — the egg crate, on its own.**

1. Glue the ten lap faces lightly and slide the divider forward into the five
   shelves as you did dry.
2. Square it up, clamp lightly, and leave it to cure.

You now have one rigid grid instead of six loose parts, which makes stage two
enormously easier.

**Stage two — the carcass.**

3. Lay one stile on the bench, inner face up.
4. Glue and seat the two end rails and the cured egg crate into their housings.
   Thin glue in the housing, not on the shelf end — less squeeze-out to clean.
5. Glue the second stile and lower it onto all seven shelf ends at once.
6. Clamp across the width, one clamp per pair of shelves, with cauls to spread
   the pressure. Snug, not crushing.
7. Check the diagonals and rack it square before the glue grabs.
8. Wipe squeeze-out inside the cells with a damp rag now. Dried glue blocks
   finish and shows as pale patches.

Leave it overnight.

---

## Step 11 — The base

1. Glue a **3/4 × 1-1/2 cleat** along the front and back edges of the bottom
   cell floor, on the inside. The bottom rail is only 3/4" thick and 5/8"
   screws don't leave much thread; this doubles the purchase. It's invisible
   from outside and a bottle still clears it.
2. Screw the four plates to the underside, set in 3/8" from the edges, each
   rotated **45° in plan** so its angle leans out toward the nearest corner.
3. Screw in the legs.
4. Stand it on a flat floor. If it rocks, trim or sand the long foot **flat and
   parallel to the floor** — not square to the leg. A splayed leg with a
   square-cut foot stands on an edge.

---

## Step 12 — Finish

1. Sand 120 → 180 → 220. Break every sharp edge with 220 or a couple of block
   plane strokes — especially the front edges of the openings, which get
   touched constantly.
2. Vacuum, then wipe with a barely damp cloth and let it dry.
3. Hardwax oil (Osmo, Rubio) or a wiping varnish. Walnut and cherry both
   deepen dramatically with the first coat.
4. Two or three thin coats, scuffing lightly between. Thin coats, always.

Cherry will keep darkening for a year. That's normal and it's the good part.

---

## The five things most likely to go wrong

1. **Boards not all the same width.** Shelves sit proud or shy at the front.
   Fix in Step 1, not later.
2. **Dado width set to nominal 3/4" instead of your actual thickness.** Sloppy
   joints throughout. Step 3.
3. **Stiles routed separately.** Shelves end up at slightly different heights
   left to right and the whole grid looks off. Step 6 — clamp them together.
4. **Lap slots cut from the wrong edge.** The grid won't assemble. Step 8.
5. **Rushing the glue-up.** Use long-open-time glue and dry fit twice.

None of these are skill problems. They're all preventable with setup.

## Roughly how long

Not a weekend, realistically. Milling and cutting to size is an evening. Jigs
and test joints another. The joinery is the bulk — call it two solid sessions.
Glue-up is an hour plus overnight. Finishing is three short sessions spread
over several days.

Take the joinery slowly. Everything else is forgiving; that part isn't.
