
lc = 1E-1;

Point(1) = {0.0, 0.0, 0.0, lc};
Point(2) = {1.0, 0.0, 0.0, lc};
Point(3) = {1.0, 1.0, 0.0, lc};
Point(4) = {0.0, 1.0, 0.0, lc};
Point(5) = {0.1, 0.1, 0.0, lc};
Point(6) = {0.9, 0.1, 0.0, lc};
Point(7) = {0.9, 0.9, 0.0, lc};
Point(8) = {0.1, 0.9, 0.0, lc};

Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};
Line(5) = {5, 6};
Line(6) = {6, 7};
Line(7) = {7, 8};
Line(8) = {8, 5};

Line Loop(1) = {1, 2, 3, 4};
Line Loop(2) = {5, 6, 7, 8};
Plane Surface(1) = {1, 2};

//EXTRUDE
beam[] = Extrude{0.0, 0.0,length} {Surface{1};};

//DEFINE PHYSICAL SURFACES/VOLUMES
Physical Surface(1) = {1};
Physical Surface(2) = {beam[0]};

Physical Volume(1) = {beam[1]};
