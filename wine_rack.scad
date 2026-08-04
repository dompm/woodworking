// =============================================================
//  Mid-century wine rack  -  12 bottle, 2 x 6
//  Walnut, 4/4 stock planed to 3/4", 9" wide boards
//  Shelves housed into the stiles, interior grid half lapped (egg crate)
//  Legs: 4 splayed round tapered legs on angled plates, brass ferrules
//
//  ALL DESIGN MATH IS IN INCHES.  The finished model is scaled by UNIT
//  on output, so the scene OpenSCAD actually draws is in millimetres --
//  a 40" object is only 40 units tall, which lands inside OpenSCAD's
//  near clip plane and makes the mouse feel absurdly sensitive.
// =============================================================

UNIT = 25.4;   // 25.4 -> emit millimetres (recommended).  1 -> emit inches.

// ---------------- what to draw ----------------
mode         = "assembled";  // assembled | exploded | carcass | joint | parts
show_bottles = true;
show_legs    = true;

// ---------------- corner joint ----------------
// The five shelves are always housed into the stiles.  This picks who wins
// at the very top and bottom, which decides where end grain shows:
//
//  "stiles_through"  stiles run the full height, the end rails land in a
//                    1/4" rabbet.  All seven horizontals are one blank.
//                    Shows a 1/2" strip of stile end grain down each side
//                    of the top and bottom faces.
//  "rails_through"   the top and bottom rails run the full width and the
//                    stiles are housed into them.  Top and bottom faces are
//                    one uninterrupted board; the end grain moves to a 3/4"
//                    band at the top and bottom of each side face.
END_JOINT = "stiles_through";

// ---------------- interior grid ----------------
//  "housed"    dividers are separate 4-3/8" blocks, housed 3/16" into the
//              face of the shelf above and the shelf below.  22 trenched
//              housings in total.
//  "eggcrate"  one continuous divider, half lapped into the shelves where
//              they cross.  Each member loses half its 9" width at the
//              crossing: the shelf keeps the front 4-1/2, the divider keeps
//              the back 4-1/2.  Every one of those cuts is an open-ended
//              slot, not a trench.
GRID = "eggcrate";

// ---------------- stock ----------------
T      = 0.75;   // planed thickness of every carcass part
DEPTH  = 9.00;   // full width of the 9" boards -> carcass depth

DADO     = 0.25;    // shelf / rail into stile, 1/3 of stock
// dividers are housed into both faces of the same shelf, so keep these
// shallower: 2 x 3/16 leaves 3/8" of shelf between them instead of 1/4"
DADO_DIV = 0.1875;

// ---------------- grid ----------------
OPENING = 4.00;  // clear opening, square
COLS    = 2;
ROWS    = 6;

// ---------------- legs ----------------
// The legs are the bought part, so they are an INPUT and the overall height
// falls out of them -- not the other way round.  Set LEG_LENGTH to a size you
// can actually order and read the resulting height off the console.
LEG_LENGTH = 10;      // nominal length of the bought leg, along the leg

// Total lean off plumb, in degrees.  This is how angled leg plates are sold:
// a single 8 or 10 degree tilt, with the plate turned 45 degrees in plan so
// the leg leans out toward the corner.  It is NOT 8 degrees on each axis --
// that would be 11.3 degrees total and no stock plate does it.
LEG_TILT_SPEC = 8;

LEG_TOP_D   = 1.50;
LEG_BOT_D   = 0.90;
FERRULE_H   = 1.25;
FERRULE_OS  = 0.02;   // brass proud of the wood

// How the legs attach.  The bottom rail is 3/4" stock, so a 1" tenon bored at
// the compound angle would break straight through it -- there is no such thing
// as boring the legs into the bottom board directly.
//  "plate"  angled steel top plate, 2-3/8" square and 1/8" thick, screwed flat
//           to the underside.  The plate carries the 8 degrees, so the leg gets
//           an ordinary square shoulder off the lathe and no compound cut.
//           Nothing chunky under the case; the leg springs off the board.
//  "block"  laminated walnut block, 2-1/4" square and 1-1/2" deep, bored at the
//           compound angle for a 1" round tenon.  All wood, no hardware, but it
//           reads as four lumps under the case.
LEG_MOUNT   = "plate";

// ---------------- leg style ----------------
//  "round"   turned, splayed, brass ferrules -- the mid-century look. Bought.
//  "square"  square section tapered on its two INNER faces, no splay, held by
//            glue blocks instead of hardware -- the scandinavian look, and you
//            can make these yourself with a table saw and a hand plane.
LEG_STYLE = "round";

SQ_TOP   = 1.50;    // square leg, across the flats at the top
SQ_BOT   = 0.875;   // at the foot
SQ_INSET = 0.125;   // reveal between the leg's outer faces and the case sides
GB_XY    = 1.00;    // glue blocks in the inner corner
GB_H     = 1.25;

PLATE_XY    = 2.375;  // steel plate footprint
PLATE_T     = 0.125;  // plate thickness
PLATE_BOSS  = 0.20;   // mean thickness of the angled seat on top of the plate

BLOCK_XY    = 2.25;
BLOCK_H     = 1.50;

MOUNT_INSET = 0.375;  // set in from the carcass edges so it sits in shadow

// ---------------- derived ----------------
W = COLS*OPENING + (COLS+1)*T;          // 10.25
H = ROWS*OPENING + (ROWS+1)*T;          // 29.25

SQUARE   = (LEG_STYLE == "square");
PLATED   = (LEG_MOUNT == "plate") && !SQUARE;
MOUNT_XY = PLATED ? PLATE_XY : BLOCK_XY;
// a square leg butts straight up against the underside; nothing in between
MOUNT_H  = SQUARE ? 0 : (PLATED ? PLATE_T + PLATE_BOSS : BLOCK_H);

// Square legs stand plumb -- the splay is a mid-century idiom, not a nordic one
LEG_TILT_EFF = SQUARE ? 0 : LEG_TILT_SPEC;

// Per-axis splay that adds up to LEG_TILT_EFF of total lean:
// cos(splay) * cos(splay) == cos(tilt).
LEG_SPLAY  = acos(sqrt(cos(LEG_TILT_EFF)));
COSTILT    = cos(LEG_TILT_EFF);
LEG_AXIS_L = LEG_LENGTH;                      // shoulder -> floor, along the leg

LEG_RISE  = LEG_LENGTH * COSTILT + MOUNT_H;   // floor -> underside of case
OVERALL_H = H + LEG_RISE;                     // derived, not chosen

// z of the bottom face of horizontal member j.  j = 0 is the bottom rail,
// j = ROWS is the top rail, everything between is a shelf.
function hz(j)    = j * (OPENING + T);
// z of the bottom of the clear opening of row j
function row_z(j) = hz(j) + T;
// x of the left face of vertical divider i
function div_x(i) = (i + 1) * (OPENING + T);

RAILS_THROUGH = (END_JOINT == "rails_through");
EGG           = (GRID == "eggcrate");
function is_end_rail(j) = (j == 0 || j == ROWS);

// the lap plane: shelves keep the front half of the depth at a crossing, the
// divider keeps the back half, so the front elevation reads as continuous
// horizontals with the verticals dying into them
LAP_Y = DEPTH / 2;

// Fit clearance in the lap slots.  Real value in the shop, and it also keeps
// the shelf notch and the divider from sharing exactly coincident faces, which
// unions into a non-manifold mesh.
LAP_FIT = 0.002;

// a horizontal that runs through spans the full width; one that is housed
// into the stiles stops 1/4" inside each of them
function hx0(j) = (RAILS_THROUGH && is_end_rail(j)) ? 0 : T - DADO;
function hx1(j) = (RAILS_THROUGH && is_end_rail(j)) ? W : W - T + DADO;

// stiles are shortened when the end rails run through
STILE_Z0 = RAILS_THROUGH ? T - DADO     : 0;
STILE_Z1 = RAILS_THROUGH ? H - T + DADO : H;

// which horizontals are housed into the stiles
J_FIRST = RAILS_THROUGH ? 1        : 0;
J_LAST  = RAILS_THROUGH ? ROWS - 1 : ROWS;

EPS = 0.01;
$fa = 2; $fs = 0.08;

WALNUT  = "#5b3a24";
WALNUT2 = "#6b4630";
WALNUT3 = "#4d3020";
BRASS   = "#c8a34a";
STEEL   = "#3c4046";

// =============================================================
//  helpers
// =============================================================

// Through housing for a horizontal part, cut into a vertical face.
// under/over push the cut past the end of the board for the two housings
// that are rabbets.  Without that the cut's face lands exactly on the end of
// the stile and the coincident faces z-fight into a hairline sliver.
module dado_horizontal(x, z, len, under = 0, over = 0) {
    translate([x, -EPS, z - under])
        cube([len, DEPTH + 2*EPS, T + under + over]);
}

// through housing for a vertical divider, cut into a horizontal face
module dado_vertical(z, i) {
    translate([div_x(i), -EPS, z]) cube([T, DEPTH + 2*EPS, DADO_DIV + EPS]);
}

// =============================================================
//  carcass parts
// =============================================================

// left / right stile
module stile(side) {   // side = 0 left, 1 right
    x0 = (side == 0) ? 0        : W - T;
    xd = (side == 0) ? T - DADO : W - T - EPS;
    difference() {
        translate([x0, 0, STILE_Z0]) cube([T, DEPTH, STILE_Z1 - STILE_Z0]);

        // With END_JOINT = "stiles_through" this also cuts j = 0 and j = ROWS,
        // which run off the ends of the board and are therefore rabbets.
        for (j = [J_FIRST : J_LAST])
            dado_horizontal(xd, hz(j), DADO + EPS,
                            (j == 0)    ? EPS : 0,
                            (j == ROWS) ? EPS : 0);
    }
}

// Any of the seven horizontals.  j = 0 is the bottom rail, j = ROWS the top
// rail, 1..ROWS-1 are shelves.  All the same blank; they differ only in how
// many divider housings they carry.
module horizontal(j) {
    z0 = hz(j);
    difference() {
        translate([hx0(j), 0, z0]) cube([hx1(j) - hx0(j), DEPTH, T]);

        for (i = [0 : COLS - 2]) {
            if (EGG && !is_end_rail(j)) {
                // half lap: give the back half of the depth to the divider.
                // Open at the back edge and through the thickness, so it is
                // two saw cuts and knock the waste out.
                // The clearance goes only on the depth axis, where it is buried
                // inside the joint.  Putting it on the slot width instead
                // leaves a hairline you can see into the cell.
                translate([div_x(i), LAP_Y - LAP_FIT, z0 - EPS])
                    cube([T, DEPTH - LAP_Y + LAP_FIT + EPS, T + 2*EPS]);
            } else {
                if (j < ROWS) dado_vertical(z0 + T - DADO_DIV, i);   // above
                if (j > 0)    dado_vertical(z0 - EPS, i);            // below
            }
        }

        // an end rail that runs through carries the stile housings itself
        if (RAILS_THROUGH && is_end_rail(j)) {
            zd = (j == 0) ? z0 + T - DADO : z0 - EPS;
            for (s = [0, 1])
                translate([(s == 0) ? -EPS : W - T, -EPS, zd])
                    cube([T + EPS, DEPTH + 2*EPS, DADO + EPS]);
        }
    }
}

// short vertical divider inside one row, for GRID = "housed"
module divider(j, i) {
    translate([div_x(i), 0, row_z(j) - DADO_DIV])
        cube([T, DEPTH, OPENING + 2*DADO_DIV]);
}

// one continuous divider for GRID = "eggcrate", notched at every crossing
module divider_full(i) {
    z0 = row_z(0) - DADO_DIV;             // into the bottom rail's housing
    z1 = hz(ROWS) + DADO_DIV;             // into the top rail's housing
    difference() {
        translate([div_x(i), 0, z0]) cube([T, DEPTH, z1 - z0]);
        for (j = [1 : ROWS - 1])
            translate([div_x(i) - EPS, -EPS, hz(j) - LAP_FIT])
                cube([T + 2*EPS, LAP_Y + EPS, T + 2*LAP_FIT]);
    }
}

// whichever divider scheme is in force, for column gap i
module dividers(i) {
    if (EGG) divider_full(i);
    else for (j = [0 : ROWS - 1]) divider(j, i);
}

// explode: stiles out sideways, rails up/down, dividers forward,
// shelves stay put so the housings in the stiles stay readable
module carcass(explode = 0) {
    e = explode;

    color(WALNUT) translate([-1.8*e, 0, 0]) stile(0);
    color(WALNUT) translate([ 1.8*e, 0, 0]) stile(1);

    for (j = [0 : ROWS])
        color(WALNUT2) translate([0, 0, (j == 0) ? -1.2*e : (j == ROWS) ? 1.2*e : 0])
            horizontal(j);

    for (i = [0 : COLS - 2])
        color(WALNUT3) translate([0, -1.8*e, 0]) dividers(i);
}

// =============================================================
//  base: corner blocks + splayed tapered legs
// =============================================================

// leg axis direction: sx = -1 left / +1 right, sy = -1 front / +1 back
function leg_ax(sy) = sy * LEG_SPLAY;
function leg_ay(sx) = -sx * LEG_SPLAY;

TENON_D = 1.00;
TENON_L = 1.25;

// shaft diameter s inches down the leg axis from the shoulder
function shaft_d(s) = LEG_TOP_D + (LEG_BOT_D - LEG_TOP_D) * s / LEG_AXIS_L;

// leg axis coordinates: origin at the shoulder, shaft runs down -Z.
// "over" extends the cone past the shoulder so the flat shoulder cut has
// stock to remove instead of leaving a knife edge.
module leg_taper(extra = 0, over = 1.0) {
    translate([0, 0, -LEG_AXIS_L])
        cylinder(h = LEG_AXIS_L + over,
                 d1 = shaft_d(LEG_AXIS_L) + extra, d2 = shaft_d(-over) + extra);
}

module leg_tenon(extra = 0, extend = 0) {
    translate([0, 0, -extend]) cylinder(h = TENON_L + extend, d = TENON_D + extra);
}

// half space used to cut the shoulder square to the floor, not square to the
// leg.  Only the block mount needs it -- with a plate, the plate's angled seat
// carries the splay and the leg keeps an ordinary square shoulder.
module above_shoulder() { translate([-60, -60, -MOUNT_H]) cube([120, 120, 60]); }

// place leg geometry at corner (sx, sy); origin sits on the leg's shoulder
module at_leg(sx, sy) {
    px = (sx < 0) ? MOUNT_INSET + MOUNT_XY/2 : W - MOUNT_INSET - MOUNT_XY/2;
    py = (sy < 0) ? MOUNT_INSET + MOUNT_XY/2 : DEPTH - MOUNT_INSET - MOUNT_XY/2;
    translate([px, py, -MOUNT_H]) rotate([leg_ax(sy), leg_ay(sx), 0]) children();
}

module leg_wood(sx, sy) {
    color(WALNUT) union() {
        difference() {
            at_leg(sx, sy) leg_taper(0, PLATED ? 0 : 1.0);
            if (!PLATED) above_shoulder();
            // the brass ferrule takes over for the last 1-1/4"
            at_leg(sx, sy) translate([0, 0, -LEG_AXIS_L - EPS])
                cylinder(h = FERRULE_H + EPS, d = LEG_TOP_D + 1);
        }
        // block mount only: the tenon runs 0.3 past the shoulder into the
        // shaft, so the two solids overlap in volume rather than meeting on a
        // shared plane.  With a plate the fastener is a hidden hangar bolt.
        if (!PLATED) at_leg(sx, sy) leg_tenon(0, 0.3);
    }
}

// half space below the floor: the feet are trimmed flat to it, not square to
// the leg, so all four sit down and the piece is exactly OVERALL_H tall
module below_floor() { translate([-60, -60, -LEG_RISE - 60]) cube([120, 120, 60]); }

module leg_ferrule(sx, sy) {
    over = 0.3;   // run past the foot, then trim flat to the floor
    color(BRASS) difference() {
        at_leg(sx, sy) translate([0, 0, -LEG_AXIS_L - over])
            cylinder(h = FERRULE_H + over,
                     d1 = shaft_d(LEG_AXIS_L + over)  + FERRULE_OS,
                     d2 = shaft_d(LEG_AXIS_L - FERRULE_H) + FERRULE_OS);
        below_floor();
    }
}

// ---------------------------------------------------------------
//  Square tapered leg, scandinavian.  Tapered on its two INNER faces only, so
//  the outer faces stay plumb and continue the line of the case sides down to
//  the floor.  That asymmetry is the whole character of the leg.
// ---------------------------------------------------------------
module corner_slab(w, dx, dy, h) {
    translate([min(0, dx*w), min(0, dy*w), 0]) cube([w, w, h]);
}

function leg_xo(sx) = (sx < 0) ? SQ_INSET : W - SQ_INSET;
function leg_yo(sy) = (sy < 0) ? SQ_INSET : DEPTH - SQ_INSET;

module leg_square(sx, sy) {
    dx = (sx < 0) ? 1 : -1;
    dy = (sy < 0) ? 1 : -1;
    color(WALNUT) hull() {
        // runs 0.02 up into the case rather than stopping flush on its face
        translate([leg_xo(sx), leg_yo(sy), -0.02]) corner_slab(SQ_TOP, dx, dy, 0.04);
        translate([leg_xo(sx), leg_yo(sy), -LEG_LENGTH]) corner_slab(SQ_BOT, dx, dy, 0.02);
    }
}

// Two blocks hugging the leg's inner faces.  Long grain to long grain on both
// the leg and the underside of the case, which is why no hardware is needed.
module leg_blocks(sx, sy) {
    dx = (sx < 0) ? 1 : -1;
    dy = (sy < 0) ? 1 : -1;
    xo = leg_xo(sx); yo = leg_yo(sy);
    o = 0.02;   // overlap into the leg and into the case underside
    color(WALNUT3) {
        translate([min(xo + dx*(SQ_TOP - o), xo + dx*(SQ_TOP + GB_XY)),
                   min(yo, yo + dy*SQ_TOP), -GB_H])
            cube([GB_XY + o, SQ_TOP, GB_H + o]);
        translate([min(xo, xo + dx*SQ_TOP),
                   min(yo + dy*(SQ_TOP - o), yo + dy*(SQ_TOP + GB_XY)), -GB_H])
            cube([SQ_TOP, GB_XY + o, GB_H + o]);
    }
}

module base(explode = 0) {
    if (SQUARE) {
        for (sx = [-1, 1], sy = [-1, 1]) {
            translate([0, 0, -explode * 0.5]) leg_blocks(sx, sy);
            translate([0, 0, -explode * 2.2]) leg_square(sx, sy);
        }
    } else base_round(explode);
}

module base_round(explode = 0) {
    for (sx = [-1, 1], sy = [-1, 1]) {
        px = (sx < 0) ? MOUNT_INSET : W - MOUNT_INSET - MOUNT_XY;
        py = (sy < 0) ? MOUNT_INSET : DEPTH - MOUNT_INSET - MOUNT_XY;

        translate([0, 0, -explode * 0.5]) {
            if (PLATED) {
                color(STEEL) {
                    // flat base, screwed to the underside of the bottom rail
                    translate([px, py, -PLATE_T])
                        cube([MOUNT_XY, MOUNT_XY, PLATE_T]);
                    // the angled seat: a wedge whose underside is square to
                    // the leg and whose top is flat against the plate
                    intersection() {
                        at_leg(sx, sy) cylinder(h = 3, d = LEG_TOP_D);
                        translate([-60, -60, -60 - PLATE_T]) cube([120, 120, 60]);
                    }
                }
            } else {
                // walnut block, glued and screwed up into the bottom rail,
                // bored at the compound leg angle to take the tenon
                color(WALNUT3) difference() {
                    translate([px, py, -MOUNT_H])
                        cube([MOUNT_XY, MOUNT_XY, MOUNT_H]);
                    at_leg(sx, sy) leg_tenon(0.03, 0.2);
                }
            }
        }

        translate([0, 0, -explode * 2.2]) {
            leg_wood(sx, sy);
            leg_ferrule(sx, sy);
        }
    }
}

// =============================================================
//  bottle, for scale / renders  (750 ml bordeaux, 11.8" x 3.0")
// =============================================================
module bottle() {
    color("#20321f") {
        cylinder(h = 8.0, d = 3.0);
        translate([0, 0, 8.0]) cylinder(h = 1.8, d1 = 3.0, d2 = 1.15);
        translate([0, 0, 9.8]) cylinder(h = 1.6, d = 1.15);
    }
    color("#8b1a1a") translate([0, 0, 11.4]) cylinder(h = 0.4, d = 1.28);
}

// lying on its side, base near the back of the cell, neck out the front
module bottle_in_cell(j, i) {
    cx = T + i*(OPENING + T) + OPENING/2;
    cz = row_z(j) + 1.55;   // resting on the shelf, 3" dia
    translate([cx, DEPTH - 0.25, cz]) rotate([90, 0, 0]) bottle();
}

FILLED = [[0,1],[1,0],[1,1],[2,0],[3,1],[4,0],[5,0],[5,1]];

module bottles() {
    for (c = FILLED) bottle_in_cell(c[0], c[1]);
}

// keep the full-width top of whatever is passed in
module clip_top() {
    intersection() {
        children();
        translate([-1, -1, H - 5.6]) cube([W + 2, DEPTH + 2, 7]);
    }
}

// keep only the top left corner of whatever is passed in, for detail views
module clip_corner() {
    intersection() {
        children();
        // 5.6 rather than a round number so the cut never lands on a dado face
        translate([-1, -1, H - 5.6]) cube([6, DEPTH + 2, 7]);
    }
}

// =============================================================
//  assembly
// =============================================================
module rack(explode = 0) {
    carcass(explode);
    if (show_legs) base(explode);
}

scale(UNIT) {
    if (mode == "assembled") {
        rack(0);
        if (show_bottles) bottles();
    } else if (mode == "exploded") {
        rack(2.0);
    } else if (mode == "carcass") {
        carcass(0);
    } else if (mode == "joint") {
        // top left corner, pulled apart to show the rabbet
        color(WALNUT)                       clip_corner() stile(0);
        color(WALNUT2) translate([0, 0, 3]) clip_corner() horizontal(ROWS);
    } else if (mode == "lap") {
        // one crossing of the egg crate, pulled apart.  Short sections built
        // directly rather than clipped, so there are no cut faces in the view.
        dx = div_x(0);
        // shelf section: keeps the front 4-1/2, slot cut in from the back edge
        color(WALNUT2) translate([0, 0, 2.5]) difference() {
            translate([dx - 3, 0, 0]) cube([7, DEPTH, T]);
            translate([dx - LAP_FIT, LAP_Y - LAP_FIT, -EPS])
                cube([T + 2*LAP_FIT, DEPTH - LAP_Y + LAP_FIT + EPS, T + 2*EPS]);
        }
        // divider section: keeps the back 4-1/2, slot cut in from the front edge
        color(WALNUT3) translate([0, 0, -2.5]) difference() {
            translate([dx, 0, -3]) cube([T, DEPTH, 6 + T]);
            translate([dx - EPS, -EPS, -LAP_FIT])
                cube([T + 2*EPS, LAP_Y + EPS, T + 2*LAP_FIT]);
        }
    } else if (mode == "eggcrate") {
        // How the grid actually goes together.  The divider CANNOT drop in from
        // above: it is full depth everywhere except at its five notches, and a
        // full-depth section cannot pass a shelf, because the shelf's slot only
        // removes the back half.  Both sets of slots open on opposite edges, so
        // the only motion that engages them is a slide along the depth axis --
        // the divider enters from the back and travels LAP_Y forward.
        for (j = [1 : ROWS - 1]) color(WALNUT2) horizontal(j);
        color(WALNUT3) translate([0, LAP_Y + 1.4, 0]) dividers(0);
    } else if (mode == "stile") {
        color(WALNUT) stile(0);
    } else if (mode == "motion") {
        // The housing at the top of each stile is a rabbet, not a groove:
        // it is open upward as well as front and back, so the top rail drops
        // straight down onto the two ledges.  No sliding from the front.
        color(WALNUT) clip_top() stile(0);
        color(WALNUT) clip_top() stile(1);
        color("#8a5c38") translate([0, 0, 4]) clip_top() horizontal(ROWS);
    } else if (mode == "parts") {
        // every unique part laid out, for checking the cut list
        gap = 1.0;
        stile(0);
        translate([2.0, 0, 0]) stile(1);
        for (j = [0 : ROWS])
            translate([0, (1 + j)*(DEPTH + gap), -hz(j)]) horizontal(j);
        for (j = [0 : ROWS - 1])
            translate([-3, (1 + j)*(DEPTH + gap), -row_z(j)]) divider(j, 0);
    }
}

echo(str("end joint           = ", END_JOINT));
echo(str("carcass W x H x D   = ", W, " x ", H, " x ", DEPTH));
echo(str("overall height      = ", H + LEG_RISE));
echo(str("stile length        = ", STILE_Z1 - STILE_Z0, " x2"));
echo(str("end rail length     = ", hx1(0) - hx0(0), " x2"));
echo(str("shelf length        = ", hx1(1) - hx0(1), " x", ROWS - 1));
echo(str("grid                = ", GRID));
echo(EGG
     ? str("divider length      = ", hz(ROWS) + DADO_DIV - (row_z(0) - DADO_DIV),
           " x", COLS - 1, "  (notched ", LAP_Y, " deep at ", ROWS - 1, " crossings)")
     : str("divider length      = ", OPENING + 2*DADO_DIV, " x", ROWS * (COLS - 1)));
echo(str("leg style           = ", LEG_STYLE,
         SQUARE ? "  (made: square, tapered inner faces, plumb)"
                : str("  (bought: ", LEG_MOUNT, " mount, ", LEG_TILT_SPEC, " deg splay)")));
echo(str("leg length          = ", LEG_LENGTH));
echo(SQUARE ? str("  -> section        = ", SQ_TOP, " sq tapering to ", SQ_BOT)
            : str("  -> per-axis splay = ", LEG_SPLAY, " deg"));
echo(str("  -> rise to case   = ", LEG_RISE));
