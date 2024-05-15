import numpy as np
import shutil
import fileinput

# Var that saves the input reactions
l = []

fileToSearch = open('mesh.inp')

start_marker = '*Node'
end_marker = 'type=CAX3'

started = False
for line in fileToSearch:
    if end_marker in line:
        started = False
    if started:
        l.append(line.strip(' \t\n\r'))
    if start_marker in line:
        started = True
fileToSearch.close()
# Range of the input data file
r = len(l)

# Create the new results file and write the nodes:
outfile = open('final_mesh.inp', 'w')

for index in range(len(l)):
    outfile.write(str(l[index]) + '\n')
outfile.close()

with open('final_mesh.inp', 'r') as file:
	filedata=file.read()

filedata=filedata.replace(',',' ')

with open('final_mesh.inp', 'w') as file:
  file.write(filedata)
