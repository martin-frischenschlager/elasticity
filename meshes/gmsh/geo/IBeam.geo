//CROSS SECTION
lc = 1E-1;

Point(1) = {0.0, 0.0, 0.0, lc};
Point(2) = {1.0, 0.0, 0.0, lc};
Point(3) = {1.0, 0.1, 0.0, lc};
Point(4) = {0.55, 0.1, 0.0, lc};
Point(5) = {0.55, 0.9, 0.0, lc};
Point(6) = {1.0, 0.9, 0.0, lc};
Point(7) = {1.0, 1.0, 0.0, lc};
Point(8) = {0.0, 1.0, 0.0, lc};
Point(9) = {0.0, 0.9, 0.0, lc};
Point(10) = {0.45, 0.9, 0.0, lc};
Point(11) = {0.45, 0.1, 0.0, lc};
Point(12) = {0.0, 0.1, 0.0, lc};

Line(13) = {1, 2};
Line(14) = {2, 3};
Line(15) = {3, 4};
Line(16) = {4, 5};
Line(17) = {5, 6};
Line(18) = {6, 7};
Line(19) = {7, 8};
Line(20) = {8, 9};
Line(21) = {9, 10};
Line(22) = {10, 11};
Line(23) = {11, 12};
Line(24) = {12, 1};

Line Loop(1) = {13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24};
Plane Surface(1) = {1};

//EXTRUDE
beam[] = Extrude{0.0, 0.0, 10.0} {Surface{1};};

//DEFINE PHYSICAL SURFACES/VOLUMES
Physical Surface(1) = {1};
Physical Surface(2) = {beam[0]};

Physical Volume(1) = {beam[1]};
