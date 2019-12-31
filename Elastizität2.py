from dolfin import *
import numpy as np
from ufl import nabla_div
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
        
print("\n1: Baustahl")
print("2: Aluminium")

Wert=0
while Wert==0:
    print("Geben Sie die Nummer für das gewünschte Material ein!")
    m=int(input())
    if m in [1,2]:
        Wert=1
    else:
        print("Die eingegebene Zahl entspricht nicht den zur Verfügung stehenden Möglichkeiten!")

if m==1:
    #Baustahl:
    nu=0.27
    E=210*10**9 #GPa
    rho=7.84*10**3 #kg/m³
elif m==2:
    #Aluminium:
    nu=0.34
    E=65*10**9 #GPa
    rho=2.7*10**3 #kg/m³


lambda_=(nu/(1-2*nu))*(1/(1+nu))*E
mu=(1/2)*(1/1+nu)*E
  
g=9.81

link="Meshing/Geometrie"
mesh=Mesh(link+".xml")
domains=MeshFunction("size_t",mesh,link+"_physical_region.xml")
facets=MeshFunction("size_t",mesh,link+"_facet_region.xml")

print("\n1: Druck")
print("2: Zug")
print("3: Scherung")
print("Wählen Sie eine Verformung!")

k=int(input())
if k==1:
    T=Constant((0,0,10**10))
elif k==2:
    T=Constant((0,0,-10**10))
elif k==3:
    T=Constant((0,10**8,0))

V=VectorFunctionSpace(mesh,"P",1)

def epsilon(u):
    return (1/2)*(nabla_grad(u)+nabla_grad(u).T)
    
def sigma(u):
    return lambda_*nabla_div(u)*Identity(d)+2*mu*epsilon(u)

bc=DirichletBC(V,Constant((0,0,0)),facets,1) 

ds=Measure("ds",mesh,subdomain_data=domains)
 
u=TrialFunction(V)
d=u.geometric_dimension()
v=TestFunction(V)
f=Constant((0,0,-g*rho))
a=inner(sigma(u),epsilon(v))*dx
rhs=dot(f,v)*dx+dot(T,v)*ds(1)+dot(-T,v)*ds(2)

u=Function(V)
solve(a==rhs,u,bc)

File('Verformung/displacement.pvd') << u

V = FunctionSpace(mesh, 'P', 1)

u_magnitude = sqrt(dot(u, u))
u_magnitude = project(u_magnitude, V)
print('min/max u:',
      np.min(np.array(u_magnitude.vector())),
      np.max(np.array(u_magnitude.vector())))
    
File('Verformung/magnitude.pvd') << u_magnitude



        
        
    
