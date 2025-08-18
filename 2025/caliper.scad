use </tmp/bezier.scad>;

width = 2;
height = 4;
$fn = 96;

LEAF_EDGE_CONTROL_POINTS = [
  [0, 0, 0],
  [-5, 100, 0],
  [60, 150, 0],
  [0, 160, 0],
];

module cylinder_with_hole(oh, or1, or2, ih, ir1, ir2, shift = 0) {
    difference() {
        cylinder(oh, or1, or2);
        translate([shift, 0, - (ih * 0.05)])
            cylinder(ih * 1.1, ir1, ir2);
    }
}

module arm(joint_rotate_angle, joint_shift, measure_joint = 0) {
    difference() {
        bezier(LEAF_EDGE_CONTROL_POINTS, 20) cube([width, width, height]);
        if (measure_joint) {
            pos = 70;
            ir = width / 4;
            translate([8.2, pos, -(height * 0.05)]) {
                cylinder(height * 1.1, ir, ir);
            }
            translate([9.2, pos + width * 2, - (height * 0.05)]) {
                cylinder(height * 1.1, ir, ir);
            }
        }
    }        
    translate([- (height / 8), -1, joint_shift - (height / 2)]) {
        rotate([joint_rotate_angle, 0, 0]) {
            cylinder_with_hole(height, width * 1.2, width * 1.4, height, width / 2, width / 2, - (width / 4));
        }
    }
    if (measure_joint) {
        translate([8.4, 70 - 3, 0]) {
            rotate([0, 0, -15]) {
                cube([width / 3, 10, height]);
            }
        }
        translate([5.7, 70 - 2.3, 0]) {
            rotate([0, 0, -14]) {
                cube([width / 3, 10, height]);
            }
        }
    }
    translate([0, 160 + width / 2, 0]) cylinder(height, width, width);
}

arm(0, 0);
translate ([-10, 0, 0]) {
    mirror([1, 0, 0]) arm(180, height * 2, 1);
};
