// =============================================================
//  Desk footrest -- solid ramp on splayed sides
//
//  A brace, not a platform.  The chair and the desk both adjust, so height is
//  already solved; the job is to give the feet something to push forward
//  against, so the legs stop extending and shoving the hips toward the front
//  of the seat.  The slope does that -- about a third of the push comes back
//  horizontally, into the chair.
//
//  Solid top rather than slats: slats read as pallet, and a solid top can be
//  sized to come off ONE board with no glue-up, which matters because there is
//  no clamp in the shop that spans it.
//
//  Everything is in inches; scale(UNIT) at the bottom emits millimetres.
//
//      openscad footrest.scad
//      openscad -D 'mode="exploded"' footrest.scad
// =============================================================
UNIT = 25.4;

mode = "assembled";   // assembled | exploded | side | parts | none

// ---------------- stock
T = 0.75;

// ---------------- the ramp
// 20 degrees is about the ceiling before the ankle starts to complain, so this
// sits just under it.  D_TOP is chosen so the top comes out of a 1x12.
D_TOP   = 11.00;      // top board, front to back ALONG the ramp
W_TOP   = 17.00;      // top board, side to side
H_FRONT =  2.75;      // top SURFACE height at the near edge
H_BACK  =  6.25;      // at the far edge

// ---------------- sides
INSET = 1.25;         // how far each side is set in from the end of the top
FRONT_SET = 1.25;     // and set back from the front edge, so the top overhangs
SPLAY = 0.75;         // how much wider the sides are at the floor than up top

// ---------------- felt strip
// Where the feet actually land.  Three jobs at once: stops a smooth ramp being
// slippery in socks, is warmer underfoot than bare wood, and puts a line of
// colour into an object that is otherwise one flat brown plane.
FELT_W    = 13.00;
FELT_D    =  4.00;    // along the ramp
FELT_FROM =  3.25;    // from the front edge, along the ramp
FELT_REC  =  0.09375; // 3/32 recess, so the felt sits flush and not proud

// ---------------- derived
RISE  = H_BACK - H_FRONT;
ANG   = asin(RISE / D_TOP);      // ramp angle -- rise over the ramp LENGTH
D     = D_TOP * cos(ANG);        // horizontal footprint
UNDER = T / cos(ANG);            // top's thickness, measured vertically

EPS = 0.01;

WALNUT  = "#5b3a24";
WALNUT2 = "#66422c";
FELT    = "#2b3a55";

// =============================================================
//  parts
// =============================================================

// Put children in the ramp frame: origin at the top's front edge, x running up
// the ramp, z normal to it (0 = top surface, negative = into the board).
module in_ramp() {
    translate([0, 0, H_FRONT]) rotate([0, -ANG, 0]) children();
}

module felt_solid(extra = 0) {
    in_ramp()
        translate([FELT_FROM, (W_TOP - FELT_W)/2, -FELT_REC - extra])
            cube([FELT_D, FELT_W, FELT_REC + extra + EPS]);
}

module top_board() {
    difference() {
        in_ramp() translate([0, 0, -T]) cube([D_TOP, W_TOP, T]);
        felt_solid(EPS);
    }
}

module felt() {
    in_ramp()
        translate([FELT_FROM, (W_TOP - FELT_W)/2, -FELT_REC])
            cube([FELT_D, FELT_W, FELT_REC]);
}

// Side profile, in x (front to back) and z (up).  A splayed trapezoid: wider
// at the floor than where it meets the top, so the piece stands on a base
// visibly broader than its waist.  Straight lines only, no boolean -- nothing
// here can go non-manifold.
module side_profile() {
    z_front = H_FRONT - UNDER;
    z_back  = H_BACK  - UNDER;
    zf = z_front + FRONT_SET * (z_back - z_front) / D;   // ramp height at the setback
    polygon([[FRONT_SET, 0],
             [D, 0],
             [D - SPLAY,           z_back],
             [FRONT_SET + SPLAY,   zf]]);
}

// j = 0 near side, 1 far side
module side(j) {
    y = (j == 0) ? INSET : W_TOP - INSET - T;
    translate([0, y + T, 0])
        rotate([90, 0, 0])
            linear_extrude(T)
                side_profile();
}

// =============================================================
//  assembly
// =============================================================
module footrest(explode = 0) {
    translate([0, 0, explode * 2.4]) color(WALNUT) top_board();
    translate([0, 0, explode * 2.4]) color(FELT)   felt();
    for (j = [0, 1])
        translate([0, (j == 0 ? -explode : explode), 0])
            color(WALNUT2) side(j);
}

scale(UNIT) {
    if (mode == "assembled") {
        footrest(0);
    } else if (mode == "exploded") {
        footrest(1.6);
    } else if (mode == "side") {
        color(WALNUT2) side(0);
    } else if (mode == "parts") {
        // every unique part laid flat, for checking the cut list
        color(WALNUT) cube([D_TOP, W_TOP, T]);
        for (j = [0, 1])
            translate([0, W_TOP + 1.5 + j*(H_BACK + 1.5), 0])
                rotate([90, 0, 0]) translate([0, 0, -T])
                    linear_extrude(T) side_profile();
    }
}

echo(str("top board            = ", W_TOP, " x ", D_TOP, " x ", T,
         "   (one board, no glue-up)"));
echo(str("ramp angle           = ", ANG, " deg"));
echo(str("footprint depth      = ", D));
echo(str("height front -> back = ", H_FRONT, " -> ", H_BACK));
echo(str("side, floor -> top   = ", D, " -> ", D - 2*SPLAY));
echo(str("side height, f -> b  = ",
         H_FRONT - UNDER + FRONT_SET*(H_BACK-H_FRONT)/D, " -> ", H_BACK - UNDER));
echo(str("sides set in         = ", INSET, " each end; top overhangs"));
echo(str("felt strip           = ", FELT_W, " x ", FELT_D,
         ", recessed ", FELT_REC));
