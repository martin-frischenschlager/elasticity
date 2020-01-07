from dolfin import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# read in images of cross-sections
imgnames = ["Circular", "CircularHollow", "Rectangular", "RectangularHollow", "I", "T", "Channel", "Angled"]
names = (n for n in imgnames)
imgpaths = ["./images/cross-sections/" + imgnames[n] + "Beam.png" for n in range(len(imgnames))]
imRead = (plt.imread(imgpaths[n]) for n in range(len(imgpaths)))

# open window with buttons for selection of cross-section
crossSec = ""

def func1(event):
    global crossSec
    crossSec = imgnames[0]
    plt.close()

def func2(event):
    global crossSec
    crossSec = imgnames[1]
    plt.close()

def func3(event):
    global crossSec
    crossSec = imgnames[2]
    plt.close()

def func4(event):
    global crossSec
    crossSec = imgnames[3]
    plt.close()

def func5(event):
    global crossSec
    crossSec = imgnames[4]
    plt.close()

def func6(event):
    global crossSec
    crossSec = imgnames[5]
    plt.close()

def func7(event):
    global crossSec
    crossSec = imgnames[6]
    plt.close()

def func8(event):
    global crossSec
    crossSec = imgnames[7]
    plt.close()
rows = 2
columns = len(imgnames) // rows
fig, ax = plt.subplots(rows, columns)
fig.suptitle("Select Cross-section")

btn1 = Button(ax=ax[0,0], label="", image=next(imRead))
btn2 = Button(ax=ax[0,1], label="", image=next(imRead))
btn3 = Button(ax=ax[0,2], label="", image=next(imRead))
btn4 = Button(ax=ax[0,3], label="", image=next(imRead))
btn5 = Button(ax=ax[1,0], label="", image=next(imRead))
btn6 = Button(ax=ax[1,1], label="", image=next(imRead))
btn7 = Button(ax=ax[1,2], label="", image=next(imRead))
btn8 = Button(ax=ax[1,3], label="", image=next(imRead))

btn1.on_clicked(func1)
btn2.on_clicked(func2)
btn3.on_clicked(func3)
btn4.on_clicked(func4)
btn5.on_clicked(func5)
btn6.on_clicked(func6)
btn7.on_clicked(func7)
btn8.on_clicked(func8)

for i in range(rows):
    for j in range(columns):
        ax[i,j].axis("off")
plt.show()

# load corresponding mesh
path = "./meshes/gmsh/xml/" + crossSec + "Beam.xml"
mesh = Mesh("./meshes/gmsh/xml/" + crossSec + "Beam.xml")

# open window with buttons for selection of material

nu=0.27
E=210*10**9 #GPa
lambda_=(nu/(1-2*nu))*(1/(1+nu))*E
mu=(1/2)*(1/1+nu)*E
g=9.81
rho=7.84*10**3 #kg/m³


# open window with buttons for selection of stress

# boundary conditions
V=VectorFunctionSpace(mesh,"P",1)

def boundary(x,on_boundary):
    return (near(x[2],0.0) or near(x[2],10.0)) and on_boundary

bc=DirichletBC(V,Constant((0,0,0)),boundary)

# define variational problem

def epsilon(u):
    return (1/2)*(nabla_grad(u)+nabla_grad(u).T)

def sigma(u):
    return lambda_*nabla_div(u)*Identity(d)+2*mu*epsilon(u)


u=TrialFunction(V)
d=u.geometric_dimension()
v=TestFunction(V)
f=Constant((0,10**4 * -rho * g,0))
T=Constant((0,0,0))
a=inner(sigma(u),epsilon(v))*dx
rhs=dot(f,v)*dx+dot(T,v)*ds

# solve
u=Function(V)
solve(a==rhs,u,bc)

# export pvd-files
File('./output/displacement.pvd') << u

V = FunctionSpace(mesh, 'P', 1)

u_magnitude = sqrt(dot(u, u))
u_magnitude = project(u_magnitude, V)

File('./output/magnitude.pvd') << u_magnitude

