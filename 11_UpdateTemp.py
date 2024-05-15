
import numpy as np
import scipy


gactin=np.genfromtxt("concentration.txt") 
f= open('mesh.inp',"r")
lines = f.readlines()
inicio = 0
fin = 0
for i in range (0, len(lines)):
	if (lines[i] == '*Element, type=CAX3\n'):
		fin = i
f = open('mesh.inp',)
n1 = open('gactin_coordinates.txt', 'w')
for j, text in enumerate (f):
	if j>inicio and j<fin:
		n1.write(text)
	else:
		pass
n1.close()

with open('gactin_coordinates.txt', 'r') as file:
	filedata=file.read()
filedata=filedata.replace(',','\t') 
with open('gactin_coordinates.txt', 'wb') as file:
  file.write(filedata)

mesh = np.genfromtxt('gactin_coordinates.txt')  
coord_y = np.zeros((len(mesh),2))
coord_y[:,1] = mesh[:,2]
front = coord_y.max()
medio = np.median(coord_y)
eliminar = np.zeros((len(mesh)))
# We look for the front nodes
contour = np.genfromtxt('SortedContour.inp')
#What if now instead of being only of the maximum in the front 2 microns we do it according to each point in the vertical?
#The easiest way is to take them according to the set.
#Another option is to take them according to the Euclidean distance to the contour.
# We take only the contour that we are interested in.
contourf = np.zeros((len(contour),2))
if (contour[0,1]>contour[-1,0]):
    a=0
    contourf[0]=contour[a]
    for i in range (0, len(contour)-1):
        if (contour[a+i,0]<5.95):
            contourf[i+1]=contour[a+i]
else:
    a=len(contour)
    contourf[0]=contour[a]
    for i in range (0, len(contour)+1):
        if (contour[a-i,0]<5.95):
            contourf[i+1]=contour[a-i]
b=np.argwhere(contourf[:,1]==0.0)
contourf = np.delete(contourf, np.s_[np.asscalar(b[0]):len(contour)],axis=0)
distance = np.zeros(len(contourf))
for i in range (0,len(mesh)):
    nodox = mesh[i,1]
    nodoy = mesh[i,2]
    for j in range (0,len(contourf)):
        distance[j] = ((nodox-contourf[j,0])**2+(nodoy-contourf[j,1])**2)**0.5
    if (np.all(distance>1.5)):
        mesh[i,:]=0.0
    
temperature_i = np.genfromtxt('interpoled_temperature.inp')
contour_nucleo=np.genfromtxt('SortedContourNucleus.inp')
contour_yn=contour_nucleo[:,1]
max_yn=contour_yn.max()
min_yn=contour_yn.min()
medio_n=(max_yn+min_yn)/2

tmax = 2
tmin = -5
temperature_grad = np.zeros((len(temperature_i),2))
temperature_grad[:,0] = temperature_i[:,0]
temperature_grad[:,1] = (tmax-tmin)/(front-medio_n)*coord_y[:,1]-(front*(tmax-tmin)/(front-medio_n))+tmax

##We make a gactin matrix that has zero where there is no temperature to be added and the value where there is.
for i in range (0, len(gactin)):
    if gactin[i,0] not in mesh[:,0]:
        gactin[i,1]=0.0
temperature=(gactin[:,1]*0.75)+temperature_i[:,1]*0.5+temperature_grad[:,1]

f = open ('temp.inp', 'wb')
for j in range (0,temperature.size):
	f.write("Cell-1.%i,		%10.4E\n" % (temperature_i[j,0],temperature[j]*0.5))
f.close()	
