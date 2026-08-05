// Export one part of the coffee table at a time, so the renderer can treat
// each board as its own object and give it its own grain.
//
// Drive it from the command line, and set mode="none" so including the main
// model does not also draw the whole table:
//
//   openscad -o out.stl -D 'mode="none"' \
//            -D 'PART="leg"' -D 'PART_I=0' export_parts.scad
//
// PART is one of: top | rail | xrail | leg | shelf | tenons | buttons

include <coffee_table.scad>

PART   = "leg";
PART_I = 0;

// leg index 0..3 -> corner (sx, sy)
LEG_CORNER = [[-1, -1], [-1, 1], [1, -1], [1, 1]];
SIDE       = [-1, 1];

scale(UNIT) {
    if      (PART == "top")     top();
    else if (PART == "rail")    long_rail(SIDE[PART_I]);
    else if (PART == "xrail")   cross_rail_cut(SIDE[PART_I]);
    else if (PART == "leg")     leg(LEG_CORNER[PART_I][0], LEG_CORNER[PART_I][1]);
    else if (PART == "shelf")   shelf();
    else if (PART == "tenons")  tenons();
    else if (PART == "buttons") buttons();
}
