// =============================================================
//  Shop jigs for the wine rack build, drawn so they can be seen
//  rather than imagined.
//
//    openscad -D 'mode="none"' -D 'JIG="dado"'      jigs.scad
//    openscad -D 'mode="none"' -D 'JIG="dado_pair"' jigs.scad
//    openscad -D 'mode="none"' -D 'JIG="slot"'      jigs.scad
//
//  Everything sits on a bench at z = 0 and is in inches, like the model.
// =============================================================

include <wine_rack.scad>

JIG = "dado";

PLY      = 0.50;   // jig stock
BAR      = 0.75;   // crossbar, thick enough to hook the board edge
FENCE_W  = 3.50;
BASE_D   = 6.00;   // router base plate
BASE_T   = 0.375;
BIT_D    = 0.50;
BENCH    = 40;

// Two-pass housing: pass 1 rides the fence, pass 2 rides a spacer clamped to
// the fence face.  Final width = bit diameter + spacer thickness, so nothing
// has to be measured and the reference wall never moves.
SPACER   = 0.25;   // T - BIT_D

PLYWOOD  = "#c9a97a";
PLYWOOD2 = "#b08f5f";
ROUTER   = "#41454b";
KNOB     = "#232629";
STEEL    = "#9aa0a6";
STOP     = "#8c2f39";
BENCHTOP = "#8d8375";

// ---------------------------------------------------------------
//  a plunge router, simplified to what matters: the base rides the
//  fence, the bit sits dead centre
// ---------------------------------------------------------------
// Ghosted on purpose: a real router base covers the cut it is making, so a
// solid one would hide the very thing these drawings exist to show.
module router(cut_depth = DADO, ghost = 0.38) {
    color([0.25, 0.27, 0.29, ghost]) {
        translate([0, 0, T]) cylinder(h = BASE_T, d = BASE_D);
        translate([0, 0, T + BASE_T]) cylinder(h = 2.4, d = 3.4);
    }
    color([0.13, 0.15, 0.16, ghost]) for (a = [-1, 1])
        translate([a * 2.1, 0, T + BASE_T + 1.7]) cylinder(h = 0.9, d = 1.4);
    color(STEEL) translate([0, 0, T - cut_depth])
        cylinder(h = 1.2 + cut_depth, d = BIT_D);
}

// drop lets the bench sit under a sacrificial board without the two tops
// landing on the same plane and z-fighting
module bench(drop = 0) {
    color(BENCHTOP) translate([-8, -10, -1.2 - drop]) cube([BENCH, 26, 1.2]);
}

// a G-clamp, just enough to read as "clamp it here"
module clamp(len = 4) {
    color("#5a6068") {
        translate([-0.6, 0, 0]) cube([1.2, 0.9, len], center = false);
        translate([-0.6, 0, len]) cube([3.2, 0.9, 0.7]);
        translate([-0.6, 0, -0.7]) cube([3.2, 0.9, 0.7]);
    }
}

// ---------------------------------------------------------------
//  T-square dado jig
//  The long fence lies on top of the work; the crossbar hooks over
//  the near edge, which is what makes the cut square without
//  measuring an angle.
// ---------------------------------------------------------------
module tsquare(board_len, board_wid, fence_x, spacer = false) {
    // fence: runs across the board, router rides its left face
    color(PLYWOOD) translate([fence_x, -1, T])
        cube([FENCE_W, board_wid + 3, PLY]);
    // crossbar: hooks the near edge, sets the fence square
    color(PLYWOOD2) translate([fence_x - 5, -BAR - 0.0, 0])
        cube([FENCE_W + 5, BAR, T]);
    // pass 2 only: the spacer strip clamped to the face of the fence
    if (spacer)
        color(STOP) translate([fence_x - SPACER, -1, T])
            cube([SPACER, board_wid + 3, PLY + 0.02]);
}

module work_dado(board_len, board_wid, dado_x, dado_w = T) {
    // colour has to sit OUTSIDE render(): a render() subtree is evaluated by
    // CGAL and discards colours set within it
    color(WALNUT) render() difference() {
        cube([board_len, board_wid, T]);
        // the housing being cut
        translate([dado_x, -EPS, T - DADO])
            cube([dado_w, board_wid + 2*EPS, DADO + EPS]);
    }
}

BL = 16; BWID = DEPTH; BDX = 9.0; BRY = DEPTH - 2.5;

module bearing_assembly() {
    work_dado(BL, BWID, BDX, T);
    // the template opening IS the housing width -- set it with a shelf offcut
    color(PLYWOOD) translate([BDX - 3, -1.5, T + 0.06]) cube([3, BWID + 3, TPL]);
    color(PLYWOOD) translate([BDX + T, -1.5, T + 0.06]) cube([3, BWID + 3, TPL]);
    color(PLYWOOD2) translate([BDX - 3, -BAR, 0]) cube([6 + T, BAR, T]);
    translate([BDX + BIT_D/2, BRY, 0]) router_pattern();
}

// ---------------------------------------------------------------
//  Exact-width ("U") dado jig.  The router is captured between two fences and
//  the housing width is set by the gap, so both walls are referenced by the jig
//  and there is nothing to clamp or unclamp between passes.
//
//      gap            = width + baseD - bitD
//      router travel  = width - bitD          <- the whole trick
//
//  Rout up one side, back down the other, done.
// ---------------------------------------------------------------
GAP = T + BASE_D - BIT_D;

// Pattern-bit version.  A top-bearing bit has bearing diameter == cutter
// diameter, so the cut reproduces the template one-to-one and the offset is
// ZERO: the gap in the jig simply IS the housing width.  Which means the jig
// can be set with a piece of the actual shelf stock -- no arithmetic, no base
// diameter, nothing to measure.
TPL      = 0.75;   // template must be thick enough for the bearing to ride on
BEAR_H   = 0.28;

module router_pattern(cut_depth = DADO) {
    // body sits ON TOP of the template, not down beside it
    color(ROUTER) {
        translate([0, 0, T + TPL]) cylinder(h = BASE_T, d = BASE_D);
        translate([0, 0, T + TPL + BASE_T]) cylinder(h = 2.4, d = 3.4);
    }
    color(KNOB) for (a = [-1, 1])
        translate([a * 2.1, 0, T + TPL + BASE_T + 1.7]) cylinder(h = 0.9, d = 1.4);
    // shank, deliberately a different diameter -- it is not what guides anything
    color(STEEL) translate([0, 0, T + TPL - BEAR_H])
        cylinder(h = BEAR_H + 1.2, d = 0.44);
    // the bearing: SAME diameter as the cutter.  This is the whole trick.
    color(STOP) translate([0, 0, T + TPL - BEAR_H - 0.02])
        cylinder(h = BEAR_H, d = BIT_D);
    // cutter, reaching down through the template into the work
    color(STEEL) translate([0, 0, T - cut_depth])
        cylinder(h = TPL - BEAR_H + cut_depth, d = BIT_D);
}

module ujig(board_wid, f1) {
    // Lifted clear of the workpiece.  0.01 was not enough -- at render scale
    // that is a sub-pixel gap and it still z-fights; the subtrahend's bottom
    // face has to clear the workpiece top too, not just the plate.
    z0 = T + 0.06;
    color(PLYWOOD) difference() {
        translate([f1 - 2, -1.5, z0]) cube([GAP + 4, board_wid + 3, PLY]);
        translate([f1, -1.5 - EPS, z0 - 0.02])
            cube([GAP, board_wid + 3 + 2*EPS, PLY + 0.04]);
    }
    // crossbar hooks the near edge, same as the T-square
    color(PLYWOOD2) translate([f1 - 3.5, -BAR, 0]) cube([GAP + 7, BAR, T]);
}

// ---------------------------------------------------------------
//  slot jig: straightedge plus a stop that ends the cut at 4-1/2"
// ---------------------------------------------------------------
module work_slot(len, wid, slot_x, depth) {
    color(WALNUT) render() difference() {
        cube([len, wid, T]);
        translate([slot_x, wid - depth, -EPS])
            cube([T, depth + EPS, T + 2*EPS]);
    }
}


// ---------------------------------------------------------------
//  Table saw scenes.  Only what reads: a table, a fence, and a blade
//  standing proud of the surface.
// ---------------------------------------------------------------
TABLE   = "#8a8d91";
FENCE_C = "#5f646a";

module saw_table(x0, x1, y0, y1) {
    color(TABLE) translate([x0, y0, -1.1]) cube([x1 - x0, y1 - y0, 1.1]);
}

// blade standing in the plane y = ypos, cutting along x
module blade_along_x(xc, ypos, dia = 10, proj = 1.6) {
    color(STEEL) translate([xc, ypos, proj - dia/2])
        rotate([90, 0, 0]) cylinder(h = 0.11, d = dia, center = true, $fn = 64);
}

// blade standing in the plane x = xpos, cutting across y
module blade_along_y(xpos, yc, dia = 10, proj = 1.6) {
    color(STEEL) translate([xpos, yc, proj - dia/2])
        rotate([90, 0, 90]) cylinder(h = 0.11, d = dia, center = true, $fn = 64);
}

// a board with one wavy edge -- the reason straight-line ripping exists
module rough_board(len, wid, thick, wave = 0.42) {
    pts = [for (i = [0 : 12])
             [len * i / 12, wave * (sin(i * 74) + 0.7 * sin(i * 131)) ]];
    linear_extrude(height = thick)
        polygon(concat(pts, [[len, wid], [0, wid]]));
}

// =============================================================
scale(UNIT) {
if (JIG == "dado" || JIG == "dado_pass2") {
    L = 16; WID = DEPTH; DX = 9.0;
    // reference wall (the fence side of the housing) sits at DX + T
    FX  = DX + T - BIT_D/2 + BASE_D/2;
    two = (JIG == "dado_pass2");
    bench();
    // pass 1 leaves a bit-wide groove; pass 2 widens it away from the fence
    work_dado(L, WID, two ? DX : DX + T - BIT_D, two ? T : BIT_D);
    tsquare(L, WID, FX, two);
    translate([FX - BASE_D/2 - (two ? SPACER : 0), WID - 2.0, 0]) router();

} else if (JIG == "dado_pair") {
    // both stiles at once: dadoes land at identical heights by
    // construction instead of by measurement
    L = 16; WID = DEPTH; DX = 9.0; GAP = 0.02;
    bench();
    work_dado(L, WID, DX);
    translate([0, WID + GAP, 0]) work_dado(L, WID, DX);
    color("#3f3a34") translate([-1.4, -0.6, 0]) cube([1.4, 2*WID + 2, T]); // end stop
    tsquare(L, 2*WID + GAP, DX + T/2 + BASE_D/2);
    translate([DX + T/2, 2*WID - 3.0, 0]) router();

} else if (JIG == "ujig") {
    L = 16; WID = DEPTH; DX = 9.0;
    F1 = DX - BASE_D/2 + BIT_D/2;      // puts the left wall of the housing at DX
    bench();
    work_dado(L, WID, DX, T);
    ujig(WID, F1);
    // shown against the left fence; the free play to the right fence is
    // exactly T - BIT_D, and that play is the housing's width beyond the bit
    // solid here, not ghosted: in this jig the base sits down inside the slot at
    // the same height as the plate, and a transparent one dithers against it
    translate([F1 + BASE_D/2, WID - 2.5, 0]) router(DADO, 1);

} else if (JIG == "ujig_bearing" || JIG == "ujig_bearing_section") {
    if (JIG == "ujig_bearing_section") {
        // sectioned through the bit axis: the bearing and the cutter are the
        // point of this drawing and they are invisible from outside
        difference() {
            bearing_assembly();
            translate([-50, BRY - 100, -50]) cube([100, 100, 100]);
        }
    } else {
        bench();
        bearing_assembly();
    }

} else if (JIG == "ripsled") {
    // One edge is straight because the SLED is straight; the blade then makes
    // the second edge parallel to it.  Nothing references the rough edge.
    FY = 7.0;                      // fence face
    saw_table(-8, 34, -12, 12);
    color(FENCE_C) translate([-8, FY, 0]) cube([42, 1.6, 3.0]);
    color(PLYWOOD) translate([1, -1.5, 0]) cube([26, FY + 1.5, PLY]);
    color(WALNUT) translate([1, -1.2, PLY]) rough_board(26, 6.0, T);
    blade_along_x(14, 0, 10, T + PLY + 0.9);
    color(STOP) for (x = [5, 20]) translate([x, 2.0, PLY + T])
        cube([1.6, 1.6, 0.5]);     // screws or double-stick tape

} else if (JIG == "stopblock") {
    // The stop is what makes seven identical parts.  Measuring each one is how
    // you get seven nearly-identical parts.
    // shelf length, derived -- HORIZ_LEN is not a variable in the model,
    // the horizontal extents are functions of the row index
    L = hx1(1) - hx0(1);           // the part length being cut
    saw_table(-L - 8, 14, -13, 6);
    color(FENCE_C) translate([-L - 8, 0, 0]) cube([L + 22, 1.6, 2.6]);
    // the part: between the stop and the blade
    color(WALNUT) translate([-L, -DEPTH, 0]) cube([L, DEPTH, T]);
    // the rest of the board, still to be cut, on the far side of the blade
    color(WALNUT) translate([0.09, -DEPTH, 0]) cube([12, DEPTH, T]);
    // stop block projects FROM the fence face, so the board end butts it
    color(STOP) translate([-L - 1.6, -2.4, 0]) cube([1.6, 2.4, 2.4]);
    blade_along_y(0, -DEPTH/2, 10, T + 1.1);

} else if (JIG == "slot") {
    L = 9.25; WID = DEPTH; SX = 4.25; CUT = 2.5;   // caught mid-cut
    bench(PLY);
    color(PLYWOOD2) translate([-1.5, -1.5, -PLY]) cube([L + 3, WID + 3, PLY]); // backer
    work_slot(L, WID, SX, CUT);
    // straightedge the base runs against
    color(PLYWOOD) translate([SX + T/2 + BASE_D/2, -1.5, T])
        cube([FENCE_W, WID + 3, PLY]);
    // stop block: ends the cut at 4-1/2" of slot
    color(STOP) translate([SX + T/2 - BASE_D/2 - 1.2, WID - 4.5 - BASE_D/2 - 1.2, T])
        cube([BASE_D + 2.4, 1.2, PLY + 0.35]);
    translate([SX + T/2, WID - CUT, 0]) router();
}
}

echo(str("jig = ", JIG));
