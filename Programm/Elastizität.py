from dolfin import *
import materials
import os
import numpy as np
from ufl import nabla_div
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

os.system("rm -r Meshing/*")

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
fig2.suptitle("Wählen Sie einen Querschnitt aus!")

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

print("Querschnitt:", crossSec)

print("Geben Sie die Länge des Balken ein!")
length=float(input())

name="meshes/gmsh/geo/"+str(crossSec)+"Beam.geo"
    
file=open(name,"r")
content=file.read()
file.close()
file=open("Meshing/Geometrie.geo","w")
file.write("length=%.9f;\n"% length)
file.write(content)
file.close()

command="gmsh Meshing/Geometrie.geo -3 Meshing/Geometrie.msh"
os.system(command)

command="dolfin-convert Meshing/Geometrie.msh Meshing/Geometrie.xml"
os.system(command)

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
fig1.suptitle("Wählen Sie ein Material aus!")

btn1 = Button(ax=ax1[0], label="Aluminium", image=next(matRead))
btn2 = Button(ax=ax1[1], label="Stahl", image=next(matRead))
btn3 = Button(ax=ax1[2], label="Beton", image=next(matRead))
btn4 = Button(ax=ax1[3], label="Glas", image=next(matRead))
btn5 = Button(ax=ax1[4], label="Gummi", image=next(matRead))

btn1.on_clicked(mat1)
btn2.on_clicked(mat2)
btn3.on_clicked(mat3)
btn4.on_clicked(mat4)
btn5.on_clicked(mat5)

for i in range(columns):
    ax1[i].axis("off")
plt.show()

print("Material:", material)

# set material constants
E, nu, rho = materials.Material.values[material]
lambda_=(nu/(1-2*nu))*(1/(1+nu))*E
mu=(1/2)*(1/1+nu)*E
g=9.81

# load corresponding mesh
mesh = Mesh("Meshing/Geometrie.xml")
domains=MeshFunction("size_t",mesh,"Meshing/Geometrie_physical_region.xml")
facets=MeshFunction("size_t",mesh,"Meshing/Geometrie_facet_region.xml")

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
fig3.suptitle("Wählen Sie eine Belastungsart!")

btn1 = Button(ax=ax3[0], label="Zug", image=next(loadRead))
btn2 = Button(ax=ax3[1], label="Kompression", image=next(loadRead))
btn3 = Button(ax=ax3[2], label="Scherung", image=next(loadRead))
btn4 = Button(ax=ax3[3], label="Biegung", image=next(loadRead))
btn5 = Button(ax=ax3[4], label="Torsion", image=next(loadRead))

btn1.on_clicked(load1)
btn2.on_clicked(load2)
btn3.on_clicked(load3)
btn4.on_clicked(load4)
btn5.on_clicked(load5)

for i in range(columns):
    ax3[i].axis("off")
plt.show()
print("Belastungsart:", loadType)

# boundary conditions
V = VectorFunctionSpace(mesh,"P",1)

class up(SubDomain):
    def inside(self,x,on_boundary):
        return near(x[2],length) and on_boundary
        
class down(SubDomain):
    def inside(self,x,on_boundary):
        return near(x[2],0.0) and on_boundary

Down=down()
Up=up()
boundaries=MeshFunction("size_t",mesh,0)
boundaries.set_all(0)
Down.mark(boundaries,1)
Up.mark(boundaries,2)
ds=Measure("ds",domain=mesh,subdomain_data=boundaries)

def boundary(x,on_boundary):
    return near(x[2], 0.0) and on_boundary
    
def boundary2(x):
    return near(x[2],length/2)

if loadType is "tension":
    bc = DirichletBC(V,Constant((0,0,0)),boundary)
elif loadType is "compression":
    bc = DirichletBC(V,Constant((0,0,0)),boundary)
elif loadType is "shear":
    bc = DirichletBC(V,Constant((0,0,0)),boundary)
elif loadType is "bending":
    bc = DirichletBC(V,Constant((0,0,0)),boundary)
elif loadType is "torsion":
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
    T = Constant((0,-10**3 * force,0))
elif loadType is "bending":
    f = Constant((0,-10**2 * force,0))
elif loadType is "torsion":
    f = Expression(("frc * -(x[1] - 0.5)","frc * (x[0] - 0.5)","0"), degree=3, frc = 10**3 * force)

a=inner(sigma(u),epsilon(v))*dx
rhs=dot(f,v)*dx+dot(-T,v)*ds(1)+dot(T,v)*ds(2)

# solve
u=Function(V)
solve(a==rhs,u,bc)

# export pvd-files
File("output/displacement.pvd") << u

V = FunctionSpace(mesh, 'P', 1)

u_magnitude = sqrt(dot(u, u))
u_magnitude = project(u_magnitude, V)

File("output/magnitude.pvd") << u_magnitude

# log min/max displacement values
minDisplace = u_magnitude.vector().get_local().min()
maxDisplace = u_magnitude.vector().get_local().max()

#von Mises:
s = sigma(u) - (1./3)*tr(sigma(u))*Identity(d)
von_Mises = sqrt(3./2*inner(s, s))
von_Mises = project(von_Mises, V)
File('output/von_Mises.pvd')<<von_Mises

# open results in paraview
command = "paraview output/displacement.pvd"
os.system(command)
