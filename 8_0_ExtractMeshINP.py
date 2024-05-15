import numpy as np

with open('Polymerization_1.inp','r') as file:
    filedata=file.read()
    filedata=filedata.replace('*Element, type=CAX3R\n','*Element, type=CAX3\n')
    filedata=filedata.replace('*Element, type=CAX4R\n','*Element, type=CAX4\n')
with open('Polymerization_1.inp','w') as file:
	file.write(filedata)
	
f= open('Polymerization_1.inp',"r")
lines = f.readlines()
inicio = 0
fin = 0


for i in range (0, len(lines)):

	if (lines[i] == '*Part, name=cell\n'):
		inicio = i
	
	elif (lines[i] == '*Orientation, name=Ori-1\n'):
		fin = i

	else:
		i=i+1
		

print fin
f = open('Polymerization_1.inp',)
n = open('mesh.inp', 'wb')
for j, text in enumerate (f):
	if j>inicio and j<fin:
		n.write(text)
	else:
		pass
n.close()
