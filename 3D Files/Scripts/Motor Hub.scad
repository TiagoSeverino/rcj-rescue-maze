$fn=16;

rotate([0,0,45])difference(){
    union(){
        difference(){
            cylinder(8.5, 4.5, 4.5, $fn=128);
            cylinder(8.5, 2.2, 2.2, $fn=128);
        }
        translate([1.5,-2,0])cube([1, 4, 8]);
        translate([3.5,0,5.5])rotate([0,90,0])cylinder(3, 2.5, 2.5); 
    }

    translate([1.5,0,5.5])rotate([0,90,0])cylinder(5, 0.5, 0.5);
}



difference(){
    cylinder(2.5, 12.5, 12.5, $fn=128);
    cylinder(2.5, 2.2, 2.2, $fn=128);
    
    union(){
        translate([8,0,0])cylinder(2.5, 1, 1);
        translate([-8,0,0])cylinder(2.5, 1, 1);
        translate([0,8,0])cylinder(2.5, 1, 1);
        translate([0,-8,0])cylinder(2.5, 1, 1);
    }
}