
import numpy as np
import sys


coord0=np.genfromtxt('4_0_initialmesh.inp')
with open('4_0_initialmesh.inp', 'r') as file:
	filedata=file.read()
filedata=filedata.replace(',','\t') 
with open('4_0_initialmesh.inp', 'wb') as file:
  file.write(filedata)

actin = np.genfromtxt('4_initialActinMesh.inp')

indices = np.zeros((len(actin)))

for i in range (0,len(indices)):
    indices[i]=np.argwhere(actin[i]==coord0[:,0])
    

coord_actin = np.zeros((len(indices),3))
for i in range (0, len(indices)):
    coord_actin[i,:] = coord0[indices[i].astype(int),:]

unique_nodes = coord_actin
temperature_i = np.zeros((len(coord_actin),2))
temperature_i[:,0] = coord_actin[:,0]

temperature_i[:,1] = 0.4*coord_actin[:,2]-14.06

gactin=np.genfromtxt("concentration.txt") 
temperature = np.zeros((len(gactin),2))
temperature[:,0] = gactin[:,0]      
#G-Actin only in the front
front = np.zeros((len(coord_actin),3))
mesh = coord_actin
deleting = np.zeros(len(mesh))
medio = np.median(coord_actin[:,2])
max= coord_actin[:,2].max()
for i in range (0, len(coord_actin)):
    if (max-coord_actin[i,2]>2):
        mesh[i,:]=0.0
for i in range (0,len(coord_actin)):
    if ((mesh[i,:].all()==0.0)):
        deleting[i]=i    
front = mesh

for i in range (0, len(gactin)):
    node = gactin[i,0]
    indice_temp = np.argwhere(temperature_i[:,0]==node)
    if len(indice_temp)>0:
        if (node in front[:,0]):
            temperature[i,1]=0.5*gactin[i,1]+temperature_i[indice_temp,1]
        else:
            temperature[i,1]=temperature_i[indice_temp,1]
        #temperature[i,1]=(gactin[i,1]**2)/(gactin[i,1]**2+0.022**2)+temperature_i[indice_temp,1]
f = open ('temp.inp', 'wb')
for j in range (0,len(temperature)):
	f.write("Cell-1.%i,		%10.4E\n" % (temperature[j,0],temperature[j,1]*0.5))
f.close()	

