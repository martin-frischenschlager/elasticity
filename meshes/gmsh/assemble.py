import os

# get all .geo files from ./gmsh/
gmsh_dir = os.getcwd() + "/geo"
file_list = os.listdir(gmsh_dir)

# perform "gmsh *.geo -o ../*.msh" and "dolfin-convert *.msh *.xml" on all those files
for file in file_list:
    cmd = "gmsh " + "geo/" + file + " -3 -o msh/" + file[:-4] + ".msh"
    os.system(cmd)
    os.system("dolfin-convert msh/" + file[:-4] + ".msh xml/" + file[:-4] + ".xml")

