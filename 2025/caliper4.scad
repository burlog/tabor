use </tmp/bezier.scad>;

width = 6;
joint_hole_r = 3;
height = 10;
length = 240;
gap = 10;
measure_height = 4;
measure_width = 13;
measure_angle_shift = 86;
measure_angle = 60;
text_size = 4;
mark_length = 2;
mark_width = 0.5;
mark_depth = 1;

$fn = 96;
bzfn = 96;

module cylinder_with_hole(oh, or1, or2, ih, ir1, ir2, shift = 0) {
    difference() {
        cylinder(oh, or1, or2);
        translate([shift, 0, - (ih * 0.05)])
            cylinder(ih * 1.1, ir1, ir2);
    }
}

module joint() {
    h = height / 2;
    ro = width * 1.5;
    ri = joint_hole_r;
    cylinder_with_hole(h, ro, ro, h, ri, ri);
}

module measure(ri, ra, dx, tx, m = 1) {
    h = measure_height;
    w = measure_width;
    marks = 100;
    mark_angle = asin(5 / length);
    difference() {
        rotate([0, 0, ra]) {
            rotate_extrude(angle = measure_angle, $fn=360) {
                translate([ri, 0, 0]) {
                    polygon(points = [
                        [dx, 0],
                        [w - dx, 0],
                        [w - tx, h],
                        [tx, h]
                    ]);
                }
            }
        }
        if (m) {
            rotate([0, 0, 90]) {
                for (i = [0: marks - 1]) {
                    rotate([0, 0, i * mark_angle]) {
                        translate([ri, 0, h - mark_depth]) {
                            l = (i % 2 == 0) ? mark_length * 2: mark_length;
                            color("black") cube([l, mark_width, mark_length]);
                        }
                        
                        if (i % 2 == 0) {
                            translate([ri + (mark_length * 2) + 1, 0, h - mark_depth]) {
                                linear_extrude(height = mark_depth) {
                                    color("black") text(
                                        text = str(i / 2), 
                                        size = text_size, 
                                        valign = "center"
                                    );
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

module straight_part() {
    translate([joint_hole_r, 0, 0]) cube([width, length / 2, height]);
}

module curved_part() {
    control_points = [
      [joint_hole_r, length / 2, 0],
      [0, length / 2 + 30, 0],
      [length / 2 + 60, length - 30, 0],
  [gap, length, 0],
    ];
    bezier(control_points, bzfn) cube([width, width, height]);
    translate([0, length, 0])
        //cylinder(height, width * 1.2, width * 1.2);
        linear_extrude(height = height) {
            polygon(points = [[-1, 0], [gap, 0], [gap, width]]);
        }
}

module arm() {
    difference() {
        straight_part();
        translate([0, 0, height / 2]) joint();
    }
    joint();
    curved_part();
    color("orange") translate([0, length / 2, 0]) cube([gap / 2, measure_width, height]);
}

module left_arm() {
    color("red") arm();
    measure(length / 2, measure_angle_shift, 1, 0, 1);
//    measure(length, measure_angle_shift, 1, 0, 1);
}

module right_arm() {
    difference() {
        color("blue") arm();
        translate([0, 0, measure_height * 1.5]) measure(length / 2, 80, 0, 1, 0);
    }
}

//rotate([0, 0, 0])
//    left_arm();
rotate([0, 0, 0 * asin(5 / 240)])
    translate([0, 0, 0])
    rotate([0, 0, 0])
    right_arm();
    
//rotate([0, 0, 3 * asin(5 / 240)])
//    translate([0, 0, height])
//    rotate([0, 180, 0])
//    right_arm();