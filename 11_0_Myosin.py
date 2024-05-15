# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 10:15:16 2018

@author: shervas
"""
import numpy as np

f= open('mesh.inp',"r")
lines = f.readlines()
inicio = 0
fin = 0

for i in range (0, len(lines)):

	if (lines[i] == '*Nset, nset=myosin\n'):
		inicio = i
	if (lines[i] == '*Elset, elset=myosin, generate\n') or (lines[i] == '*Elset, elset=myosin\n'):
		fin = i
   	

f = open('mesh.inp',)
n1 = open('nodesmyosin.txt', 'w')
for j, text in enumerate (f):
	if j>inicio and j<fin:
		n1.write(text)
	else:
		pass
n1.close()

with open('nodesmyosin.txt', 'r') as file:
	filedata=file.read()

filedata=filedata.replace(',','\n')

with open('nodesmyosin.txt', 'wb') as file:
  file.write(filedata)
  
             
nodes_myosin = np.genfromtxt('nodesmyosin.txt')
nodes_1= np.genfromtxt('mesh_final.inp')
nodes = nodes_1[:,0]
nodes_array = np.array(nodes)
coordinates = nodes_1
nodes_nucleus = np.genfromtxt('nodesNucleus.txt')
coord_0 = nodes_nucleus[:,2].min()
myosin = np.zeros((len(nodes_myosin),3))

for i in range(0, len(nodes_myosin)):
    indice = np.argwhere(coordinates[:,0]==nodes_myosin[i])
    myosin[i,0] = nodes_myosin[i]
    myosin[i,1] = coordinates[indice,1]
    myosin[i,2] = coordinates[indice,2]

myosin_threshold = np.zeros((len(myosin),4))
myosin_threshold[:,0] = myosin[:,0]
myosin_threshold[:,1] = myosin[:,1]
myosin_threshold[:,2] = myosin[:,2]

for i in range(0,len(nodes_myosin)):
    myosin_threshold[i,3] = myosin[i,2] - coord_0

temperature = np.zeros((len(nodes_myosin),2))
temperature[:,0] = myosin[:,0]
temperature[:,1] = myosin_threshold[:,3]*(0.05)

f = open ('tempmyosin.inp', 'wb')
for j in range (0,len(nodes_myosin)):
	f.write("Cell-1.%i,		%10.4E\n" % (temperature[j,0],temperature[j,1]*0.5))
f.close()	
