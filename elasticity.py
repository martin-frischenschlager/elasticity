from dolfin import *
import materials
import os

material = "steel"
print("Material is", material)

# set material constants
E, nu, rho = materials.Material.values[material]
lambda_=(nu/(1-2*nu))*(1/(1+nu))*E
mu=(1/2)*(1/1+nu)*E
g=9.81

crossSec = "Rectangular"
print("Cross-section is", crossSec)

# load corresponding mesh
path = "./meshes/gmsh/xml/" + crossSec + "Beam.xml"
mesh = Mesh("./meshes/gmsh/xml/" + crossSec + "Beam.xml")

loadType = "bending"
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
    f = Constant((0,-force,0))
elif loadType is "torsion":
    f = Expression(("frc * -(x[1] - 0.5)","frc * (x[0] - 0.5)","0"), degree=3, frc = 10**4 * force)
    pass

a=inner(sigma(u),epsilon(v))*dx
rhs=dot(f,v)*dx+dot(T,v)*ds

# solve
u=Function(V)
solve(a==rhs,u,bc)

# export pvd-files
File("./output/"+material+crossSec+loadType+".pvd") << u

V = FunctionSpace(mesh, 'P', 1)

u_magnitude = sqrt(dot(u, u))
u_magnitude = project(u_magnitude, V)

File("./output/magnitude"+material+crossSec+loadType+".pvd") << u_magnitude

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
#command = "paraview ./output/displacement.pvd; leafpad ./output/log.txt"
#os.system(command)

