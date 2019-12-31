from dolfin import *
import numpy as np
from ufl import nabla_div
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

A=mpimg.imread("Querschnitte/I_Balken.png")
B=mpimg.imread("Querschnitte/Kreisbalken.png")
C=mpimg.imread("Querschnitte/O_Balken.png")
D=mpimg.imread("Querschnitte/Rechtecksbalken.png")
E=mpimg.imread("Querschnitte/RechtecksO_Balken.png")
F=mpimg.imread("Querschnitte/T_Balken.png")
G=mpimg.imread("Querschnitte/U_Balken.png")

plt.subplot(241)
plt.imshow(A)
plt.axis("off")
plt.title("1")
plt.subplot(242)
plt.imshow(B)
plt.axis("off")
plt.title("2")
plt.subplot(243)
plt.imshow(C)
plt.axis("off")
plt.title("3")
plt.subplot(244)
plt.imshow(D)
plt.axis("off")
plt.title("4")
plt.subplot(245)
plt.imshow(E)
plt.axis("off")
plt.title("5")
plt.subplot(246)
plt.imshow(F)
plt.axis("off")
plt.title("6")
plt.subplot(247)
plt.imshow(G)
plt.axis("off")
plt.title("7")

plt.show()

Wert=0

while Wert==0:
    print("Geben Sie die Nummer des gewünschten Querschnittes an!")
    z=int(input())
    if z in [1,2,3,4,5,6,7]:
        Wert=1
    else:
        print("Die eingegebene Zahl entspricht nicht den zur Verfügung stehenden Möglichkeiten!")

Querschnitte=["I_Balken","Kreisbalken","O_Balken","Rechtecksbalken","RechtecksO_Balken","T-Balken","U_Balken"]
link="Meshes/"+Querschnitte[z-1]+"/"+Querschnitte[z-1]

mesh=Mesh(link+".xml")
domains=MeshFunction("size_t",mesh,link+"_physical_region.xml")
facets=MeshFunction("size_t",mesh,link+"_facet_region.xml")

print("\n1: Baustahl")
print("2: Aluminium")

Wert=0
while Wert==0:
    print("Geben Sie die Nummer für das gewünschte Material ein!")
    z=int(input())
    if z in [1,2]:
        Wert=1
    else:
        print("Die eingegebene Zahl entspricht nicht den zur Verfügung stehenden Möglichkeiten!")

if z==1:
    #Baustahl:
    nu=0.27
    E=210*10**9 #GPa
    rho=7.84*10**3 #kg/m³
elif z==2:
    #Aluminium:
    nu=0.34
    E=65*10**9 #GPa
    rho=2.7*10**3 #kg/m³


lambda_=(nu/(1-2*nu))*(1/(1+nu))*E
mu=(1/2)*(1/1+nu)*E
  
g=9.81

V=VectorFunctionSpace(mesh,"P",1)

def epsilon(u):
    return (1/2)*(nabla_grad(u)+nabla_grad(u).T)
    
def sigma(u):
    return lambda_*nabla_div(u)*Identity(d)+2*mu*epsilon(u)

bc=DirichletBC(V,Constant((0,0,0)),facets,3) 

ds=Measure("ds",mesh,subdomain_data=domains)
 
u=TrialFunction(V)
d=u.geometric_dimension()
v=TestFunction(V)
f=Constant((0,0,0))
T=Constant((0,0,10**9)) #10**12 N in z-Richtung
a=inner(sigma(u),epsilon(v))*dx
rhs=dot(f,v)*dx+dot(T,v)*ds(1)+dot(-T,v)*ds(2)

u=Function(V)
solve(a==rhs,u,bc)

File('Zug/displacement.pvd') << u

V = FunctionSpace(mesh, 'P', 1)

u_magnitude = sqrt(dot(u, u))
u_magnitude = project(u_magnitude, V)
print('min/max u:',
      np.min(np.array(u_magnitude.vector())),
      np.max(np.array(u_magnitude.vector())))
    
File('Zug/magnitude.pvd') << u_magnitude
