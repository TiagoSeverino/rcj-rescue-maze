$fn=64;

difference(){
    union(){
        difference(){
            cylinder(10, 4.5, 4.5);
            cylinder(10, 2.2, 2.2);
        }

        translate([1.6,-2,0])cube([1, 4, 8.5]);
    }

    #translate([1.5,0,4.25])rotate([0,90,0])cylinder(3, 0.5, 0.5); 
}

difference(){
    translate([0,0,-1.25])cylinder(2.5, 12.5, 12.5);
    cylinder(10, 2.2, 2.2);
    
    #translate([0,0,-1.25])union(){
        translate([8,0,0])cylinder(2.5, 1, 1);
        translate([-8,0,0])cylinder(2.5, 1, 1);
        translate([0,8,0])cylinder(2.5, 1, 1);
        translate([0,-8,0])cylinder(2.5, 1, 1);
    }
}

