// Export individual parts of the bedside table for Blender Cycles beauty renders.
//
// Drive from the command line:
//   openscad -o out.stl -D 'mode="none"' -D 'PART="top"' export_parts.scad

include <bedside_table.scad>

PART = "top";

scale(UNIT) {
    if      (PART == "top")    board_top();
    else if (PART == "bottom") board_bottom();
    else if (PART == "left")   board_left();
    else if (PART == "right")  board_right();
    else if (PART == "legs")   all_metal_legs();
    else if (PART == "glides") all_glides();
}



