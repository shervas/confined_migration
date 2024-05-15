import numpy as np


f= open('mesh.inp',"r")
lines = f.readlines()
inicio1 = 0

for i in range (0, len(lines)):

	if (lines[i] == '*Element, type=CAX3\n'):
		inicio1 = i
	else:
		i=i+1

f = open('mesh.inp',)
n = open('initial_mesh.inp', 'wb')
for j, text in enumerate (f):
	if j>0 and j<inicio1:
		n.write(text)
	else:
		pass
n.close()

with open('initial_mesh.inp', 'r') as file:
	filedata=file.read()

filedata=filedata.replace(',',' ')

with open('initial_mesh.inp', 'w') as file:
  file.write(filedata)
