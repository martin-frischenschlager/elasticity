from dolfin import *
import materials
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# read in images of materials
mat_names = ["aluminum", "steel", "concrete", "glass", "rubber"]
mat_paths = ["./images/materials/" + name  + ".png" for name in mat_names]
matRead = (plt.imread(path) for path in mat_paths)

# open material window
material = ""

def mat1(event):
    global material
    material = mat_names[0]
    plt.close()

def mat2(event):
    global material
    material = mat_names[1]
    plt.close()

def mat3(event):
    global material
    material = mat_names[2]
    plt.close()

def mat4(event):
    global material
    material = mat_names[3]
    plt.close()

def mat5(event):
    global material
    material = mat_names[4]
    plt.close()

columns = len(mat_names)
fig1, ax1 = plt.subplots(ncols=columns)
fig1.suptitle("Select Material")

btn1 = Button(ax=ax1[0], label="", image=next(matRead))
btn2 = Button(ax=ax1[1], label="", image=next(matRead))
btn3 = Button(ax=ax1[2], label="", image=next(matRead))
btn4 = Button(ax=ax1[3], label="", image=next(matRead))
btn5 = Button(ax=ax1[4], label="", image=next(matRead))

btn1.on_clicked(mat1)
btn2.on_clicked(mat2)
btn3.on_clicked(mat3)
btn4.on_clicked(mat4)
btn5.on_clicked(mat5)

for i in range(columns):
    ax1[i].axis("off")
plt.show()

print("Material is", material)

# set material constants
E, nu, rho = materials.Material.values[material]
lambda_=(nu/(1-2*nu))*(1/(1+nu))*E
mu=(1/2)*(1/1+nu)*E
g=9.81

# read in images of cross-sections
crossec_names = ["Circular", "CircularHollow", "Rectangular", "RectangularHollow", "I", "T", "Channel", "Angled"]
crossec_paths = ["./images/cross-sections/" + name + "Beam.png" for name in crossec_names]
crossecRead = (plt.imread(path) for path in crossec_paths)

# open window for selection of cross-section
crossSec = ""

def sec1(event):
    global crossSec
    crossSec = crossec_names[0]
    plt.close()

def sec2(event):
    global crossSec
    crossSec = crossec_names[1]
    plt.close()

def sec3(event):
    global crossSec
    crossSec = crossec_names[2]
    plt.close()

def sec4(event):
    global crossSec
    crossSec = crossec_names[3]
    plt.close()

def sec5(event):
    global crossSec
    crossSec = crossec_names[4]
    plt.close()

def sec6(event):
    global crossSec
    crossSec = crossec_names[5]
    plt.close()

def sec7(event):
    global crossSec
    crossSec = crossec_names[6]
    plt.close()

def sec8(event):
    global crossSec
    crossSec = crossec_names[7]
    plt.close()

rows = 2
columns = len(crossec_names) // rows
fig2, ax2 = plt.subplots(rows, columns)
fig2.suptitle("Select Cross-section")

btn1 = Button(ax=ax2[0,0], label="", image=next(crossecRead))
btn2 = Button(ax=ax2[0,1], label="", image=next(crossecRead))
btn3 = Button(ax=ax2[0,2], label="", image=next(crossecRead))
btn4 = Button(ax=ax2[0,3], label="", image=next(crossecRead))
btn5 = Button(ax=ax2[1,0], label="", image=next(crossecRead))
btn6 = Button(ax=ax2[1,1], label="", image=next(crossecRead))
btn7 = Button(ax=ax2[1,2], label="", image=next(crossecRead))
btn8 = Button(ax=ax2[1,3], label="", image=next(crossecRead))

btn1.on_clicked(sec1)
btn2.on_clicked(sec2)
btn3.on_clicked(sec3)
btn4.on_clicked(sec4)
btn5.on_clicked(sec5)
btn6.on_clicked(sec6)
btn7.on_clicked(sec7)
btn8.on_clicked(sec8)

for i in range(rows):
    for j in range(columns):
        ax2[i,j].axis("off")
plt.show()

print("Cross-section is", crossSec)

# load corresponding mesh
path = "./meshes/gmsh/xml/" + crossSec + "Beam.xml"
mesh = Mesh("./meshes/gmsh/xml/" + crossSec + "Beam.xml")

# read in images of types of load
load_names = ["tension", "compression", "shear", "bending", "torsion"]
load_paths = ["./images/load-types/" + name  + ".png" for name in load_names]
loadRead = (plt.imread(path) for path in load_paths)

# open window for selection of stress
loadType = ""

def load1(event):
    global loadType
    loadType = load_names[0]
    plt.close()

def load2(event):
    global loadType
    loadType = load_names[1]
    plt.close()

def load3(event):
    global loadType  
    loadType = load_names[2]
    plt.close()

def load4(event):
    global loadType
    loadType = load_names[3]
    plt.close()

def load5(event):
    global loadType
    loadType = load_names[4]
    plt.close()

columns = len(load_names)
fig3, ax3 = plt.subplots(ncols=columns)
fig3.suptitle("Select Type of Load")

btn1 = Button(ax=ax3[0], label="", image=next(loadRead))
btn2 = Button(ax=ax3[1], label="", image=next(loadRead))
btn3 = Button(ax=ax3[2], label="", image=next(loadRead))
btn4 = Button(ax=ax3[3], label="", image=next(loadRead))
btn5 = Button(ax=ax3[4], label="", image=next(loadRead))

btn1.on_clicked(load1)
btn2.on_clicked(load2)
btn3.on_clicked(load3)
btn4.on_clicked(load4)
btn5.on_clicked(load5)

for i in range(columns):
    ax3[i].axis("off")
plt.show()
print("Type of Load is:", loadType)

# boundary conditions
V = VectorFunctionSpace(mesh,"P",1)

def boundary(x,on_boundary):
    return near(x[2], 0.0) and on_boundary

bc = DirichletBC(V,Constant((0,0,0)),boundary)

# define variational problem

def epsilon(u):
    return (1/2)*(nabla_grad(u)+nabla_grad(u).T)

def sigma(u):
    return lambda_*nabla_div(u)*Identity(d)+2*mu*epsilon(u)


u = TrialFunction(V)
d = u.geometric_dimension()
v = TestFunction(V)

force = rho * g

f = Constant((0,0,0))
T = Constant((0,0,0))

if loadType is "tension":
    f = Constant((0,0,10**5 * force))
elif loadType is "compression":
    f = Constant((0,0,-10**5 * force))
elif loadType is "shear":
    T = Constant((0,-10**2 * force,0))
elif loadType is "bending":
    pass
elif loadType is "torsion":
    pass

a=inner(sigma(u),epsilon(v))*dx
rhs=dot(f,v)*dx+dot(T,v)*ds

# solve
u=Function(V)
solve(a==rhs,u,bc)

# export pvd-files
File("./output/displacement.pvd") << u

V = FunctionSpace(mesh, 'P', 1)

u_magnitude = sqrt(dot(u, u))
u_magnitude = project(u_magnitude, V)

File("./output/magnitude.pvd") << u_magnitude

# log min/max displacement values
minDisplace = u_magnitude.vector().get_local().min()
maxDisplace = u_magnitude.vector().get_local().max()

logEntry = "*"*80 + "\n"
logEntry += """Material: {}
Shape: {}
Load: {}
Force: {}
Max / Min Displacement: {} | {}
""".format(material, crossSec, loadType, force, maxDisplace, minDisplace)

with open("./output/log.txt", "a") as outputFile:
    outputFile.write(logEntry)
 
# open results in paraview
command = "paraview ./output/displacement.pvd; leafpad ./output/log.txt"
os.system(command)

