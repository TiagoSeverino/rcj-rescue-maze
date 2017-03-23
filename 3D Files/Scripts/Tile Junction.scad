difference(){
    cube([20, 20, 12.5], center=true);
    
    rotate([0,0,45])translate([0,0,2.5])cube([29,3.35,10], center=true);
    rotate([0,0,135])translate([0,0,2.5])cube([29,3.35,10], center=true);
}