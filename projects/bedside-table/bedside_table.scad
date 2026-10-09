// =============================================================
//  Bedside table -- cubby box in solid yellow birch
//
//  Parametric CAD model for a mid-century cubby bedside table:
//  - 18" W x 13" D x 7" H carcass in 3/4" yellow birch
//  - Joinery options: "rabbet" (default, self-squaring 3/8" rebate),
//    "miter" (45-degree through miter), or "butt" (simple butt joint)
//  - Refined 1/8" chamfer easing all outer and inner rim arrises
//    and the 4 long front-to-back horizontal corners
//  - Completely open pass-through for cables and clean minimalist look
//  - 14" mid-century splayed tapered conical metal legs (21" overall height,
//    perfect match for IKEA MALM bed / 55 cm nightstand standard)
//
//  ALL DESIGN MATH IS IN INCHES. Emits millimetres (UNIT = 25.4) on output.
// =============================================================

UNIT = 25.4;

// ---------------- mode ----------------
// assembled | exploded | carcass | waterfall | joint | miter_joint | rabbet_joint
mode = "assembled";

// ---------------- joinery style ----------------
// "rabbet" (recommended DIY) | "miter" | "butt"
joint_type = "rabbet";

show_legs   = true;
show_screws = false;
chamfer_on  = false; // Set false for clean, honest rabbet casework; true for miter


// ---------------- carcass dimensions ----------------
W = 16.00;   // outside width (scaled down from 18" to 16" for compact nightstand)
D = 12.00;   // outside depth (scaled from 13" to 12" for perfect 4:3 proportion)
H =  7.00;   // outside height of wooden box (matches IKEA MALM height with 14" legs)
T =  0.75;   // stock thickness (4/4 yellow birch planed to 3/4")

// Rabbet dimensions (for joint_type == "rabbet")
R_DEPTH = 0.375; // 3/8" deep rabbet (half of stock thickness T)
R_WIDTH = T;     // 3/4" wide rabbet to receive side panel

CHAMFER = 0.125; // 1/8" chamfer (used if chamfer_on = true)

// Internal clear opening (derived)
CLEAR_W = W - 2*T;  // 14.50"
CLEAR_H = H - 2*T;  //  5.50"
CLEAR_D = D;        // 12.00" pass-through

// ---------------- legs (store-bought mid-century metal) ----------------
LEG_H        = 14.00;  // vertical rise from floor to underside of box
LEG_TOP_D    =  1.00;  // diameter at top of shaft
LEG_BOT_D    =  0.50;  // diameter at foot
LEG_TILT     = 11.00;  // total degrees tilt off plumb toward corner
LEG_SPLAY    = acos(sqrt(cos(LEG_TILT))); // per-axis tilt (~7.8 deg)

// Mounting plate (80mm x 80mm ~ 3-1/8" square stamped steel plate)
PLATE_W      = 3.125;
PLATE_L      = 3.125;
PLATE_T      = 0.125;  // 1/8" plate thickness
HOLE_D       = 0.20;   // screw hole diameter
HOLE_OS      = 0.40;   // hole distance from plate edge

// Plate position inset from carcass outer edges
LEG_INSET_X  = 1.75;
LEG_INSET_Y  = 1.75;

// Foot glide (rubber / brass)
GLIDE_H      = 0.375;
GLIDE_D      = 0.625;

// Overall height derived
OVERALL_H    = H + LEG_H; // 21.00" nominal

// ---------------- colors ----------------
BIRCH        = "#e5cca0";
BIRCH_EDGE   = "#d8b684";
BIRCH_END    = "#c89f68";
METAL        = "#222222";
BRASS        = "#caa355";
SCREW        = "#888888";

EPS = 0.01;
$fn = 48;

c = chamfer_on ? CHAMFER : 0;

// =============================================================
//  2D board cross-sections (in X-Z plane, extruded along Y)
// =============================================================

// --- 1. Rabbet Joint Polygons (Top/Bottom cap the Sides) ---
poly_bottom_rabbet = [
    [0, 0],
    [W, 0],
    [W, R_DEPTH],
    [W - R_WIDTH, R_DEPTH],
    [W - R_WIDTH, T],
    [R_WIDTH, T],
    [R_WIDTH, R_DEPTH],
    [0, R_DEPTH]
];

poly_top_rabbet = [
    [0, H],
    [0, H - R_DEPTH],
    [R_WIDTH, H - R_DEPTH],
    [R_WIDTH, H - T],
    [W - R_WIDTH, H - T],
    [W - R_WIDTH, H - R_DEPTH],
    [W, H - R_DEPTH],
    [W, H]
];

poly_left_rabbet = [
    [0, R_DEPTH],
    [T, R_DEPTH],
    [T, H - R_DEPTH],
    [0, H - R_DEPTH]
];

poly_right_rabbet = [
    [W - T, R_DEPTH],
    [W, R_DEPTH],
    [W, H - R_DEPTH],
    [W - T, H - R_DEPTH]
];

// --- 2. 45-degree Miter Joint Polygons ---
poly_bottom_miter = [
    [0, 0],
    [W, 0],
    [W - T, T],
    [T, T]
];

poly_top_miter = [
    [0, H],
    [T, H - T],
    [W - T, H - T],
    [W, H]
];

poly_left_miter = [
    [0, 0],
    [T, T],
    [T, H - T],
    [0, H]
];

poly_right_miter = [
    [W, 0],
    [W, H],
    [W - T, H - T],
    [W - T, T]
];

// --- 3. Butt Joint Polygons ---
poly_bottom_butt = [
    [0, 0],
    [W, 0],
    [W, T],
    [0, T]
];

poly_top_butt = [
    [0, H],
    [0, H - T],
    [W, H - T],
    [W, H]
];

poly_left_butt = [
    [0, T],
    [T, T],
    [T, H - T],
    [0, H - T]
];

poly_right_butt = [
    [W - T, T],
    [W, T],
    [W, H - T],
    [W - T, H - T]
];

// Active polygons selected by joint_type
poly_bottom = (joint_type == "rabbet") ? poly_bottom_rabbet :
              (joint_type == "miter")  ? poly_bottom_miter  :
                                         poly_bottom_butt;

poly_top    = (joint_type == "rabbet") ? poly_top_rabbet :
              (joint_type == "miter")  ? poly_top_miter  :
                                         poly_top_butt;

poly_left   = (joint_type == "rabbet") ? poly_left_rabbet :
              (joint_type == "miter")  ? poly_left_miter  :
                                         poly_left_butt;

poly_right  = (joint_type == "rabbet") ? poly_right_rabbet :
              (joint_type == "miter")  ? poly_right_miter  :
                                         poly_right_butt;


// =============================================================
//  Finishing Chamfer Cutters
// =============================================================

// Right-triangle prism cutter along X: cross section in Y-Z
module chamfer_wedge_x(x0, x1, y0, z0, dy, dz) {
    translate([x0 - EPS, 0, 0])
        rotate([0, 90, 0])
            linear_extrude(height = (x1 - x0) + 2*EPS)
                polygon([
                    [z0 - dz*EPS, y0 - dy*EPS],
                    [z0 + dz*(c + EPS), y0 - dy*EPS],
                    [z0 - dz*EPS, y0 + dy*(c + EPS)]
                ]);
}

// Right-triangle prism cutter along Z: cross section in X-Y
module chamfer_wedge_z(z0, z1, x0, y0, dx, dy) {
    translate([0, 0, z0 - EPS])
        linear_extrude(height = (z1 - z0) + 2*EPS)
            polygon([
                [x0 - dx*EPS, y0 - dy*EPS],
                [x0 + dx*(c + EPS), y0 - dy*EPS],
                [x0 - dx*EPS, y0 + dy*(c + EPS)]
            ]);
}

// Right-triangle prism cutter along Y: cross section in X-Z
module chamfer_wedge_y(y0, y1, x0, z0, dx, dz) {
    translate([0, y0 - EPS, 0])
        rotate([-90, 0, 0])
            linear_extrude(height = (y1 - y0) + 2*EPS)
                polygon([
                    [x0 - dx*EPS, -(z0 - dz*EPS)],
                    [x0 + dx*(c + EPS), -(z0 - dz*EPS)],
                    [x0 - dx*EPS, -(z0 + dz*(c + EPS))]
                ]);
}

// Chamfers around front rim (y = 0) and back rim (y = D)
module rim_chamfers() {
    if (c > 0) {
        // --- FRONT RIM (y = 0) ---
        chamfer_wedge_x(0, W, 0, 0, 1, 1);         // outer bottom (z=0, y=0)
        chamfer_wedge_x(0, W, 0, H, 1, -1);        // outer top (z=H, y=0)
        chamfer_wedge_x(T, W - T, 0, T, 1, -1);     // inner bottom (z=T, y=0)
        chamfer_wedge_x(T, W - T, 0, H - T, 1, 1);   // inner top (z=H-T, y=0)
        chamfer_wedge_z(0, H, 0, 0, 1, 1);         // outer left (x=0, y=0)
        chamfer_wedge_z(0, H, W, 0, -1, 1);        // outer right (x=W, y=0)
        chamfer_wedge_z(T, H - T, T, 0, -1, 1);     // inner left (x=T, y=0)
        chamfer_wedge_z(T, H - T, W - T, 0, 1, 1);   // inner right (x=W-T, y=0)

        // --- BACK RIM (y = D) ---
        chamfer_wedge_x(0, W, D, 0, -1, 1);
        chamfer_wedge_x(0, W, D, H, -1, -1);
        chamfer_wedge_x(T, W - T, D, T, -1, -1);
        chamfer_wedge_x(T, W - T, D, H - T, -1, 1);
        chamfer_wedge_z(0, H, 0, D, 1, -1);
        chamfer_wedge_z(0, H, W, D, -1, -1);
        chamfer_wedge_z(T, H - T, T, D, -1, -1);
        chamfer_wedge_z(T, H - T, W - T, D, 1, -1);
    }
}

// 4 long outer front-to-back arrises along Y
module corner_chamfers() {
    if (c > 0) {
        chamfer_wedge_y(0, D, 0, 0, 1, 1);     // bottom-left
        chamfer_wedge_y(0, D, 0, H, 1, -1);    // top-left
        chamfer_wedge_y(0, D, W, 0, -1, 1);    // bottom-right
        chamfer_wedge_y(0, D, W, H, -1, -1);   // top-right
    }
}

module all_chamfers() {
    rim_chamfers();
    corner_chamfers();
}

// Extrude polygon in X-Z along Y from 0 to D
module extrude_xz(pts) {
    rotate([90, 0, 0])
        translate([0, 0, -D])
            linear_extrude(height = D)
                polygon(pts);
}

// Individual board solids with finishing chamfers applied
module board_bottom_solid() {
    difference() {
        extrude_xz(poly_bottom);
        all_chamfers();
    }
}

module board_top_solid() {
    difference() {
        extrude_xz(poly_top);
        all_chamfers();
    }
}

module board_left_solid() {
    difference() {
        extrude_xz(poly_left);
        all_chamfers();
    }
}

module board_right_solid() {
    difference() {
        extrude_xz(poly_right);
        all_chamfers();
    }
}

// Colored boards
module board_bottom() { color(BIRCH) board_bottom_solid(); }
module board_top()    { color(BIRCH) board_top_solid(); }
module board_left()   { color(BIRCH_EDGE) board_left_solid(); }
module board_right()  { color(BIRCH_EDGE) board_right_solid(); }

// =============================================================
//  Leg Hardware
// =============================================================

function leg_rot_x(sy) = sy * LEG_SPLAY;
function leg_rot_y(sx) = -sx * LEG_SPLAY;

function leg_plate_cx(sx) = (sx < 0) ? LEG_INSET_X + PLATE_W/2 : W - LEG_INSET_X - PLATE_W/2;
function leg_plate_cy(sy) = (sy < 0) ? LEG_INSET_Y + PLATE_L/2 : D - LEG_INSET_Y - PLATE_L/2;

module mounting_plate() {
    difference() {
        translate([0, 0, -PLATE_T])
            linear_extrude(height = PLATE_T)
                offset(r = 0.25)
                    offset(delta = -0.25)
                        square([PLATE_W, PLATE_L], center = true);
        for (dx = [-1, 1], dy = [-1, 1]) {
            translate([dx * (PLATE_W/2 - HOLE_OS), dy * (PLATE_L/2 - HOLE_OS), -PLATE_T - EPS])
                cylinder(d = HOLE_D, h = PLATE_T + 2*EPS);
        }
    }
}

module leg_metal_part(sx, sy) {
    px = leg_plate_cx(sx);
    py = leg_plate_cy(sy);

    translate([px, py, 0]) {
        color(METAL) mounting_plate();
        color(METAL) {
            translate([0, 0, -PLATE_T])
                cylinder(h = 0.20, d = LEG_TOP_D + 0.20);
            translate([0, 0, -PLATE_T])
                rotate([leg_rot_x(sy), leg_rot_y(sx), 0])
                    translate([0, 0, -((LEG_H - PLATE_T) / cos(LEG_TILT))])
                        cylinder(h = (LEG_H - PLATE_T) / cos(LEG_TILT),
                                 d1 = LEG_BOT_D, d2 = LEG_TOP_D);
        }
    }
}

module leg_glide_part(sx, sy) {
    px = leg_plate_cx(sx);
    py = leg_plate_cy(sy);

    translate([px, py, 0]) {
        color(BRASS) {
            translate([0, 0, -PLATE_T])
                rotate([leg_rot_x(sy), leg_rot_y(sx), 0])
                    translate([0, 0, -((LEG_H - PLATE_T) / cos(LEG_TILT))])
                        cylinder(h = GLIDE_H, d = GLIDE_D);
        }
    }
}

module single_leg(sx, sy) {
    leg_metal_part(sx, sy);
    leg_glide_part(sx, sy);
}

module all_metal_legs() {
    for (sx = [-1, 1], sy = [-1, 1]) leg_metal_part(sx, sy);
}

module all_glides() {
    for (sx = [-1, 1], sy = [-1, 1]) leg_glide_part(sx, sy);
}

module all_legs() {
    all_metal_legs();
    all_glides();
}

// =============================================================
//  Assembly & Modes
// =============================================================

module carcass() {
    board_bottom();
    board_top();
    board_left();
    board_right();
}

module assembled() {
    carcass();
    if (show_legs) all_legs();
}

module exploded() {
    ez = 3.5;
    ex = 3.5;
    el = 6.0;

    translate([0, 0, -ez]) board_bottom();
    translate([0, 0,  ez]) board_top();
    translate([-ex, 0, 0]) board_left();
    translate([ ex, 0, 0]) board_right();

    if (show_legs) {
        translate([0, 0, -ez - el]) all_legs();
    }
}

// Cutting layout of continuous board blank:
// Rabbet: Left (6.25") + Top (18") + Right (6.25") + Bottom (18") = 48.5" total
module waterfall() {
    kerf = 0.125;
    side_len = (joint_type == "rabbet") ? (H - 2*(T - R_DEPTH)) :
               (joint_type == "butt")   ? (H - 2*T) : H;
    color(BIRCH) translate([0, 0, 0]) cube([side_len, D, T]);
    color(BIRCH) translate([side_len + kerf, 0, 0]) cube([W, D, T]);
    color(BIRCH) translate([side_len + kerf + W + kerf, 0, 0]) cube([side_len, D, T]);
    color(BIRCH) translate([side_len + kerf + W + kerf + side_len + kerf, 0, 0]) cube([W, D, T]);
}

// Close up on top-left joint detail
module joint_detail() {
    sep = 0.8;
    translate([0, 0, 0]) {
        translate([-sep, 0, 0]) board_left();
        translate([0, 0, sep]) board_top();
    }
}

// =============================================================
//  Root selection & scaling
// =============================================================

scale(UNIT) {
    if (mode == "assembled")                                    assembled();
    else if (mode == "exploded")                                exploded();
    else if (mode == "carcass")                                 carcass();
    else if (mode == "waterfall")                               waterfall();
    else if (mode == "joint" || mode == "miter_joint" || mode == "rabbet_joint") joint_detail();
}
