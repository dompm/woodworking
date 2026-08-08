// =============================================================
//  Salt boxes -- stack-laminated hardwood, swivelling lid
//
//  A pair, differing only in height: one for MSG, one for sugar.
//
//  Laminated rather than hollowed from a solid blank, because a blind pocket
//  that deep can't be template-routed -- the bearing has to stay inside the
//  template, and the deeper you plunge the higher it sits.  Cut the cavity
//  straight THROUGH the middle layers instead and it is one template pass per
//  layer, dead square, no Forstner wandering off perpendicular.
//
//  Cut the layers in sequence from one board and stack them in order: the
//  figure runs on through the glue lines and they nearly disappear.
//
//      openscad salt_box.scad
//      openscad -D LAYERS=3 -D 'mode="open"' salt_box.scad
// =============================================================
UNIT = 25.4;

mode = "assembled";  // assembled | open | exploded | section | parts | none

// ---------------- stock
// Everything is 3/4.  A thinner lid and bottom would sit a touch better, but
// it would mean getting stock planed specially, and one thickness throughout
// means every one of the ten pieces comes off the same board.
T_MID = 0.75;        // middle layers -- 4/4 dressed
T_CAP = 0.75;        // lid and bottom

// ---------------- box
SIZE   = 3.25;       // outside, square
WALL   = 0.50;
LAYERS = 2;          // middle layers.  2 -> MSG, 3 -> sugar

// Outside vertical corners.  Generous on purpose: a small ease on an object
// this size just reads as a slightly less sharp box.  At 1/2 the corners
// become quarter-cylinders and the silhouette actually changes.
CORNER_R = 0.50;

// Inside corners come free from the cutter -- a 1/2 bit CANNOT leave anything
// tighter than 1/4.  Nothing to decide and nothing to pay for.
BIT_D  = 0.50;
CAV_R  = BIT_D / 2;

// Roundover on the lid's edges.  The lid is what the hand meets, so it gets
// softened all the way round rather than just at the corners.
LID_R = 0.1875;

// ---------------- hardware
PIVOT_IN = 0.40;     // pivot centre, in from two adjacent edges
PIVOT_D  = 0.15;     // #6 brass screw
MAG_D    = 0.25;     // 6mm disc magnet
MAG_H    = 0.125;    // 3mm deep
MAG_IN   = 0.55;

// ---------------- derived
INNER  = SIZE - 2*WALL;
CAV_H  = LAYERS * T_MID;
BODY_H = T_CAP + CAV_H;
TOTAL  = BODY_H + T_CAP;

EPS   = 0.01;
OVER  = 0.02;        // layers overlap rather than share a face -- see README
SHRNK = 0.012;       // hardware modelled undersize, same reason

WOOD  = "#8a5a34";
WOOD2 = "#7d5130";
BRASS = "#c8a34a";
STEEL = "#8d949c";

// =============================================================
//  2D
// =============================================================
module outer_2d() {
    translate([CORNER_R, CORNER_R])
        offset(r = CORNER_R, $fn = 64)
            square(SIZE - 2*CORNER_R);
}

module cavity_2d() {
    translate([WALL + CAV_R, WALL + CAV_R])
        offset(r = CAV_R, $fn = 48)
            square(INNER - 2*CAV_R);
}

// =============================================================
//  parts
// =============================================================
module bottom() {
    linear_extrude(T_CAP) outer_2d();
}

function mid_z(i) = T_CAP + i*T_MID - OVER;
function mid_h()  = T_MID + OVER;

module middle() {
    difference() {
        linear_extrude(mid_h()) outer_2d();
        translate([0, 0, -EPS]) linear_extrude(mid_h() + 2*EPS) cavity_2d();
    }
}

// Rounded on every edge, not just the vertical corners.  Minkowski with a
// sphere is the honest way to say that: shrink the profile by the radius,
// shorten it by twice the radius, then grow it back in every direction at once.
module lid() {
    difference() {
        translate([0, 0, LID_R])
            minkowski() {
                linear_extrude(T_CAP - 2*LID_R)
                    offset(r = -LID_R, $fn = 48) outer_2d();
                sphere(r = LID_R, $fn = 24);
            }
        translate([PIVOT_IN, PIVOT_IN, -EPS])
            cylinder(h = T_CAP + 2*EPS, d = PIVOT_D + 0.02, $fn = 32);
        translate([SIZE - MAG_IN, SIZE - MAG_IN, -EPS])
            cylinder(h = MAG_H + EPS, d = MAG_D, $fn = 48);
    }
}

// =============================================================
//  assembly
// =============================================================
module hardware() {
    color(BRASS) translate([PIVOT_IN, PIVOT_IN, BODY_H - 0.5])
        cylinder(h = 0.5 + T_CAP, d = PIVOT_D - SHRNK, $fn = 32);
    color(BRASS) translate([PIVOT_IN, PIVOT_IN, BODY_H + T_CAP])
        cylinder(h = 0.07, d = PIVOT_D*2.1, $fn = 32);
    color(STEEL) translate([SIZE - MAG_IN, SIZE - MAG_IN, BODY_H - MAG_H])
        cylinder(h = MAG_H, d = MAG_D - SHRNK, $fn = 48);
}

module box(swing = 0, explode = 0) {
    color(WOOD) bottom();
    for (i = [0 : LAYERS - 1])
        color(WOOD2) translate([0, 0, mid_z(i) + explode*(1 + i)]) middle();
    translate([0, 0, BODY_H + EPS + explode*(1 + LAYERS)])
        translate([PIVOT_IN, PIVOT_IN, 0])
            rotate([0, 0, swing])
                translate([-PIVOT_IN, -PIVOT_IN, 0])
                    color(WOOD) lid();
    if (explode == 0) hardware();
}

scale(UNIT) {
    if (mode == "assembled") {
        box(0);
    } else if (mode == "open") {
        box(85);
    } else if (mode == "exploded") {
        box(0, 0.85);
    } else if (mode == "section") {
        difference() {
            box(0);
            translate([-1, -1, -1]) cube([SIZE + 2, SIZE/2 + 1, TOTAL + 2]);
        }
    } else if (mode == "parts") {
        color(WOOD)  bottom();
        color(WOOD2) translate([SIZE + 0.5, 0, 0]) middle();
        color(WOOD)  translate([2*(SIZE + 0.5), 0, 0]) lid();
    }
}

CAV_AREA = INNER*INNER - (4 - PI)*CAV_R*CAV_R;
VOL_ML   = CAV_AREA * CAV_H * 16.387;

echo(str("outside          = ", SIZE, " sq x ", TOTAL, " tall"));
echo(str("wall             = ", WALL, " at the faces, ",
         "thicker at the corners"));
echo(str("cavity           = ", INNER, " sq x ", CAV_H, " deep  (",
         LAYERS, " middle layers)"));
echo(str("corner radius    = ", CORNER_R, " outside, ", CAV_R,
         " inside (the bit)"));
echo(str("holds            = ", VOL_ML, " ml = ", VOL_ML/236.6, " cups"));
echo(str("parts            = 1 bottom @", T_CAP, " + ", LAYERS, " middle @",
         T_MID, " + 1 lid @", T_CAP));
