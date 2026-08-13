// =============================================================
//  Plant stands -- ring top, two designs
//
//  STAND = "four"  square top, four tapered legs, aprons.  No angled joinery
//                  anywhere: the legs stand plumb and the taper does the work.
//
//  STAND = "three" round top, three legs splayed outward.  Harder, and the
//                  reason it is possible at all is the compound mitre saw --
//                  set bevel AND mitre, cut the leg's top once, and it mates
//                  flat against a horizontal underside.  That is the whole
//                  trick; without it, splayed square legs need hand-cut
//                  compound angles.
//
//  The pot NESTS in the opening and hangs by its rim, so the stand carries the
//  pot's weight in shear at the ring rather than in bending across a top.
//  Which means the ring can be thin and still strong.
//
//      openscad plant_stand.scad
//      openscad -D 'STAND="three"' -D HEIGHT=14 plant_stand.scad
// =============================================================
UNIT = 25.4;

STAND = "four";      // four | three
mode  = "assembled"; // assembled | exploded | parts | none

// ---------------- stock
T = 0.75;

// ---------------- overall
HEIGHT = 18.00;      // floor to the top surface
POT_D  = 6.00;       // the opening.  A 6" nursery pot has a ~6-1/2" rim, so
                     // it drops in and hangs -- measure YOUR pots, this is the
                     // one dimension the whole thing is built around.
TOP_W  = 12.00;      // square side (four) or diameter (three)
TOP_R  = 0.75;       // corner radius on the square top

// ---------------- legs
LEG_TOP = 1.50;      // square at the top
LEG_BOT = 0.875;     // at the foot -- tapered on all four faces
LEG_IN  = 1.00;      // outer face, in from the edge of the top

// ---------------- four-leg version
APRON_H   = 2.00;    // apron depth
APRON_T   = T;
APRON_REC = 0.375;   // apron face set back from the leg's outer face
APRON_DAD = 0.25;    // housed this deep into the leg

// ---------------- three-leg version
SPLAY  = 9;          // degrees the legs lean out
LEG_R  = 3.60;       // radius to the leg centre at the top
BLOCK  = 1.00;       // glue block in the inner corner
BLOCK_H = 1.25;

EPS = 0.01;

WOOD  = "#7a4f2e";
WOOD2 = "#8a5c38";

// =============================================================
//  shared
// =============================================================
module ring_2d() {
    difference() {
        if (STAND == "three") circle(d = TOP_W, $fn = 160);
        else translate([TOP_R, TOP_R])
                offset(r = TOP_R, $fn = 64) square(TOP_W - 2*TOP_R);
        translate(STAND == "three" ? [0, 0] : [TOP_W/2, TOP_W/2])
            circle(d = POT_D, $fn = 120);
    }
}

module top_ring() {
    translate([0, 0, HEIGHT - T]) linear_extrude(T) ring_2d();
}

// A leg standing on the origin, big end up, tapering to the foot.
module leg(h) {
    hull() {
        translate([-LEG_TOP/2, -LEG_TOP/2, h - EPS]) cube([LEG_TOP, LEG_TOP, EPS]);
        translate([-LEG_BOT/2, -LEG_BOT/2, 0])       cube([LEG_BOT, LEG_BOT, EPS]);
    }
}

// =============================================================
//  four: square top, plumb tapered legs, housed aprons
// =============================================================
LEG_C = LEG_IN + LEG_TOP/2;              // leg centre, in from the top's edge
SPAN  = TOP_W - 2*LEG_C;                 // centre to centre

module four_legs() {
    for (sx = [0, 1], sy = [0, 1])
        translate([LEG_C + sx*SPAN, LEG_C + sy*SPAN, 0])
            leg(HEIGHT - T);
}

// One apron, running in x, at y.  Housed into the legs at each end.
module apron_x(y) {
    x0 = LEG_C - LEG_TOP/2 + LEG_TOP - APRON_DAD;
    x1 = LEG_C + SPAN + LEG_TOP/2 - LEG_TOP + APRON_DAD;
    translate([x0, y - APRON_T/2, HEIGHT - T - APRON_H - 0.25])
        cube([x1 - x0, APRON_T, APRON_H]);
}

module four_aprons() {
    yin = LEG_C - LEG_TOP/2 + APRON_REC + APRON_T/2;
    for (y = [yin, TOP_W - yin]) apron_x(y);
    for (x = [yin, TOP_W - yin])
        translate([x, 0, 0]) rotate([0, 0, 90]) translate([0, -TOP_W, 0])
            apron_x(TOP_W - x < 0 ? 0 : 0);
}

// simpler: build the two y-running aprons by rotating the whole x pair
module four_aprons_all() {
    yin = LEG_C - LEG_TOP/2 + APRON_REC + APRON_T/2;
    for (y = [yin, TOP_W - yin]) apron_x(y);
    translate([TOP_W, 0, 0]) rotate([0, 0, 90])
        for (y = [yin, TOP_W - yin]) apron_x(y);
}

module stand_four(explode = 0) {
    color(WOOD)  translate([0, 0, explode*3]) top_ring();
    color(WOOD2) four_legs();
    color(WOOD)  translate([0, 0, explode*1.4]) four_aprons_all();
}

// =============================================================
//  three: round top, splayed legs, glue blocks
// =============================================================
module three_legs() {
    for (a = [0 : 120 : 359])
        rotate([0, 0, a])
            translate([LEG_R, 0, HEIGHT - T])
                rotate([0, -SPLAY, 0])   // negative: foot moves OUTWARD
                    translate([0, 0, -(HEIGHT - T)])
                        leg(HEIGHT - T);
}

// blocks in the inner corner, the same trick the scandinavian wine rack uses
module three_blocks() {
    for (a = [0 : 120 : 359])
        rotate([0, 0, a])
            translate([LEG_R - LEG_TOP/2 - BLOCK, -BLOCK/2, HEIGHT - T - BLOCK_H])
                cube([BLOCK, BLOCK, BLOCK_H]);
}

module stand_three(explode = 0) {
    color(WOOD)  translate([0, 0, explode*3]) top_ring();
    color(WOOD2) three_legs();
    color(WOOD)  three_blocks();
}

// =============================================================
scale(UNIT) {
    if (mode == "assembled") {
        if (STAND == "three") stand_three(0); else stand_four(0);
    } else if (mode == "exploded") {
        if (STAND == "three") stand_three(1); else stand_four(1);
    } else if (mode == "parts") {
        color(WOOD) linear_extrude(T) ring_2d();
        color(WOOD2) translate([TOP_W + 3, 0, 0]) leg(HEIGHT - T);
    }
}

echo(str("stand               = ", STAND));
echo(str("height              = ", HEIGHT, " to the top surface"));
echo(str("top                 = ", TOP_W,
         STAND == "three" ? " dia" : " square", " x ", T));
echo(str("opening             = ", POT_D, "  -> takes a pot with a rim wider than this"));
echo(str("ring width          = ", (TOP_W - POT_D)/2, " all round"));
echo(str("leg                 = ", LEG_TOP, " sq tapering to ", LEG_BOT));
if (STAND == "four")
    echo(str("apron               = ", APRON_H, " deep, housed ", APRON_DAD,
             " into the legs"));
else
    echo(str("splay               = ", SPLAY, " deg  -> feet spread ",
             2*(LEG_R + (HEIGHT-T)*tan(SPLAY)), " across"));
