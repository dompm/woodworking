// Concept envelope, not a mounting/drilling template. Select the actual plate
// and jig before fixing the recess, slot, mounting screws, or guard clearances.
UNIT=25.4;
PART="all";
W=26; D=22; Z=14; TOP=1.5;
PX=13; PY=13; PW=11.75; PD=8.25; PT=.375;
$fn=48;
module structure() {
 difference() {
  translate([0,0,Z]) cube([W,D,TOP]);
  translate([PX-PW/2,PY-PD/2,Z-.01]) cube([PW,PD,TOP+.02]);
  translate([-.01,6.75,Z+TOP-.375]) cube([W+.02,.75,.4]);
 }
 // Two side panels, broad feet and a rear brace leave motor access open.
 for(x=[1,24.25]) {
  translate([x,2,.75]) cube([.75,18,Z-.75]);
  translate([x-.75,0,0]) cube([2.25,D,.75]);
 }
 translate([1.75,19,5]) cube([22.5,.75,6]);
 // Plate support frame: illustrative continuous ledge, positively retained
 // using the selected plate's own hardware (fastener locations not guessed).
 difference() {
  translate([PX-PW/2-.5,PY-PD/2-.5,Z+.625]) cube([PW+1,PD+1,.5]);
  translate([PX-PW/2+.375,PY-PD/2+.375,Z+.6]) cube([PW-.75,PD-.75,.6]);
 }
}
module plate() {
 difference() {
  translate([PX-PW/2,PY-PD/2,Z+TOP-PT]) cube([PW,PD,PT]);
  translate([PX,PY,Z+TOP-PT-.01]) cylinder(d=1,h=PT+.02);
 }
}
module fence() {
 difference() {
  translate([1,PY+.2,Z+TOP]) cube([24,.75,3.5]);
  translate([PX-.65,PY+.19,Z+TOP-.01]) cube([1.3,.78,1.4]);
 }
 translate([1,PY+.95,Z+TOP]) cube([24,3,.5]);
}
module router() {
 translate([PX,PY,Z+TOP-1]) cylinder(d=6,h=.6);
 translate([PX,PY,Z-8]) cylinder(d=3.8,h=7.5);
 for(x=[PX-3.5,PX+2.5])translate([x,PY-.5,Z-2])cube([1,1,1.5]);
}
module guard() { translate([PX-1.1,PY-2,Z+TOP+1.4]) cube([2.2,3,.125]); }
module controls() { translate([1,1.25,8])cube([2.5,1,3]); }
module clamps() {
 for(x=[1,25]) {
  translate([x-.3,-.5,-1])cube([.6,.5,3]);
  translate([x-.3,-.5,1.5])cube([.6,2,.3]);
  translate([x-.3,-.5,-1])cube([.6,2,.3]);
 }
}
scale(UNIT) {
 if(PART=="all" || PART=="structure")color("burlywood")structure();
 if(PART=="all" || PART=="plate")color("gray")plate();
 if(PART=="all" || PART=="fence")color("burlywood")fence();
 if(PART=="all" || PART=="router")color("teal")router();
 if(PART=="all" || PART=="guard")color([.7,.9,1,.3])guard();
 if(PART=="all" || PART=="controls")color("red")controls();
 if(PART=="all" || PART=="clamps")color("orange")clamps();
}
