// =============================================================
//  Plant stand -- crossed rails, four legs running past the disc
//
//  The clever part is where the legs sit: at the ENDS of a crossed pair of
//  rails, not at the corners of a square.  Each leg then leans outward in the
//  plane of its own rail, which is a SINGLE bevel.  Legs at the corners of a
//  square have to lean toward the corner, which is a compound angle and a
//  different class of problem.  That one choice is what makes this buildable.
//
//  Everything else is joinery already in this repo:
//      - the two rails cross in a half lap, the egg-crate joint
//      - the rails are housed into the legs, the same housing as a shelf
//      - the disc just sits on the cross
//
//  The legs continue above the disc and become a cradle, so the pot cannot
//  slide off -- the ring idea done with four posts instead of a closed ring,
//  and no big circle to cut.
//
//      openscad cradle_stand.scad
//      openscad -D 'mode="exploded"' cradle_stand.scad
// =============================================================
UNIT = 25.4;

mode = "assembled";   // assembled | exploded | parts | none

// ---------------- stock
T = 0.75;

// ---------------- overall
H_TOP  = 16.00;      // floor to the top of the legs
DISC_Z =  9.50;      // floor to the TOP of the disc -- the pot stands here
DISC_D =  8.00;

// ---------------- rails
RAIL_W = 1.50;       // how deep the rail is, seen from the side
RAIL_T = T;          // its thickness

// ---------------- legs
LEG_W   = 1.50;      // square, at the rail
LEG_END = 1.00;      // at both ends -- widest at the waist, like the photo
LEG_R   = 5.00;      // radius to the leg's centre, at rail height
SPLAY   = 5;         // degrees the legs lean out.  Single bevel, not compound.

HOUSING = 0.625;     // how far the rail is let into the leg

LAP_FIT = 0.004;     // clearance in the half lap -- a real shop tolerance, and
                     // it keeps the two rails off exactly coincident faces
EPS = 0.01;

WOOD  = "#5b3a24";
WOOD2 = "#6b4630";
DISC  = "#63412a";

// ---------------- derived
Z_RAIL = DISC_Z - T - RAIL_W/2;          // centre of the rails
LEN_DN = Z_RAIL / cos(SPLAY) + 0.6;      // down the leg, past the floor
LEN_UP = (H_TOP - Z_RAIL) / cos(SPLAY);  // up the leg
RAIL_L = 2 * (LEG_R - LEG_W/2 + HOUSING);

// =============================================================
//  parts
// =============================================================
module sec(w, z) { translate([-w/2, -w/2, z]) cube([w, w, EPS]); }

// leg in its own frame: z runs along the leg, 0 at the rail
module leg_solid() {
    hull() { sec(LEG_W, 0); sec(LEG_END, -LEN_DN); }
    hull() { sec(LEG_W, 0); sec(LEG_END,  LEN_UP); }
}

// put children where leg i lives, tilted by SPLAY
module at_leg(i) {
    rotate([0, 0, i * 90])
        translate([LEG_R, 0, Z_RAIL])
            rotate([0, -SPLAY, 0])
                children();
}

// One rail running in x, before the half lap is cut.
module rail_blank() {
    translate([-RAIL_L/2, -RAIL_T/2, Z_RAIL - RAIL_W/2])
        cube([RAIL_L, RAIL_T, RAIL_W]);
}

// i = 0 notched on TOP, i = 1 notched underneath, so they interlock
module rail(i) {
    rotate([0, 0, i * 90])
        difference() {
            rail_blank();
            translate([-RAIL_T/2 - LAP_FIT, -RAIL_T/2 - EPS,
                       i == 0 ? Z_RAIL - LAP_FIT : Z_RAIL - RAIL_W/2 - EPS])
                cube([RAIL_T + 2*LAP_FIT, RAIL_T + 2*EPS,
                      RAIL_W/2 + LAP_FIT + EPS]);
        }
}

module rails() { for (i = [0, 1]) rail(i); }

// the legs, with the rail housings cut out of them
module legs() {
    difference() {
        for (i = [0 : 3]) at_leg(i) leg_solid();
        for (i = [0, 1]) rotate([0, 0, i * 90]) rail_blank();
    }
}

module disc() {
    translate([0, 0, DISC_Z - T]) linear_extrude(T) circle(d = DISC_D, $fn = 160);
}

// =============================================================
//  assembly.  Trimmed at the floor so the feet sit flat -- a splayed leg
//  cut square to its own axis stands on an edge and the whole thing rocks.
// =============================================================
module stand(explode = 0) {
    intersection() {
        union() {
            color(WOOD)  legs();
            color(WOOD2) translate([0, 0, explode * 2.2]) rails();
            color(DISC)  translate([0, 0, explode * 4.0]) disc();
        }
        translate([-40, -40, 0]) cube([80, 80, 80]);
    }
}

scale(UNIT) {
    if (mode == "assembled")     stand(0);
    else if (mode == "exploded") stand(1);
    else if (mode == "parts") {
        color(DISC) linear_extrude(T) circle(d = DISC_D, $fn = 160);
        color(WOOD2) translate([DISC_D/2 + 2, 0, 0]) rotate([0, 0, 0]) rail(0);
    }
}

echo(str("overall             = ", H_TOP, " tall, legs spread ",
         2*(LEG_R + Z_RAIL*tan(SPLAY)), " at the floor"));
echo(str("disc                = ", DISC_D, " dia x ", T, ", top at ", DISC_Z));
echo(str("legs stand proud    = ", H_TOP - DISC_Z, " above the disc"));
echo(str("clear between legs  = ", 2*(LEG_R - (DISC_Z - Z_RAIL)*tan(SPLAY)) - LEG_W,
         " at the disc, closing to ",
         2*(LEG_R - (H_TOP - Z_RAIL)*tan(SPLAY)) - LEG_W, " at the top"));
echo(str("rail                = ", RAIL_L, " x ", RAIL_W, " x ", RAIL_T,
         "  x2, half lapped"));
echo(str("leg                 = ", LEG_W, " sq at the waist, ", LEG_END,
         " at both ends"));
echo(str("splay               = ", SPLAY, " deg -- single bevel"));
