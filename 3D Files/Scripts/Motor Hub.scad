$fn = 64;

difference(){
    cylinder(20, 8, 8);
    translate([0, 0, 5])rotate([0,90,0])#cylinder(8, 2, 2);
    cylinder(10, 4, 4);
}