// =============================================================
//  Coffee table -- solid walnut, mid-century
//
//  The position: ONE PLANE, FLOATING.  The top is a soft-edged solid slab that
//  overhangs the base by 2-1/2 to 3-1/2 inches on every side, undercut so hard
//  on its underside that a 1" panel shows a 7/16" arris.  The base is pulled
//  right back inside that outline and sits in the top's own shadow: two slim
//  rails, four splayed chamfered posts, and nothing across the ends at the top
//  at all, so you look straight through under the table from either end.
//
//  There is no visible joinery anywhere.  Every leg joint is a loose tenon,
//  which is also the only sane way to cut a joint against a compound-splayed
//  leg: both mating faces get routed square to themselves, and the angle lives
//  in the end cut instead of in the joint.
//
//  ALL DESIGN MATH IS IN INCHES.  The model is scaled by UNIT on output so the
//  scene OpenSCAD draws is in millimetres -- a 15" object is 15 units tall,
//  which sits inside OpenSCAD's near clip plane and makes the viewport
//  unusable.  Same reasoning as wine_rack.scad.
// =============================================================

UNIT = 25.4;   // 25.4 -> emit millimetres (recommended).  1 -> emit inches.

// ---------------- what to draw ----------------
// assembled | exploded | base | joint | edge | parts | none
mode       = "assembled";
show_top   = true;
show_shelf = true;

// =============================================================
//  the piece
// =============================================================
// 48 x 21 x 15.  Lower than the mid-century convention (15-17) on purpose:
// at 15" the top sits well below a seat cushion, so from a sofa you read the
// EDGE of the top and not its surface -- which is the whole argument for
// undercutting a 1" slab to a 7/16" arris.
LEN    = 48.00;
DEPTH  = 21.00;    // maximum, at mid-length
HEIGHT = 15.00;

// =============================================================
//  top
// =============================================================
TOP_T     = 1.000;    // 5/4 planed.  Thick for stiffness, thin to look at.
// The long edges bow out by BOW at mid-length, so the ends are 2*BOW narrower
// than the middle.  Three eighths over four feet is almost nothing measured and
// everything seen: it kills the parallel-sided slab look, and it is the reason
// the corners can be eased without the top turning into a lozenge.
BOW       = 0.375;
CORNER    = 1.500;    // corner radius

// The undercut.  EDGE_FACE is all you ever see of the top's thickness; the
// remaining 9/16 is chamfered away underneath at BEVEL_A and lives in shadow.
// Below about 3/8 the arris is too fragile to survive a vacuum cleaner, and
// above about 1/2 the top stops floating and starts sitting.
EDGE_FACE = 0.4375;
BEVEL_A   = 22;       // degrees off the underside plane

// =============================================================
//  legs
// =============================================================
LEG_TOP  = 1.625;   // square at the top
LEG_BOT  = 1.000;   // square at the foot
LEG_CHAM = 0.125;   // chamfer on all four arrises, at the top; it tapers with
                    // the leg, so the post reads as an elongated octagon and
                    // carries a highlight down its whole length

// Total lean off plumb, toward the corner -- a genuine compound splay, not a
// lean in one plane.  Written the way angled leg hardware is sold and the way
// wine_rack.scad already writes it: ONE number for the total tilt, with the
// per-axis angle derived, because cos(a)*cos(a) == cos(tilt).
LEG_TILT = 8;

END_OS  = 3.50;   // leg's outer face in from the end of the top
SIDE_OS = 3.00;   // leg's outer face in from y = 0, the top's widest line
LEG_SQ  = 3.00;   // full square before the taper starts, so the long rail joint
                  // sits on parallel faces

// =============================================================
//  rails
// =============================================================
// The long rails are the whole of the top frame.  Slim, set back a quarter of
// an inch inside the legs' faces so the post reads as a post and the rail as a
// plane behind it, and deep enough to make a real glue joint and no deeper.
RAIL_T = 1.125;
RAIL_H = 2.000;

// The cross rails are the only things that cross the width, and they are what
// stops the piece racking side to side.  Tapered: deep where the work is, at
// the legs, shallow in the middle where they are only carrying the shelf.
XR_T      = 0.875;
XR_TOP_Z  = 5.000;   // top edge off the floor -- the shelf sits on this
XR_H_LEG  = 3.000;
XR_H_MID  = 1.750;

// =============================================================
//  loose tenons
// =============================================================
// Shopmade, quartersawn, grain along the length, ends rounded to match a routed
// mortise.  Not dominoes: 5/16 x 1-1/2 in walnut is a real tenon, and it is cut
// on the same router jig that cuts the mortises -- which is the only sane way to
// hold a compound-splayed leg square to a cutter without building a cradle for
// each of the eight joints.
LT_T   = 0.3125;
LT1_W  = 1.500;   // long rail: one tenon
LT1_L  = 2.250;   // 1-1/8 into each member
// The cross rail gets TWO, stacked.  A single central tenon resists racking
// with whatever moment arm its own width gives it; two tenons 1-1/2 apart
// resist it with 1-1/2 inches of lever, and neither mortise has to be deeper
// than the tapered leg can take.
LT2_W  = 1.000;
LT2_L  = 1.500;   // 3/4 into each member
LT2_DZ = 0.750;   // above and below the cross rail joint's centre

// =============================================================
//  shelf
// =============================================================
// A second thin plane, undercut on its long edges the same way as the top, so
// the two read as the same object at two scales.
SHELF_T  = 0.625;
SHELF_D  = 11.00;
SHELF_CH = 0.250;   // undercut, leaving 3/8 of visible edge
SHELF_OS = 0.500;   // overhang past the cross rail

// =============================================================
//  buttons -- the only thing holding the top on
// =============================================================
BTN_N    = 4;       // per rail
BTN_L    = 1.125;
BTN_W    = 0.875;
BTN_T    = 0.500;
BTN_TN_T = 0.250;
// The groove runs along the length, so a button cannot slide along it in the
// direction the top actually moves.  Instead it rides OUT of the groove as the
// top shrinks, and BTN_GAP is that travel.  Close the gap up and you have
// screwed a 21"-wide slab of walnut to a rigid frame.
BTN_GAP  = 0.125;
GRV_W    = 0.280;
GRV_D    = 0.375;
GRV_DN   = 0.500;   // top of the groove below the rail's top edge

// =============================================================
//  tolerances
// =============================================================
// FIT does three jobs: a real joint clearance, a lap of solid into solid where
// two parts merely touch (coplanar faces union into a non-manifold mesh), and
// enough of an offset that mating surfaces do not z-fight.  0.01 is below one
// pixel at render scale; 0.02 is not.
FIT = 0.02;
EPS = 0.01;    // overshoot on subtractive cuts, so a cut face never lands
               // exactly on the parent's face
BIG = 400;

$fa = 2; $fs = 0.08;

WALNUT  = "#5b3a24";   // legs
WALNUT2 = "#6b4630";   // top
WALNUT3 = "#4d3020";   // rails
WALNUT4 = "#7d5a3e";   // shelf
PEGWOOD = "#a87c4a";   // loose tenons and buttons, drawn light so the hidden
                       // joinery can be seen at all in the detail views

// =============================================================
//  derived
// =============================================================
TOP_Z1 = HEIGHT;
TOP_Z0 = HEIGHT - TOP_T;      // underside of the top
LEG_Z  = TOP_Z0;

BEVEL_DROP = TOP_T - EDGE_FACE;
BEVEL_R    = BEVEL_DROP / tan(BEVEL_A);       // horizontal run of the undercut

// the bow, as a very large radius
BOW_R = ((LEN/2)*(LEN/2) + BOW*BOW) / (2*BOW);

// Per-axis splay that adds up to LEG_TILT of total lean.  Exactly the wine
// rack's identity: cos(splay)*cos(splay) == cos(tilt).
SPLAY  = acos(sqrt(cos(LEG_TILT)));
LEG_L  = LEG_Z / cos(LEG_TILT);               // along the leg's own axis
LEG_OVER = 0.75;                              // built long, then trimmed flat
LEG_BOT2 = LEG_TOP - (LEG_TOP - LEG_BOT) * (LEG_L + LEG_OVER - LEG_SQ)
                                          / (LEG_L - LEG_SQ);
TAPER_A = atan(((LEG_TOP - LEG_BOT)/2) / (LEG_L - LEG_SQ));

function leg_cx(sx) = (sx < 0) ? END_OS + LEG_TOP/2 : LEN - END_OS - LEG_TOP/2;
function leg_cy(sy) = (sy < 0) ? SIDE_OS + LEG_TOP/2 : DEPTH - SIDE_OS - LEG_TOP/2;
// where the leg's centre has got to by height z.  Falls straight out of the
// rotation: dX/dZ = -tan(splay), dY/dZ = -tan(splay)/cos(splay).
function leg_cx_at(sx, z) = leg_cx(sx) + sx * (LEG_Z - z) * tan(SPLAY);
function leg_cy_at(sy, z) = leg_cy(sy) + sy * (LEG_Z - z) * tan(SPLAY) / cos(SPLAY);
// across the flats at height z
function leg_d(z)   = (LEG_Z - z) / cos(LEG_TILT);      // distance along the axis
function leg_sec(z) = (leg_d(z) <= LEG_SQ) ? LEG_TOP
    : LEG_TOP - (LEG_TOP - LEG_BOT) * (leg_d(z) - LEG_SQ) / (LEG_L - LEG_SQ);

// rails
RAIL_Z1 = TOP_Z0 + FIT;                 // laps FIT up into the underside
RAIL_Z0 = RAIL_Z1 - RAIL_H;
RAIL_SETBACK = (LEG_TOP - RAIL_T) / 2;  // rail centred on the leg
function rail_yc(sy) = leg_cy(sy);
RAIL_ZC = (RAIL_Z0 + RAIL_Z1) / 2;

XR_Z_LEG = XR_TOP_Z - XR_H_LEG;         // bottom edge at the legs
XR_Z_MID = XR_TOP_Z - XR_H_MID;         // bottom edge at mid-span
XR_ZC    = (XR_Z_LEG + XR_TOP_Z) / 2;   // the joint's centre
function xr_cx(sx) = leg_cx_at(sx, XR_ZC);
// where the legs' inner faces are, so the taper can start AT them.  Run the
// taper from the blank's ends instead and the rail arrives at the leg already
// two thirds of the way up its V, with the lower tenon hanging out in the air.
XR_Y0 = leg_cy_at(-1, XR_ZC) + leg_sec(XR_ZC)/2;
XR_Y1 = leg_cy_at( 1, XR_ZC) - leg_sec(XR_ZC)/2;

// joint centres, as distances down the leg's OWN axis
ZL_LONG  = -(LEG_Z - RAIL_ZC) / cos(LEG_TILT);
ZL_XR    = -(LEG_Z - XR_ZC)   / cos(LEG_TILT);
// the leg's face, in local coordinates, at a given local height
function local_face(zl) = (zl >= -LEG_SQ)
    ? LEG_TOP/2
    : LEG_TOP/2 + (zl + LEG_SQ) * tan(TAPER_A);
// which way to spin the leg's local frame so +x is the face we want
function ang_long(sx)  = (sx < 0) ? 0  : 180;
function ang_cross(sy) = (sy < 0) ? 90 : 270;

// shelf
SHELF_X0 = xr_cx(-1) - XR_T/2 - SHELF_OS;
SHELF_X1 = xr_cx( 1) + XR_T/2 + SHELF_OS;
SHELF_L  = SHELF_X1 - SHELF_X0;
SHELF_Y0 = DEPTH/2 - SHELF_D/2;
SHELF_Z0 = XR_TOP_Z - FIT;

// =============================================================
//  the top
// =============================================================

// The plan: a lens cut off square at both ends, then every convex corner eased
// by offsetting in and back out again.  Shrink-then-grow rounds convex corners
// only, which is exactly what is wanted -- there are no concave ones.
module top_plan() {
    offset(r = CORNER) offset(delta = -CORNER)
        intersection() {
            translate([LEN/2, BOW_R])         circle(r = BOW_R, $fn = 1440);
            translate([LEN/2, DEPTH - BOW_R]) circle(r = BOW_R, $fn = 1440);
            translate([0, -1]) square([LEN, DEPTH + 2]);
        }
}

// EDGE_FACE of square edge, then the undercut running in to the underside.
// Built as a hull between the full plan and the plan offset in by the chamfer's
// run, so the undercut follows the bow and the eased corners for free.
module top() {
    translate([0, 0, TOP_Z1]) hull() {
        translate([0, 0, -EDGE_FACE]) linear_extrude(EDGE_FACE + EPS) top_plan();
        translate([0, 0, -TOP_T])
            linear_extrude(EPS) offset(delta = -BEVEL_R) top_plan();
    }
}

// =============================================================
//  legs
// =============================================================

// square with all four arrises chamfered
module cham_square(s, c) {
    polygon([[-s/2 + c, -s/2], [ s/2 - c, -s/2], [ s/2, -s/2 + c], [ s/2,  s/2 - c],
             [ s/2 - c,  s/2], [-s/2 + c,  s/2], [-s/2,  s/2 - c], [-s/2, -s/2 + c]]);
}

// leg-local: origin on the top face centre, post running down -Z
module leg_local() {
    translate([0, 0, -LEG_SQ])
        linear_extrude(LEG_SQ + LEG_OVER) cham_square(LEG_TOP, LEG_CHAM);
    // the chamfer narrows with the section, which is what a tapered chamfered
    // post actually does -- hold it constant and the leg looks like a moulding
    hull() {
        translate([0, 0, -LEG_SQ]) linear_extrude(EPS) cham_square(LEG_TOP, LEG_CHAM);
        translate([0, 0, -(LEG_L + LEG_OVER)])
            linear_extrude(EPS) cham_square(LEG_BOT2, LEG_CHAM*LEG_BOT2/LEG_TOP);
    }
}

// place a child in one leg's own frame
module at_leg(sx, sy) {
    translate([leg_cx(sx), leg_cy(sy), LEG_Z])
        rotate([sy*SPLAY, -sx*SPLAY, 0]) children();
}

// Everything on the LEG's side of one of its faces, so a rail can be cut back
// to it.  FIT of the rail is left buried in the leg: two solids that merely
// touch on a plane union into a non-manifold mesh.
module leg_side_straight(ang) {
    rotate([0, 0, ang])
        translate([LEG_TOP/2 - FIT - BIG, -BIG/2, -BIG/2]) cube(BIG);
}
// the same, for the tapered part of the leg -- this is the angle the cross
// rail's ends are actually sawn to, on top of the compound splay
module leg_side_taper(ang) {
    rotate([0, 0, ang])
        translate([LEG_TOP/2 - FIT, 0, -LEG_SQ]) rotate([0, TAPER_A, 0])
            translate([-BIG, -BIG/2, -BIG/2]) cube(BIG);
}

// a routed mortise, and the loose tenon that fills it: a slot with rounded ends
module lt_shape(len, w, t) {
    rotate([0, 90, 0]) linear_extrude(len, center = true)
        hull() {
            translate([-(w - t)/2, 0]) circle(d = t);
            translate([ (w - t)/2, 0]) circle(d = t);
        }
}

// straddling the joint face, half in the leg and half in the rail
module lt_at(sx, sy, ang, zl) {
    at_leg(sx, sy) rotate([0, 0, ang]) translate([local_face(zl), 0, zl]) children();
}

module lt_long(sx, sy, extra = 0) {
    lt_at(sx, sy, ang_long(sx), ZL_LONG)
        lt_shape(LT1_L + extra, LT1_W + extra, LT_T + extra);
}

module lt_cross(sx, sy, extra = 0) {
    for (k = [-1, 1])
        lt_at(sx, sy, ang_cross(sy), ZL_XR + k*LT2_DZ)
            lt_shape(LT2_L + extra, LT2_W + extra, LT_T + extra);
}

module leg(sx, sy) {
    render(convexity = 8) difference() {
        at_leg(sx, sy) leg_local();
        // trimmed flat to the FLOOR and flat to the underside of the top, not
        // square to the leg -- a compound-splayed post cut square stands on a
        // corner and holds the top on a knife edge
        translate([-BIG/2, -BIG/2, -BIG]) cube(BIG);
        translate([-BIG/2, -BIG/2, LEG_Z + FIT]) cube(BIG);
        lt_long(sx, sy, 2*FIT);
        lt_cross(sx, sy, 2*FIT);
    }
}

module tenons() {
    for (sx = [-1, 1], sy = [-1, 1]) {
        lt_long(sx, sy);
        lt_cross(sx, sy);
    }
}

// =============================================================
//  rails
// =============================================================

module long_rail(sy) {
    yc = rail_yc(sy);
    render(convexity = 8) difference() {
        translate([-1, yc - RAIL_T/2, RAIL_Z0]) cube([LEN + 2, RAIL_T, RAIL_H]);
        for (sx = [-1, 1]) at_leg(sx, sy) leg_side_straight(ang_long(sx));
        for (sx = [-1, 1]) lt_long(sx, sy, 2*FIT);
        // groove for the buttons, ploughed along the inner face
        translate([-1, yc + ((sy < 0) ? RAIL_T/2 - GRV_D : -RAIL_T/2 - EPS),
                   RAIL_Z1 - GRV_DN - GRV_W])
            cube([LEN + 2, GRV_D + EPS, GRV_W]);
    }
}

// Profile in (y, z), extruded along the length axis.
//
// TRAP, and it cost an hour: OpenSCAD's OpenCSG PREVIEW silently drops whole
// subtractions from non-convex solids.  Every rail here is a blank with four
// half spaces and several mortises taken out of it, and the preview showed the
// rails running straight through the legs while the CGAL mesh was correct all
// along.  Every part that is a difference is therefore wrapped in render(),
// with colour() outside it -- render() discards a colour set inside.
module cross_rail(sx) {
    xc = xr_cx(sx);
    translate([xc - XR_T/2, 0, 0]) rotate([90, 0, 90])
        linear_extrude(XR_T, convexity = 6)
            polygon([[-2, XR_TOP_Z], [DEPTH + 2, XR_TOP_Z],
                     [DEPTH + 2, XR_Z_LEG], [XR_Y1, XR_Z_LEG],
                     [DEPTH/2, XR_Z_MID], [XR_Y0, XR_Z_LEG], [-2, XR_Z_LEG]]);
}

module cross_rail_cut(sx) {
    render(convexity = 6) difference() {
        cross_rail(sx);
        for (sy = [-1, 1]) at_leg(sx, sy) leg_side_taper(ang_cross(sy));
        for (sy = [-1, 1]) lt_cross(sx, sy, 2*FIT);
    }
}

// =============================================================
//  shelf
// =============================================================
module shelf() {
    run = SHELF_CH / tan(BEVEL_A);
    hull() {
        translate([SHELF_X0, SHELF_Y0, SHELF_Z0 + SHELF_CH])
            cube([SHELF_L, SHELF_D, SHELF_T - SHELF_CH]);
        translate([SHELF_X0, SHELF_Y0 + run, SHELF_Z0])
            cube([SHELF_L, SHELF_D - 2*run, EPS]);
    }
}

// =============================================================
//  buttons
// =============================================================
module button(sy) {
    d     = (sy < 0) ? 1 : -1;                        // toward the middle
    yface = rail_yc(sy) + ((sy < 0) ? RAIL_T/2 : -RAIL_T/2);
    ybody = yface + d*BTN_GAP;
    ztop  = TOP_Z0 + FIT;
    translate([-BTN_L/2, min(ybody, ybody + d*BTN_W), ztop - BTN_T])
        cube([BTN_L, BTN_W, BTN_T]);
    ztn = RAIL_Z1 - GRV_DN - GRV_W/2;
    translate([-BTN_L/2, min(yface + d*(BTN_GAP + FIT), yface - d*(GRV_D - BTN_GAP)),
               ztn - BTN_TN_T/2])
        cube([BTN_L, GRV_D + FIT, BTN_TN_T]);
}

module buttons() {
    // the middle pair on each rail are screwed through round holes and fix the
    // top along its length, where it does not move.  Nothing fixes it across
    // the width -- that is the point.
    x0 = leg_cx(-1) + 2.5;
    x1 = leg_cx( 1) - 2.5;
    for (sy = [-1, 1], k = [0 : BTN_N - 1])
        translate([x0 + k*(x1 - x0)/(BTN_N - 1), 0, 0]) button(sy);
}

// =============================================================
//  assembly
// =============================================================
// Explode factors: every part moves along the axis it is assembled on, so the
// picture doubles as an assembly order.
module base_only(e = 0) {
    for (sx = [-1, 1], sy = [-1, 1])
        color(WALNUT) translate([sx*3.0*e, sy*3.0*e, -3.0*e]) leg(sx, sy);
    for (sy = [-1, 1])
        color(WALNUT3) translate([0, sy*8.0*e, 1.5*e]) long_rail(sy);
    for (sx = [-1, 1])
        color(WALNUT3) translate([sx*5.0*e, 0, -1.5*e]) cross_rail_cut(sx);
    color(PEGWOOD) translate([0, 0, 4.5*e]) tenons();
    if (show_shelf) color(WALNUT4) translate([0, 0, -5.5*e]) shelf();
}

module table(e = 0) {
    base_only(e);
    color(PEGWOOD) translate([0, 0, 7.5*e]) buttons();
    if (show_top) color(WALNUT2) translate([0, 0, 14.0*e]) top();
}

// ---- detail helpers ----
module clip(x0, x1, y0, y1, z0, z1) {
    intersection() {
        children();
        translate([x0, y0, z0]) cube([x1 - x0, y1 - y0, z1 - z0]);
    }
}

// everything past a plane, for the sectioned edge detail
module beyond_x(x) { translate([x, -BIG/2, -BIG/2]) cube(BIG); }
module beyond_y(y) { translate([-BIG/2, y, -BIG/2]) cube(BIG); }
module section_cut() { beyond_x(LEN/2); beyond_y(DEPTH/2 - 1); }

scale(UNIT) {
    if (mode == "assembled") {
        table(0);
    } else if (mode == "exploded") {
        table(1.0);
    } else if (mode == "base") {
        base_only(0);
    } else if (mode == "joint") {
        // The front left leg with both rails drawn off along their own axes and
        // the three loose tenons standing in the air between them.  This is the
        // whole of the piece's joinery; there is nothing else to show.
        rx = 5.0; ry = 8.0;
        color(WALNUT) leg(-1, -1);
        color(WALNUT3) translate([rx, 0, 0])
            clip(0, leg_cx(-1) + 3.5, 0, DEPTH, 0, HEIGHT) long_rail(-1);
        // the cross rail is drawn off toward the BACK leg, not the front: it
        // extends inboard from this joint, so pulling it forward would just
        // slide its own body over the gap
        color(WALNUT3) translate([0, ry, 0])
            clip(0, LEN/2, -BIG, DEPTH/2, 0, HEIGHT) cross_rail_cut(-1);
        color(PEGWOOD) translate([rx/2, 0, 0]) lt_long(-1, -1);
        color(PEGWOOD) translate([0, ry/2, 0]) lt_cross(-1, -1);
    } else if (mode == "edge") {
        // A section across the table at mid-length: the only place the float is
        // actually measurable.  7/16 of visible edge, then the undercut running
        // back into shadow, then daylight before the rail even starts.
        // render() around each piece, colour() outside it: sibling
        // colour(difference(...)) nodes at the same level get merged into one
        // CSG product by the preview and come out in the last colour declared.
        color(WALNUT2) render() difference() { top(); section_cut(); }
        color(WALNUT3) render() difference() { long_rail(-1); section_cut(); }
        color(PEGWOOD) render() difference() {
            intersection() {
                buttons();
                translate([LEN/2 - 7, -1, 0]) cube([7, DEPTH + 2, HEIGHT]);
            }
            section_cut();
        }
        if (show_shelf) color(WALNUT4) render() difference() { shelf(); section_cut(); }
    } else if (mode == "parts") {
        // every unique part, spread clear of the others
        g   = 3.0;
        py1 = DEPTH + g;
        py2 = py1 + SHELF_D + g;
        color(WALNUT2) translate([0, 0, -TOP_Z0]) top();
        color(WALNUT4) translate([0, py1 - SHELF_Y0, -SHELF_Z0]) shelf();
        color(WALNUT3) translate([0, py2 - rail_yc(-1), -RAIL_Z0]) long_rail(-1);
        color(WALNUT3) translate([LEN + g - xr_cx(-1) + XR_T/2, 0, -XR_Z_LEG])
            cross_rail_cut(-1);
        for (i = [0, 1])
            color(WALNUT) translate([LEN + 3*g + 3 + i*3.5 - leg_cx(-1),
                                     py1 - leg_cy((i == 0) ? -1 : 1), 0])
                leg(-1, (i == 0) ? -1 : 1);
        color(PEGWOOD) translate([LEN + 3*g, py2 - rail_yc(-1), -RAIL_Z0])
            button(-1);
    }
}

// =============================================================
//  the numbers
// =============================================================
echo(str("overall            = ", LEN, " L x ", DEPTH, " D x ", HEIGHT, " H"));
echo(str("top                = ", LEN, " x ", DEPTH, " x ", TOP_T,
         "   (", DEPTH - 2*BOW, " at the ends, ", CORNER, " corner radius)"));
echo(str("  edge reads as    = ", EDGE_FACE, "  (", BEVEL_A, " deg undercut, ",
         BEVEL_R, " of run)"));
echo(str("  bow radius       = ", BOW_R));
echo(str("leg                = ", LEG_TOP, " sq -> ", LEG_BOT, " sq, ", LEG_L,
         " on the axis, ", LEG_CHAM, " chamfer"));
echo(str("  splay            = ", LEG_TILT, " deg total toward the corner = ",
         SPLAY, " deg per axis"));
echo(str("  foot centres     = ", leg_cx_at(-1,0), ", ", leg_cy_at(-1,0),
         "   (top centres ", leg_cx(-1), ", ", leg_cy(-1), ")"));
echo(str("  taper angle      = ", TAPER_A,
         " deg  (on top of the splay, on the cross rail's end cuts)"));
echo(str("top overhangs base = ", leg_cx(-1) - LEG_TOP/2, " at the ends, ",
         leg_cy(-1) - LEG_TOP/2 - BOW, " at the sides (at the legs)"));
echo(str("long rail          = ", LEN - 2*(leg_cx(-1) + LEG_TOP/2),
         " between the legs, ", RAIL_H, " x ", RAIL_T,
         ", set back ", RAIL_SETBACK));
echo(str("cross rail         = ", XR_T, " thick, ", XR_H_LEG,
         " deep at the legs, ", XR_H_MID, " at mid-span, top edge at ",
         XR_TOP_Z));
echo(str("loose tenons       = long ", LT_T, " x ", LT1_W, " x ", LT1_L,
         " x4;  cross ", LT_T, " x ", LT2_W, " x ", LT2_L, " x8 (twin, ",
         2*LT2_DZ, " apart)"));
echo(str("shelf              = ", SHELF_L, " x ", SHELF_D, " x ", SHELF_T));
echo(str("leg section at the cross rail joints = ", leg_sec(XR_ZC - LT2_DZ),
         " and ", leg_sec(XR_ZC + LT2_DZ)));
