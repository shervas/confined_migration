# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 10:15:16 2018

@author: shervas
"""
import numpy as np

f= open('4_p_initial_mesh.inp',"r")
lines = f.readlines()
start = 0
end = 0

for i in range (0, len(lines)):

	if (lines[i] == '*Nset, nset=Myosin\n'):
		start = i
	if (lines[i] == '*Elset, elset=Myosin\n'):
		end = i
   	

f = open('4_p_initial_mesh.inp',)
n1 = open('nodesMyosin0.txt', 'w')
for j, text in enumerate (f):
	if j>start and j<end:
		n1.write(text)
	else:
		pass
n1.close()

with open('nodesMyosin0.txt', 'r') as file:
	filedata=file.read()

filedata=filedata.replace(',','\n')

with open('nodesMyosin0.txt', 'wb') as file:
  file.write(filedata)
  

f = open('4_p_initial_mesh.inp',)
n1 = open('InitialMyosinMesh.txt', 'w')
for j, text in enumerate (f):
	if j>=0 and j<6638:
		n1.write(text)
	else:
		pass
n1.close()

with open('InitialMyosinMesh.txt', 'r') as file:
	filedata=file.read()

filedata=filedata.replace(',','\t')

with open('InitialMyosinMesh.txt', 'wb') as file:
  file.write(filedata)
             
nodes_myosin = np.genfromtxt('nodesMyosin0.txt')
nodes_1= np.genfromtxt('InitialMyosinMesh.txt')

nodes = nodes_1[:,0]
nodes_array = np.array(nodes)
coordinates = nodes_1
coord_0 = 12.5
myosin = np.zeros((len(nodes_myosin),3))

for i in range(0, len(nodes_myosin)):
    index = np.argwhere(coordinates[:,0]==nodes_myosin[i])
    myosin[i,0] = nodes_myosin[i]
    myosin[i,1] = coordinates[index,1]
    myosin[i,2] = coordinates[index,2]

range_myosin = np.zeros((len(myosin),4))
range_myosin[:,0] = myosin[:,0]
range_myosin[:,1] = myosin[:,1]
range_myosin[:,2] = myosin[:,2]

for i in range(0,len(nodes_myosin)):
    range_myosin[i,3] = myosin[i,2] - coord_0

temperature = np.zeros((len(nodes_myosin),2))
temperature[:,0] = myosin[:,0]
temperature[:,1] = range_myosin[:,3]*(0.04)

f = open ('tempmyosin.inp', 'wb')
for j in range (0,len(nodes_myosin)):
	f.write("Cell-1.%i,		%10.4E\n" % (temperature[j,0],temperature[j,1]*0.5))
f.close()	
