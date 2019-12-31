#!/bin/sh
for file in geo/*.geo; do
    name=$(basename "$file" .geo)
    gmsh $file -3 -o msh/$name.msh
    dolfin-convert msh/$name.msh xml/$name.xml
done
