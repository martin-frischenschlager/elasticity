from dolfin import *
import numpy as np
from ufl import nabla_div

mesh=Mesh("I_Balken.xml")
domains=MeshFunction("size_t",mesh,"I_Balken_physical_region.xml")
facets=MeshFunction("size_t",mesh,"I_Balken_facet_region.xml")

#Baustahl:
nu=0.27
E=210*10**9 #GPa
lambda_=(nu/(1-2*nu))*(1/(1+nu))*E
mu=(1/2)*(1/1+nu)*E
g=9.81
rho=7.84*10**3 #kg/m³

V=VectorFunctionSpace(mesh,"P",1)

def epsilon(u):
    return (1/2)*(nabla_grad(u)+nabla_grad(u).T)
    
def sigma(u):
    return lambda_*nabla_div(u)*Identity(d)+2*mu*epsilon(u)

def boundary(x,on_boundary):
    return near(x[2],200.0) and on_boundary

bc=DirichletBC(V,Constant((0,0,0)),boundary) 

class LowerBoundary(SubDomain):
    def inside(self,x,on_boundary):
        return near(x[2],0.0) and on_boundary
        
class UpperBoundary(SubDomain):
    def inside(self,x,on_boundary):
        return near(x[2],200.0) and on_boundary

lower=LowerBoundary()
upper=UpperBoundary()

boundaries=MeshFunction("size_t",mesh,2)
boundaries.set_all(0)
lower.mark(boundaries,1)
upper.mark(boundaries,2)
ds=Measure("ds",mesh,subdomain_data=boundaries)
 
u=TrialFunction(V)
d=u.geometric_dimension()
v=TestFunction(V)
f=Constant((0,0,0))
T=Constant((0,0,10**11)) #10**11 N in z-Richtung
a=inner(sigma(u),epsilon(v))*dx
rhs=dot(f,v)*dx+dot(T,v)*ds(1)+dot(-T,v)*ds(2)

u=Function(V)
solve(a==rhs,u,bc)

File('Druck/displacement.pvd') << u

V = FunctionSpace(mesh, 'P', 1)

u_magnitude = sqrt(dot(u, u))
u_magnitude = project(u_magnitude, V)
print('min/max u:',
      np.min(np.array(u_magnitude.vector())),
      np.max(np.array(u_magnitude.vector())))
    
File('Druck/magnitude.pvd') << u_magnitude
