//CROSS SECTION
lc = 1E-1;

Point(1) = {0.5, 0.5, 0.0, lc};
Point(2) = {1.0, 0.5, 0.0, lc};
Point(3) = {0.5, 1.0, 0.0, lc};
Point(4) = {0.0, 0.5, 0.0, lc};
Point(5) = {0.5, 0.0, 0.0, lc};
Point(6) = {0.9, 0.5, 0.0, lc};
Point(7) = {0.5, 0.9, 0.0, lc};
Point(8) = {0.1, 0.5, 0.0, lc};
Point(9) = {0.5, 0.1, 0.0, lc};

Circle(1) = {2, 1, 3};
Circle(2) = {3, 1, 4};
Circle(3) = {4, 1, 5};
Circle(4) = {5, 1, 2};
Circle(5) = {6, 1, 7};
Circle(6) = {7, 1, 8};
Circle(7) = {8, 1, 9};
Circle(8) = {9, 1, 6};

Line Loop(1) = {1, 2, 3, 4};
Line Loop(2) = {5, 6, 7, 8};

Plane Surface(1) = {1, 2};

//EXTRUDE
beam[] = Extrude{0.0, 0.0, 10.0} {Surface{1};};

//DEFINE PHYSICAL SURFACES/VOLUMES
Physical Surface(1) = {1};
Physical Surface(2) = {beam[0]};

Physical Volume(1) = {beam[1]};
