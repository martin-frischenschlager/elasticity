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
H=mpimg.imread("Querschnitte/Eckbalken.png")

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
plt.subplot(248)
plt.imshow(H)
plt.axis("off")
plt.title("8")

plt.show()
plt.draw()

Wert=0

while Wert==0:
    print("Geben Sie die Nummer des gewünschten Querschnittes an!")
    z=int(input())
    if z in [1,2,3,4,5,6,7,8]:
        Wert=1
    else:
        print("Die eingegebene Zahl entspricht nicht den zur Verfügung stehenden Möglichkeiten!")
        
print("Geben Sie die Länge des Balken ein!")
length=float(input())

if z==1:
    name="meshes/gmsh/geo/IBeam.geo"
elif z==2:
    name="meshes/gmsh/geo/CircularBeam.geo"
elif z==3:
    name="meshes/gmsh/geo/CircularHollowBeam.geo"
elif z==4:
    name="meshes/gmsh/geo/RectangularBeam.geo"
elif z==5:
    name="meshes/gmsh/geo/RectangularHollowBeam.geo"
elif z==6:
    name="meshes/gmsh/geo/TBeam.geo"
elif z==7:
    name="meshes/gmsh/geo/ChannelBeam.geo"
elif z==8:
    name="meshes/gmsh/geo/AngledBeam.geo"
    
file=open(name,"r+")
file.write("length=%.9f;\n"% length)
file.close()
file=open(name,"r")
content=file.read()
file.close()
file=open("Meshing/Geometrie.geo","w")
file.write(content)
file.close()