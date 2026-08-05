# Sourcing brief — mid-century wine rack

Self-contained shopping spec. Everything needed to buy materials for one
12-bottle walnut wine rack, 10-1/4 W × 9 D × 39-1/2 H inches.

**Input needed before starting:** the buyer's city / region, so suppliers can be
local. Shipping 8-foot hardwood boards is expensive and often impractical —
prefer somewhere they can drive to.

**Deliverable:** for each numbered item below, 2–3 concrete options with
supplier name, product/page, price, and stock status. Flag anything that fails
an acceptance criterion rather than silently substituting.

---

## 1. Lumber — the critical item

**What:** black walnut, 4/4 (four-quarter, nominally 1" rough).
Acceptable alternate: cherry. Do not substitute poplar, pine, or any softwood.

**Milling:**

| Spec | Value | Hard requirement? |
|---|---|---|
| Thickness | Surfaced two sides (S2S) to **3/4"** | Yes. 0.72–0.75" acceptable, but must be *consistent across all boards* |
| Width | 8" or more. **Boards of similar width to each other** — avoid a mix of 8" and 11", since the wide ones get ripped down and the offcut is waste | Soft |
| Uniform width | Nice to have via the supplier, **not required** — the buyer can rip to a single width themselves | No |
| Final width | Set later to ~1/2" under the narrowest board received | n/a |
| Length | Leave long, **do not crosscut to length** | Yes — the buyer crosscuts with a stop block |

**Quantity:** 18 linear feet at the chosen width ≈ **13–14 board feet**.
Includes ~2 ft for test joints and ~20% for waste and defects. Round up.

**Why width consistency matters eventually:** every part uses the full board width,
and those edges become the visible front and back edges of the case, so all parts
must finish at the same width. The buyer has table saw access and can do that rip
themselves — so this is a preference when sourcing, not a requirement. Do not
reject a supplier over it.

**Do not upgrade to S4S or SLR.** The buyer is ripping both edges anyway; paying
for edge milling that gets cut away is wasted money. S2S to 3/4" is correct.

**Terminology to use with suppliers** — planing and ripping are *different
operations* and a planer cannot change width:

- **S2S** — both faces planed, edges untouched, widths random. **This is what to order.**
- **SLR1E / S3S** — S2S plus one straight-line-ripped reference edge.
- **S4S** — all four sides, but *at whatever width each board happens to be*
  unless a width is specified. **This is the trap — S4S alone does not mean uniform.**
- **"Rip to width"** — cutting to a specified width. A separate charge, and optional here.

**Script for the supplier:** *"Do you have 4/4 walnut, S2S to 3/4, in 8 inch or
wider boards — ideally of similar widths? I need about 18 linear feet. And do you
offer rip-to-width as an option?"* Keep the rip question clearly optional; framing
it as a condition of sale can get the whole enquiry declined by a terse supplier.

**Supplier types, in order of likelihood:**

1. Dedicated hardwood dealers serving woodworkers and cabinet shops. They have a
   millroom and this is routine for them. **Best bet.**
2. Commercial hardwood suppliers serving cabinet shops — definitely capable, but
   may have board-footage minimums that make a 14 bd ft order awkward.
3. Local cabinet or millwork shops — will often run a small job for cash.
4. Makerspaces / shared shops with a jointer and planer — the buyer mills it.

**Will not work:** big-box stores (fixed narrow pre-dimensioned stock, no custom
milling), sawmills selling rough only.

**Report back:** available species, the actual board widths in stock, price per
board foot, whether they rip to width and the up-charge, minimum order, turnaround.

---

## 2. Legs and mounting hardware

Buy — do not attempt to turn these. Requires a lathe.

| Spec | Value |
|---|---|
| Style | Mid-century tapered, round |
| Length | **10"** preferred (gives 39-1/2" overall). 12" acceptable (41-1/2") |
| Top diameter | ~1-1/2" |
| Foot diameter | ~7/8" |
| Ferrule | Brass foot cap, ~7/8" ID — included or bought separately |
| Mounting plate | **Angled, 8° or 10°.** Steel, ~2-3/8" square, with hangar bolt |
| Quantity | 4 legs, 4 plates, 4 hangar bolts, 4 ferrules |
| Material | Walnut preferred; beech or maple acceptable if stainable |

**Critical:** the plates must be **angled**, not flat. Many sellers ship 0° flat
plates by default and sell angled ones separately. An 8° and a 10° plate change
the finished height by less than 1/10" — either is fine, but note which, because
the CAD model has a parameter for it.

**Report back:** exact leg length, top and foot diameters, plate angle, whether
ferrules and bolts are included, price per set of 4.

---

## 3. Consumables

| Item | Spec | Qty |
|---|---|---|
| Wood glue | **Long open time** — Titebond II/III Extend, or liquid hide glue (Old Brown Glue, Titebond Liquid Hide). Standard Titebond II is too fast for a 14-joint glue-up | 8–16 oz |
| Screws | #8 × 5/8" wood screws, for the leg plates | 20 (16 + spares) |
| Sandpaper | 120, 180, 220 grit | a few sheets each |
| Finish | Hardwax oil (Osmo Polyx, Rubio Monocoat) **or** wiping varnish (Arm-R-Seal, Waterlox) | smallest can |

Confirm the screw length against the actual plate thickness once chosen.

---

## 4. Tooling

| Item | Spec | Notes |
|---|---|---|
| **Pattern bit** (top-bearing straight bit) | **1/2" diameter**, bearing OD **equal to** the cutter OD, cutting length ~1", shank to match the router collet | For the 14 housings. The equal bearing makes the cut reproduce the template one-to-one, so the jig can be set with a piece of the actual shelf stock — no measuring |
| Straight or spiral upcut bit | **1/2" diameter**, cutting length **≥ 1"** | For the 10 lap slots, which are through-cuts guided by a straightedge rather than a template. Not a 3/4" bit |
| Clamps | **6, opening to 18"** — F-style bar or quick-grip trigger | The glue-up clamps across the case width: 10-1/4 plus 1-1/2 of cauls = 11-3/4 needed, so 12" is the hard minimum and tight. Six puts one at nearly every housing. Beware: some "12-inch" clamps quote bar length, not jaw opening |
| Plywood scrap | 3/4" for the housing template, 1/2" for other jigs | Template thickness must roughly equal bit cutting length minus housing depth |
| Cauls | two straight strips, ~1 × 1-1/2 × 12" | Scrap. Spreads clamp pressure across all seven housings and stops the pads embossing the wood |

**Template stock:** 3/4" plywood or MDF for the housing jig. The thickness has to
roughly equal (bit cutting length − housing depth) so the bearing rides on the
template; 1/2" is too thin with a 1" cutter.

**Not needed:** dado stack. A table saw is used only to rip the boards to a single
width (the buyer has access to one) — all the joinery is router work.

---

## Acceptance criteria — flag, don't substitute

1. Any softwood substitution → wrong, report it.
2. Flat 0° leg plates instead of angled → wrong, report it.
3. Fast-setting glue only → report it; open time matters here.
4. Boards narrower than 8" → report the actual widths available; the design adapts,
   but the buyer needs to know before ordering.

**Not** a failure: a supplier who won't rip to width. That's optional.

## Nice to know

- Wide boards are the scarce thing, not the milling service. If 9" is hard,
  8" or even 7-1/2" is completely fine — the design adapts by changing one
  parameter.
- Fully-milled stock moves. Buy reasonably close to when it'll be worked, and
  don't have it milled to sit for a month.
- Rough budget sanity check: the lumber is the dominant cost, legs are second.
  Report actual prices; don't assume.
