translate([0,0,5])rotate([0,0,45])cube([3.35, 3.35, 10], center=true);

translate([0,0,5])difference(){
    union(){
        cube([20, 20, 10], center=true);
    }
    
    translate([0,0,1])union(){
        rotate([0,0,45])cube([29,3.35,10], center=true);
        rotate([0,0,135])cube([29,3.35,10], center=true);
    }
}

translate([0,0,-1.7])union(){
    rotate([0,0,45])cube([29,3.35,3.4], center=true);
    rotate([0,0,135])cube([29,3.35,3.4], center=true);
}

translate([0,0,-4.4])cube([20, 20, 2], center=true);