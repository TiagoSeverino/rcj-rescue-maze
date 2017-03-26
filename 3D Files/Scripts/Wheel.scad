difference(){
    difference(){
        cylinder(8, 33.5, 33.5, $fn = 256);
        cylinder(4, 29.5, 29.5, $fn = 128);
    }
    
    union(){
        translate([8,0,0])cylinder(8, 1, 1);
        translate([-8,0,0])cylinder(8, 1, 1);
        translate([0,8,0])cylinder(8, 1, 1);
        translate([0,-8,0])cylinder(8, 1, 1);
    }
}