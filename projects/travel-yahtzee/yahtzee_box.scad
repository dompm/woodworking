// Inches internally; millimetres at the output, as elsewhere in this repo.
UNIT = 25.4;
joinery = "finger"; // finger | butt
track = "groove";   // groove | strips
mode = "open";      // open | closed | exploded | section | export | manifest
PART = 0;
SHOW_CONTENTS = true;

T = 0.25;
BASE = 0.25;
LID = 0.125;
PAPER_W = 4;
PAPER_L = 6;
PAPER_H = 4/25.4;
PAPER_CLEAR = 4/25.4;
DIE = 15/25.4;
PENCIL_L = 99.1/25.4;
PENCIL_D = 5.6/25.4;
DICE_BAY = 22/25.4;
PENCIL_BAY = 12/25.4;
FINGER = 0.25;
GROOVE_DEPTH = 0.125;
SLIDE_CLEAR = 0.2/25.4; // each side, including above/below the lid
RAIL = 0.25;
EPS = 0.001;

PAD_W = PAPER_W + PAPER_CLEAR;
PAD_L = PAPER_L + PAPER_CLEAR;
MARGIN = T + (track == "strips" ? RAIL : 0);
W = PAD_W + 2*MARGIN;
L = PAD_L + 2*T + 2*T + DICE_BAY + PENCIL_BAY;
// Front height is three complete fingers. Side/back have a substantial lip
// above the thin lid; the last back finger is partial, never a sliver.
FRONT_H = 3*FINGER;
LID_Z = BASE + FRONT_H + SLIDE_CLEAR;
SLOT_Z = BASE + FRONT_H;
SLOT_H = LID + 2*SLIDE_CLEAR;
H = SLOT_Z + SLOT_H + T;
SIDE_H = H - BASE;
LOWER_Z = SLOT_Z - RAIL;
UPPER_Z = SLOT_Z + SLOT_H;
DIV_H = FRONT_H - 0.04;
DICE_Y = L-T-DICE_BAY;
DIV1_Y = DICE_Y-T;
PENCIL_Y = DIV1_Y-PENCIL_BAY;
DIV2_Y = PENCIL_Y-T;
PAPER_Y = T + PAPER_CLEAR/2;
LID_X = track == "groove" ? T-GROOVE_DEPTH+SLIDE_CLEAR : T+SLIDE_CLEAR;
LID_W = W-2*LID_X;
LID_L = L-T-SLIDE_CLEAR;
END_X = joinery == "butt" ? T : 0;
END_W = W-2*END_X;
PIP_R = 1.1/25.4;
$fn=32;

assert(joinery=="finger" || joinery=="butt");
assert(track=="groove" || track=="strips");
assert(T-GROOVE_DEPTH >= 0.1, "Insufficient wood behind the lid groove");
assert(DIE+0.03 < FRONT_H, "Dice hit the lid");
assert(PENCIL_L+4/25.4 < PAD_W, "Pencil needs more end clearance");
assert(2*T+PENCIL_D+0.02 < FRONT_H, "Raised pencil hits the lid");
assert(PAPER_H < FRONT_H, "Score stack hits the lid");
assert(5*DIE+4*3/25.4 < PAD_W, "Five dice do not fit the row");
assert(DIV_H > FRONT_H-PENCIL_D, "Pencil can cross a divider with lid closed");

// [name, lower corner, blank size, material, grain / plywood thickness axis].
// Both the cut list and Blender's part positions come from these records.
wood_parts = [
 ["base",[0,0,0],[W,L,BASE],"ply","Z"],
 ["left",[0,0,BASE],[T,L,SIDE_H],"wall","X"],
 ["right",[W-T,0,BASE],[T,L,SIDE_H],"wall","X"],
 ["front",[END_X,0,BASE],[END_W,T,FRONT_H],"wall","Y"],
 ["back",[END_X,L-T,BASE],[END_W,T,SIDE_H],"wall","Y"],
 ["dice_divider",[T,DIV1_Y,BASE],[W-2*T,T,DIV_H],"ply","Y"],
 ["pencil_divider",[T,DIV2_Y,BASE],[W-2*T,T,DIV_H],"ply","Y"],
 ["lid",[LID_X,0,LID_Z],[LID_W,LID_L,LID],"ply","Z"],
 // Raise the very slim pencil so it can be reached through the finger scoop.
 // Two stock-thickness laminations avoid a special thicknessing operation.
 ["pencil_riser_bottom",[T,PENCIL_Y,BASE],[W-2*T,PENCIL_BAY,T],"ply","Z"],
 ["pencil_riser_top",[T,PENCIL_Y,BASE+T],[W-2*T,PENCIL_BAY,T],"ply","Z"]
];
rail_parts = track=="strips" ? [
 ["lower_left",[T,T,LOWER_Z],[RAIL,L-2*T,RAIL],"rail","Y"],
 ["lower_right",[W-T-RAIL,T,LOWER_Z],[RAIL,L-2*T,RAIL],"rail","Y"],
 ["upper_left",[T,0,UPPER_Z],[RAIL,L-T,T],"rail","Y"],
 ["upper_right",[W-T-RAIL,0,UPPER_Z],[RAIL,L-T,T],"rail","Y"]
] : [];
function dice_x(i)=MARGIN+(PAD_W-(5*DIE+4*3/25.4))/2+i*(DIE+3/25.4);
content_parts = concat([
 ["scorepad",[MARGIN+PAPER_CLEAR/2,PAPER_Y,BASE],[PAPER_W,PAPER_L,PAPER_H],"paper","Z"],
 ["pencil",[MARGIN+(PAD_W-PENCIL_L)/2,PENCIL_Y+PENCIL_BAY/2,BASE+2*T+PENCIL_D/2],[PENCIL_L,PENCIL_D,PENCIL_D],"pencil","X"]
], [for(i=[0:4]) [str("die",i+1),[dice_x(i),DICE_Y+(DICE_BAY-DIE)/2,BASE],[DIE,DIE,DIE],"ivory","Z"]],
 [for(i=[0:4]) [str("pips",i+1),[dice_x(i),DICE_Y+(DICE_BAY-DIE)/2,BASE],[DIE,DIE,DIE],"ink","Z"]]);
parts = concat(wood_parts,rail_parts,content_parts);

module block(size) { cube(size); }
module corner_removals(is_side, corner_h, x, y) {
 for(k=[0:ceil(corner_h/FINGER)-1])
  if((k%2==1 && is_side) || (k%2==0 && !is_side))
   translate([x-EPS,y-EPS,BASE+k*FINGER])
    cube([T+2*EPS,T+2*EPS,min(FINGER,corner_h-k*FINGER)+EPS]);
}
module side_wall(right=false) {
 x=right?W-T:0;
 difference() {
  translate([x,0,BASE]) cube([T,L,SIDE_H]);
  if(joinery=="finger") {
   corner_removals(true,FRONT_H,x,0);
   corner_removals(true,SIDE_H,x,L-T);
  }
  // Stop before the rear corner joinery. The lid's back corners are rounded
  // to match the cutter, rather than silently demanding square stopped cuts.
  if(track=="groove") translate([right?W-T-EPS:T-GROOVE_DEPTH, -EPS,SLOT_Z])
   cube([GROOVE_DEPTH+EPS,L-T+EPS,SLOT_H]);
 }
}
module end_wall(back=false) {
 yy=back?L-T:0; hh=back?SIDE_H:FRONT_H;
 difference() {
  translate([END_X,yy,BASE]) cube([END_W,T,hh]);
  if(joinery=="finger") for(xx=[0,W-T]) corner_removals(false,hh,xx,yy);
 }
}
module divider(y, scoop=false) {
 difference() {
  translate([T,y,BASE]) cube([W-2*T,T,DIV_H]);
  if(track=="strips") for(xx=[T,W-T-RAIL])
   translate([xx-EPS,y-EPS,LOWER_Z-EPS]) cube([RAIL+2*EPS,T+2*EPS,RAIL+2*EPS]);
  if(scoop) translate([W/2,y-EPS,BASE+DIV_H]) rotate([-90,0,0]) cylinder(r=0.3,h=T+2*EPS);
 }
}
module lid() {
 difference() {
  translate([LID_X,0,LID_Z]) cube([LID_W,LID_L,LID]);
  translate([W/2,0,LID_Z-EPS]) cylinder(r=0.32,h=LID+2*EPS);
  // A small plan chamfer clears the rounded end left by a narrow groove bit.
  for(xx=[LID_X,LID_X+LID_W]) translate([xx,LID_L,LID_Z-EPS])
   linear_extrude(LID+2*EPS) polygon(xx<W/2?[[0,0],[0,-0.08],[0.08,0]]:[[0,0],[0,-0.08],[-0.08,0]]);
 }
}
function pip_pattern(n)=n==1?[[.5,.5]]:n==2?[[.27,.27],[.73,.73]]:n==3?[[.27,.27],[.5,.5],[.73,.73]]:n==4?[[.27,.27],[.73,.27],[.27,.73],[.73,.73]]:[[.27,.27],[.73,.27],[.5,.5],[.27,.73],[.73,.73]];
module die(n, ink=false) {
 p=parts[len(wood_parts)+len(rail_parts)+2+n-1][1];
 translate(p) {
  if(!ink) difference() {
   hull() for(xx=[0.045,DIE-0.045],yy=[0.045,DIE-0.045],zz=[0.045,DIE-0.045])
    translate([xx,yy,zz]) sphere(r=0.045,$fn=12);
   for(pt=pip_pattern(n)) translate([DIE*pt[0],DIE*pt[1],DIE-.025]) cylinder(r=PIP_R,h=.04);
   for(pt=pip_pattern(6-n)) translate([DIE*pt[0],-.01,DIE*pt[1]]) rotate([-90,0,0]) cylinder(r=PIP_R,h=.035);
  }
  else {
   for(pt=pip_pattern(n)) translate([DIE*pt[0],DIE*pt[1],DIE-.026]) cylinder(r=PIP_R*.95,h=.006);
   for(pt=pip_pattern(6-n)) translate([DIE*pt[0],.018,DIE*pt[1]]) rotate([-90,0,0]) cylinder(r=PIP_R*.95,h=.006);
  }
 }
}
module pencil() {
 p=content_parts[1][1];
 translate(p) {
  rotate([0,90,0]) cylinder(d1=.025,d2=PENCIL_D,h=.25,$fn=24);
  translate([.25,0,0]) rotate([0,90,0]) cylinder(d=PENCIL_D,h=PENCIL_L-.4,$fn=6);
  translate([PENCIL_L-.15,0,0]) rotate([0,90,0]) cylinder(d=PENCIL_D*.65,h=.15,$fn=24);
  translate([PENCIL_L-0.65,-PENCIL_D/2-0.025,PENCIL_D*.2]) cube([.55,.035,.04]);
 }
}
module part(i) {
 n=parts[i][0];
 if(n=="left") side_wall(false);
 else if(n=="right") side_wall(true);
 else if(n=="front") end_wall(false);
 else if(n=="back") end_wall(true);
 else if(n=="dice_divider") divider(DIV1_Y);
 else if(n=="pencil_divider") divider(DIV2_Y,true);
 else if(n=="lid") lid();
 else if(n=="pencil") pencil();
 else if(i>=len(wood_parts)+len(rail_parts)+2 && i<len(wood_parts)+len(rail_parts)+7) die(i-len(wood_parts)-len(rail_parts)-1);
 else if(i>=len(wood_parts)+len(rail_parts)+7) die(i-len(wood_parts)-len(rail_parts)-6,true);
 else translate(parts[i][1]) block(parts[i][2]);
}
module assembly() {
 for(i=[0:len(parts)-1]) if(SHOW_CONTENTS || i<len(wood_parts)+len(rail_parts)) {
  mat=parts[i][3];
  color(mat=="paper"?"ivory":mat=="ink"?"#242424":mat=="ivory"?"#eee5ce":mat=="pencil"?"silver":"#ccad7b")
   translate(parts[i][0]=="lid" ? (mode=="open"?[W+0.5,0,-LID_Z]:mode=="exploded"?[0,0,1.4]:[0,0,0]) : [0,0,0]) part(i);
 }
}
if(mode=="manifest") {
 echo(["dimensions",W,L,H,PAD_W,PAD_L,FRONT_H,GROOVE_DEPTH,SLOT_H]);
 for(i=[0:len(parts)-1]) echo(concat([i],parts[i]));
} else scale(UNIT) {
 if(mode=="export") part(PART);
 else if(mode=="collisions") union() {
  for(i=[0:len(wood_parts)+len(rail_parts)-2],j=[i+1:len(wood_parts)+len(rail_parts)-1])
   intersection() { part(i);part(j); }
 }
 else if(mode=="section") difference() { assembly(); translate([W/2,-1,-1]) cube([W,L+2,H+4]); }
 else if(mode=="open" || mode=="closed" || mode=="exploded") assembly();
}
