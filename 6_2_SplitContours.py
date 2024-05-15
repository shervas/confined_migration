import numpy as np

f= open('nodes1.txt',"r")
lines = f.readlines()
inicio = 0
fin = 0

for i in range (0, len(lines)):

	if (lines[i] == 'NOTE\n'):
		fin = i
		break
		
print fin

f = open('nodes1.txt',)
n1 = open('nodesContour.txt', 'w')
for j, text in enumerate (f):
	if j>=inicio and j<fin:
		n1.write(text)
	else:
		pass
n1.close()

f = open('nodes1.txt',)
n2 = open('allnodes.txt', 'w')
for j, text in enumerate (f):
	if j>fin and j<len(lines):
		n2.write(text)
	else:
		pass
n2.close()

f= open('allnodes.txt',"r")
lines = f.readlines()
inicio = 0
fin = 0

for i in range (0, len(lines)):

	if (lines[i] == 'NOTE\n'):
		fin = i
		break
		
print fin

f = open('allnodes.txt',)
n1 = open('nodesNucleus.txt', 'w')
for j, text in enumerate (f):
	if j>=inicio and j<fin:
		n1.write(text)
	else:
		pass
n1.close()

f = open('allnodes.txt',)
n2 = open('InitialMesh.inp', 'w')
for j, text in enumerate (f):
	if j>fin and j<len(lines):
		n2.write(text)
	else:
		pass
n2.close()
