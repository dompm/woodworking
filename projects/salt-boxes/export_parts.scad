// Export individual parts of the salt boxes for Blender Cycles beauty renders.
//
// Drive from the command line:
//   openscad -o out.stl -D 'mode="none"' -D 'PART="short_lid"' export_parts.scad

include <salt_box.scad>

PART = "short_bottom";
SWING_SHORT = 80;
SWING_TALL  = 0;

DX = 3.90;
DY = 0.70;

module layer_mid() {
    difference() {
        linear_extrude(T_MID) outer_2d();
        translate([0, 0, -EPS]) linear_extrude(T_MID + 2*EPS) cavity_2d();
    }
}

module box_part(part_name, layers, dx=0, dy=0, swing=0) {
    body_h = T_CAP + layers*T_MID;
    translate([dx, dy, 0]) {
        if (part_name == "bottom") {
            bottom();
        } else if (part_name == "mid0") {
            translate([0, 0, T_CAP]) layer_mid();
        } else if (part_name == "mid1") {
            translate([0, 0, T_CAP + T_MID]) layer_mid();
        } else if (part_name == "mid2" && layers > 2) {
            translate([0, 0, T_CAP + 2*T_MID]) layer_mid();
        } else if (part_name == "lid") {
            translate([0, 0, body_h + EPS])
                translate([PIVOT_IN, PIVOT_IN, 0])
                    rotate([0, 0, swing])
                        translate([-PIVOT_IN, -PIVOT_IN, 0])
                            lid();
        } else if (part_name == "brass") {
            translate([PIVOT_IN, PIVOT_IN, body_h - 0.5])
                cylinder(h = 0.5 + T_CAP, d = PIVOT_D - SHRNK, $fn = 32);
            translate([PIVOT_IN, PIVOT_IN, body_h + T_CAP])
                cylinder(h = 0.07, d = PIVOT_D*2.1, $fn = 32);
        } else if (part_name == "steel") {
            // Steel strike plate in box rim
            translate([SIZE - MAG_IN, SIZE - MAG_IN, body_h - MAG_H])
                cylinder(h = MAG_H, d = MAG_D - SHRNK, $fn = 48);
            // Magnet in lid
            translate([0, 0, body_h + EPS])
                translate([PIVOT_IN, PIVOT_IN, 0])
                    rotate([0, 0, swing])
                        translate([-PIVOT_IN, -PIVOT_IN, 0])
                            translate([SIZE - MAG_IN, SIZE - MAG_IN, -EPS])
                                cylinder(h = MAG_H, d = MAG_D - SHRNK, $fn = 48);
        }
    }
}

scale(UNIT) {
    if      (PART == "short_bottom") box_part("bottom", 2, 0, 0, SWING_SHORT);
    else if (PART == "short_mid0")   box_part("mid0",   2, 0, 0, SWING_SHORT);
    else if (PART == "short_mid1")   box_part("mid1",   2, 0, 0, SWING_SHORT);
    else if (PART == "short_lid")    box_part("lid",    2, 0, 0, SWING_SHORT);
    else if (PART == "short_brass")  box_part("brass",  2, 0, 0, SWING_SHORT);
    else if (PART == "short_steel")  box_part("steel",  2, 0, 0, SWING_SHORT);
    else if (PART == "tall_bottom")  box_part("bottom", 3, DX, DY, SWING_TALL);
    else if (PART == "tall_mid0")    box_part("mid0",   3, DX, DY, SWING_TALL);
    else if (PART == "tall_mid1")    box_part("mid1",   3, DX, DY, SWING_TALL);
    else if (PART == "tall_mid2")    box_part("mid2",   3, DX, DY, SWING_TALL);
    else if (PART == "tall_lid")     box_part("lid",    3, DX, DY, SWING_TALL);
    else if (PART == "tall_brass")   box_part("brass",  3, DX, DY, SWING_TALL);
    else if (PART == "tall_steel")   box_part("steel",  3, DX, DY, SWING_TALL);
}
