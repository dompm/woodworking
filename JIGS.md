# Jig plan — two 3/4" MDF panels

Everything the document unit needs, cut from **2 × (24" × 48") handy panels**.

The order below matters: the aux fence comes off first because it's the only
piece needing a full 48", and the saw guide gets built before anything else
because every later cut depends on it.

---

## Cutting layout

### Panel 1 — the guide and the fences

```
   ┌────────────────────────────────────────────────┐ 24"
   │  aux fence            4 × 48                   │
   ├────────────────────────────────────────────────┤
   │                                                │
   │  GUIDE BASE          11 × 36        │  spare   │
   │                                     │  20 × 12 │
   ├─────────────────────────────────────┤          │
   │  guide fence          3 × 36        │  crossbar│
   ├─────────────────────────────────────┤  stops   │
   │  rip fence            3 × 30        │  spacers │
   ├─────────────────────────────────────┤          │
   │  U-jig rails    2 × (3 × 14)        │          │
   └─────────────────────────────────────┴──────────┘
                        48"
```

### Panel 2 — the station

```
   ┌──────────────────────────────┬─────────────────┐ 24"
   │                              │  station rails  │
   │   STATION BASE               │  2 × (3 × 24)   │
   │      24 × 34                 │                 │
   │                              │  spare 24 × 14  │
   └──────────────────────────────┴─────────────────┘
                    48"
```

---

## 1. The saw guide — build this first

**Base 11 × 36, fence 3 × 36.**

The awkward part is the bootstrap: you need a straightedge to cut a
straightedge. You don't — **the edge you'll guide against is the panel's
factory edge, the one you aren't cutting.** So the cut that frees these pieces
can be freehand, or against the saw's rip fence riding a factory edge. Only the
*fence* piece needs a good edge, and it gets one for free.

1. Free the aux fence strip and the guide pieces, roughly.
2. Glue and screw the fence to the base, **factory edge outward**, set in far
   enough that the blade will land inside the base on both sides — about 5"
   from one edge and 1-1/2" from the other, since your blade sits off-centre in
   the shoe.
3. **Run the saw down both sides.** Now both edges of the base are cut lines —
   one for each hand, which matters whenever the offcut is on the side you'd
   naturally stand.

From here on: **align the base's edge to your mark, clamp, cut.** No offset to
measure, ever.

---

## 2. The cutting station

**Base 24 × 34. Two rails 3 × 24, screwed on with a 28" gap between them.**

The gap has to clear the *longest* dimension being cut across, and the two
operations want different things:

| | cut runs across | gap needed |
|---|---|---|
| Crosscut to length | the 11" width | > 11" |
| Rip to width | the 26" length | > 26" |

Hence 28". The guide bridges the rails, boards slide underneath, and the guide
never gets re-clamped — which is the whole point.

**Cut the rails from pine, not MDF.** Then they're exactly the workpiece
thickness, so the guide sits on rails and workpiece equally, and its own kerf
becomes a zero-clearance slot pressed against the top face — which is where a
circular saw tears out.

**Screw a stop block to each rail** that the guide butts against. Clamping it by
eye each time moves the cut line, and repeatability was the reason to build
this.

### Using it — ripping to width

Clamp a fence (the 3 × 30 piece) parallel to the guide, **11" from the cut
line**, set with two spacer sticks. Boards slide in against it. One setup for
every board, no per-board gauging.

### Using it — crosscutting to length

Board's already-squared end butts a stop; the guide's edge is the cut line.
A straight stop touching a square end at two points forces the board
perpendicular, so no edge fence is needed.

**One wart: for the 25-1/4" horizontals the stop lands about 1-1/4" off the
base**, because a 24"-wide panel can't give you 26" in that direction. Clamp it
to the bench instead. The 22" stiles and 20-7/8" divider sit on the base fine.

**Relieve the stop's bottom corner** — chamfer 1/8" off. Sawdust packs into the
inside corner otherwise and every board comes out a fraction longer than the
last.

---

## 3. The U-jig (housings and lap slots)

Two rails **3 × 14** plus a crossbar. The crossbar comes from **pine**, not MDF:
the rails bridge from the workpiece onto it, so it has to match the board's
thickness, and cutting it from the same stock guarantees that with no measuring.

Gap between rails = `slot width + base Ø − bit Ø` ≈ **6-1/4"** with a 6" base
and a 1/2" bit — but **don't calculate it, dial it in.** Clamp one rail, set the
other by test cut, creep outward a paper's thickness at a time until a real
offcut slides in snugly, then screw it down. That one setting cuts all 24
joints.

Build order: crossbar and rail A first, square. Calibrate rail B by test cut.
Fix rail B last.

---

## Build order for the day

```
   1. saw guide                      everything downstream needs it
   2. rough-crosscut all parts +1"   circular saw, sloppy
   3. station + U-jig                while the boards settle
   4. rip to width                   station, fence, spacers
   5. crosscut to length             station, stop
   6. housings and laps              U-jig
```

Step 3 is deliberate: boards release internal stress the moment they're cut,
and most of that movement shows up within hours. Building jigs is exactly the
right thing to do in that window — you need the time anyway, so the settling
comes free.
