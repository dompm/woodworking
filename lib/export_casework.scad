// Export one part of the rack at a time, so the renderer can treat each board
// as its own object and give it its own grain.
//
// Drive it from the command line, and set mode="none" so including the main
// model does not also draw the whole assembly:
//
//   openscad -o out.stl -D 'mode="none"' \
//            -D 'PART="stile"' -D 'PART_I=0' lib/export_casework.scad
//
// PART is one of: stile | horiz | divider | leg | brass | steel | bottles

include <casework.scad>

PART   = "stile";
PART_I = 0;

// leg index 0..3 -> corner (sx, sy)
LEG_CORNER = [[-1, -1], [-1, 1], [1, -1], [1, 1]];

module leg_plate(sx, sy) {
    px = (sx < 0) ? MOUNT_INSET : W - MOUNT_INSET - MOUNT_XY;
    py = (sy < 0) ? MOUNT_INSET : DEPTH - MOUNT_INSET - MOUNT_XY;
    if (PLATED) {
        translate([px, py, -PLATE_T]) cube([MOUNT_XY, MOUNT_XY, PLATE_T]);
        intersection() {
            at_leg(sx, sy) cylinder(h = 3, d = LEG_TOP_D);
            translate([-60, -60, -60 - PLATE_T]) cube([120, 120, 60]);
        }
    } else {
        difference() {
            translate([px, py, -MOUNT_H]) cube([MOUNT_XY, MOUNT_XY, MOUNT_H]);
            at_leg(sx, sy) leg_tenon(0.03, 0.2);
        }
    }
}

scale(UNIT) {
    if      (PART == "stile")   stile(PART_I);
    else if (PART == "horiz")   horizontal(PART_I);
    else if (PART == "divider") dividers(PART_I);
    else if (PART == "leg")
        if (SQUARE) leg_square(LEG_CORNER[PART_I][0], LEG_CORNER[PART_I][1]);
        else        leg_wood(LEG_CORNER[PART_I][0], LEG_CORNER[PART_I][1]);
    else if (PART == "blocks")
        for (k = [0 : 3]) leg_blocks(LEG_CORNER[k][0], LEG_CORNER[k][1]);
    else if (PART == "brass")
        for (k = [0 : 3]) leg_ferrule(LEG_CORNER[k][0], LEG_CORNER[k][1]);
    else if (PART == "steel")
        for (k = [0 : 3]) leg_plate(LEG_CORNER[k][0], LEG_CORNER[k][1]);
    else if (PART == "bottles") bottles();
}
