from dolfin import *
import materials
import os
import numpy as np
from ufl import nabla_div
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

E=210*10**9
nu=0.35
rho=2.7*10**3
length = 10

lambda_=(nu/(1-2*nu))*(1/(1+nu))*E
mu=(1/2)*(1/1+nu)*E
g=9.81

# load corresponding mesh
mesh = Mesh("Meshing/Geometrie.xml")
domains=MeshFunction("size_t",mesh,"Meshing/Geometrie_physical_region.xml")
facets=MeshFunction("size_t",mesh,"Meshing/Geometrie_facet_region.xml")

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

f = Constant((0,-10**2 * force,0))
T=Constant((0,0,0))

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
print(minDisplace)
print(maxDisplace)

#von Mises:
s = sigma(u) - (1./3)*tr(sigma(u))*Identity(d)
von_Mises = sqrt(3./2*inner(s, s))
von_Mises = project(von_Mises, V)
File('output/von_Mises.pvd')<<von_Mises

# open results in paraview
command = "paraview output/displacement.pvd"
os.system(command)
