from dolfin import *
import numpy as np
from ufl import nabla_div

y=2
z=2
x=100
mesh=BoxMesh(Point(0,0,0),Point(x,y,z),200,5,5)

#Aluminium:
nu=0.35
E=70*10**9 #GPa
lambda_=(nu/(1-2*nu))*(1/(1+nu))*E
mu=(1/2)*(1/1+nu)*E
g=9.81
rho=2.7*10**3 #kg/m³

V=VectorFunctionSpace(mesh,"P",1)

def epsilon(u):
    return (1/2)*(nabla_grad(u)+nabla_grad(u).T)
    
def sigma(u):
    return lambda_*nabla_div(u)*Identity(d)+2*mu*epsilon(u)

def boundary(x,on_boundary):
    return near(x[0],0.0) and on_boundary

bc=DirichletBC(V,Constant((0,0,0)),boundary) 
 
u=TrialFunction(V)
d=u.geometric_dimension()
v=TestFunction(V)
f=Constant((0,0,-rho*g))
T=Constant((0,0,0))
a=inner(sigma(u),epsilon(v))*dx
rhs=dot(f,v)*dx+dot(T,v)*ds

u=Function(V)
solve(a==rhs,u,bc)

File('Schwerkraft/displacement.pvd') << u

V = FunctionSpace(mesh, 'P', 1)

u_magnitude = sqrt(dot(u, u))
u_magnitude = project(u_magnitude, V)
print('min/max u:',
      np.min(np.array(u_magnitude.vector())),
      np.max(np.array(u_magnitude.vector())))

#theoretisch:

maxdisp = -(1/3)*(x*rho*g*x**3)/(E*(1/12)*z*y**3)
print(maxdisp)
    
File('Schwerkraft/magnitude.pvd') << u_magnitude
