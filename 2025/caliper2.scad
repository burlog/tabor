use </tmp/bezier.scad>;

width = 6;
height = 10;
lenght = 200;

$fn = 96;
bzfn = 96;

LEAF_EDGE_CONTROL_POINTS = [
  [0, 0, 0],
  [-5, 100, 0],
  [90, lenght - 10, 0],
  [0, lenght, 0],
];

module cylinder_with_hole(oh, or1, or2, ih, ir1, ir2, shift = 0) {
    difference() {
        cylinder(oh, or1, or2);
        translate([shift, 0, - (ih * 0.05)])
            cylinder(ih * 1.1, ir1, ir2);
    }
}

module arm_joint(h) {
    translate([- (height / 4), 3, -height + 10]) {
        cylinder_with_hole(h, width * 1.5, width * 1.5, h, width / 2, width / 2, -1);
    }
}


module arm(measure_holes = 0) {
    difference() {
        union() {
            difference() {
                bezier(LEAF_EDGE_CONTROL_POINTS, bzfn) cube([width, width, height]);
                if (measure_holes) {
                    pos = 70;
                    ir = width / 4;
                    translate([12, pos + 1, -(height * 0.05)]) {
                        cylinder(height * 1.1, ir, ir);
                    }
                    translate([14.5, pos + 10, - (height * 0.05)]) {
                        cylinder(height * 1.1, ir, ir);
                    }
                }
            }
            if (measure_holes) {
                arm_joint(height / 3 - 0.5);
                translate([0, 0, 2 * height / 3 + 0.5]) arm_joint(height / 3 - 0.5);
            } else {
                translate([0, 0, height / 3 - 0.45]) arm_joint(height / 3 + 0.9);
            }
        }
        if (measure_holes) {
            translate([0, 0, height / 3]) arm_joint(height / 3);
        } else {
                arm_joint(height / 3);
                translate([0, 0, 2 * height / 3]) arm_joint(height / 3);
        }
    }
    
    translate([0, lenght + width / 2, 0]) cylinder(height, width, width);
}

mh = 4;

module measure() {
    r1 = 75;
    r2 = r1 - height * 1.5;
    h = mh;
    difference() {
        cylinder_with_hole(h, r1, r1, h, r2, r2);
        translate([0, - r1, - (h * 0.05)]) cube([r1 * 2, r1 * 2, h * 1.1]);
        translate([-r1, - r1, - (h * 0.05)]) cube([r1, r1, h * 1.1]);
        pos = 62;
        ir = width / 4;
        translate([-4, pos + 1, -(height * 0.05)]) {
            cylinder(height * 1.1, ir, ir);
        }
        translate([-4.5, pos + 10, - (height * 0.05)]) {
            cylinder(height * 1.1, ir, ir);
        }
    }
}

mirror([0, 0, 1]) {
    translate([0, 0, - height]) arm();
    translate ([-40, 0, - height]) arm(1);
    translate([-20, 70, - height + mh + 2]) measure();
}

