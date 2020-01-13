
lc = 1E-1;

Point(1) = {0.0, 0.0707, 0.0, lc};
Point(2) = {0.0707, 0.0, 0.0, lc};
Point(3) = {0.5, 0.4293, 0.0, lc};
Point(4) = {0.9293, 0.0, 0.0, lc};
Point(5) = {1.0, 0.0707, 0.0, lc};
Point(6) = {0.5, 0.5707, 0.0, lc};

Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 5};
Line(5) = {5, 6};
Line(6) = {6, 1};

Line Loop(1) = {1, 2, 3, 4, 5, 6};
Plane Surface(1) = {1};

//EXTRUDE
beam[] = Extrude{0.0, 0.0, length} {Surface{1};};

//DEFINE PHYSICAL SURFACES/VOLUMES
Physical Surface(1) = {1};
Physical Surface(2) = {beam[0]};

Physical Volume(1) = {beam[1]};
