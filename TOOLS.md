# Shop inventory

What's on hand, and what each tool needs in consumables. Kept here so blade and
bit sizes don't have to be re-derived in a store aisle.

**Open questions are marked ⚠️ — resolve these before ordering anything.**

## Power tools

| Tool | Model | Notes |
|---|---|---|
| **Plunge router** | Mastercraft 11A 2 HP combination plunge / fixed base, with case — [CT 0546821p](https://www.canadiantire.ca/en/pdp/mastercraft-11a-2-hp-corded-combination-plunge-fixed-base-router-with-case-0546821p.html) | **1/2" collet**, variable speed. Combo kit, so both plunge and fixed bases. 4-step turret, ~1" total. |
| **Mitre saw** | Genesis sliding compound, 10" — almost certainly **GMSDR1015LC** (confirm on the motor plate) | 15A, 4800 RPM. **10" blade, 5/8" arbor.** Crosscuts **12" at 90°**, so the 9-1/4" boards go through in one pass with room to spare. Ships with a 60T carbide blade. |
| **Circular saw** | Black & Decker, model unrecorded | Carbide-tipped blade fitted, **visibly rusted** — replace before use. |
| **Jigsaw** | Skil 4225, 3200 SPM | ⚠️ Older model; likely takes **U-shank** blades, not the modern T-shank. Verify before buying blades. |
| **Drill/driver** | DeWALT DCD771C2, 20V Max, 2-speed | 2 × 1.3Ah XR batteries, charger, bag. |

## Clamping

| | |
|---|---|
| 2 × F-clamps, 12" bar | ~13" actual opening |
| 2 × F-clamps, 7" | |
| 8 × ratchet straps | Standing in for long bar clamps — see below |

**Nothing spans the document unit's 26-1/4" width.** The eight straps cover it
(a strap loop delivers ~2× its tension), so no clamp purchase is needed for
that build. The wine rack is only 10-1/4" wide, so the 12" clamps already
handle it. The first thing that genuinely needs 36" capacity is the coffee
table's glued-up top.

## ⚠️ Before the build: shake down the shed tools

The mitre saw and circular saw sat in a shed for ~15 years, and the whole plan
now leans on the mitre saw. **Test it before buying materials, not after.**

**The slide rails matter more than the blade.** Rust or stiffness there makes
the head wander mid-cut, which no blade fixes. Clean them and use a *dry*
lubricant — oil holds sawdust and makes it worse.

**Check square in both axes.** A slider can be out at the fence and at the
bevel. The flip-and-butt test from the guide catches the fence: cut a piece,
flip one half, butt the cut edges — any error doubles.

**Check for play.** Rock the head side to side at the end of the slide. Any
slop shows up as a cut that isn't square through the thickness.

Also worth checking: cord condition, that the blade guard returns freely, and
that the motor runs without smell or grinding.

## ⚠️ Resolve before buying

**Jigsaw shank type.** U-shank and T-shank are not interchangeable, and a Skil
4225 is old enough to predate T-shank being standard. Look at the blade clamp.

## Consumables to buy

### Router bits

| Bit | Why |
|---|---|
| **1/2" straight, 2-flute carbide, 1/2" shank** | Does every joint in the document unit — 12 stile housings, 10 lap slots, 2 divider-end housings. All 3/4" wide, all off one jig setting. |

The 1/2" shank is the one to buy now that the collet is confirmed — noticeably
stiffer than 1/4" in the 4-5/8"-deep lap slots, where deflection would show up
as a bowed slot wall. Cutting length isn't critical with a base-riding jig:
there's no bearing, so none of the template-thickness geometry applies.

**Speed: run it flat out.** The variable speed exists for large-diameter bits,
where rim speed gets dangerous — anything under 1" wants full RPM. The rough
guide, worth keeping for later:

| Bit diameter | RPM |
|---|---|
| up to 1" | full (~22–24,000) |
| 1–2" | ~18,000 |
| 2–2-1/2" | ~16,000 |
| 3"+ | ~12,000 |

If pine starts to burn at full speed, the fix is a faster, steadier feed — not
a lower speed. Burning comes from dwelling in the cut.

**Not needed: a pattern bit.** It was the plan for a while, but a top-bearing
bit can't step depth (the whole depth range across passes has to fit inside the
bearing's height), which rules it out for the through-cuts. One straight bit and
one two-fence jig does everything instead.

### Saw blades

| Saw | Blade | Why |
|---|---|---|
| **Mitre saw** | 10", **60T ATB**, 5/8" arbor, **negative or low hook angle** | Cutting parts to final length. The saw shipped with a 60T carbide blade, but it's been in a shed ~15 years — the carbide won't have dulled, but the plate will have rusted. Not worth reviving a stock budget blade. |
| **Circular saw** | 7-1/4", **40T ATB**, 5/8" arbor | Ripping boards to one common width, and breaking down MDF. The fitted blade is visibly rusted. 40T rather than a 24T ripper because that ripped edge becomes the visible front edge of the case. |

Freud Diablo, Irwin Marples or CMT — all carried locally, all fine. Roughly
$40–50 for the 10" and $25 for the 7-1/4".

**Hook angle matters on a slider.** A blade with a high positive hook angle —
which is what a general-purpose or table-saw blade has — wants to self-feed,
and on a sliding saw that means the head grabs and lunges toward you mid-cut.
Buy a blade whose description says **sliding** or **compound mitre saw**; those
run a negative hook (around −5°). This is a safety spec, not a finish one, and
tooth count alone doesn't tell you.
| **Jigsaw** | Clean-cut wood blades — ⚠️ **check U- vs T-shank** | Only needed if roughing out lap-slot waste. Optional. |

### Sheet goods and shop stock

| | For |
|---|---|
| 1 × 3/4" MDF handy panel (2×4 ft) | Router jig rails + crossbar, mitre saw auxiliary fence, stop blocks |
| 1 × rigid foam board or scrap OSB | Sacrificial backer under the through-cuts |
| 1 × straight 2x4 | Two 22" cauls for the glue-up |

## Shop-made jigs

| Jig | Status | Notes |
|---|---|---|
| **Two-fence U-jig** | to build | Two rails + a crossbar. Gap dialled in by test cut; that one setting cuts all 24 joints. Screw it down once it's right. |
| **Rectangular router sub-base** | optional | Removes rotation as a variable, and stops the round base tipping when it overhangs on the end rabbets. |
| **Mitre saw auxiliary fence + stop block** | to build | Relieve the stop's bottom corner or sawdust packs in and parts creep longer through the day. |

## Notes to self

**Don't cut to the laser.** Budget-saw lasers drift out of alignment and are
only ever as accurate as their last calibration. Cut to the kerf the blade
makes in the auxiliary fence — that's a zero-clearance reference that can't lie
— and set length with the stop block, never by eye.

**Mark the router base and keep it facing one way.** The U-jig references
opposite sides of the base, so a base that isn't perfectly concentric puts that
error into the slot width. Consistency matters far more than centring — check
concentricity once by measuring shank-to-rim at four points.

**Keep clamp bars clean and dry.** If clutch-style clamps get bought: the
clutch grips by friction on the bar, so oiling it is exactly wrong. (Opposite
of pipe clamps, where waxing the pipe prevents black staining.)
