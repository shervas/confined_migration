import shutil
import fileinput

# Var that saves the input reactions
l = []

fileToSearch = open('4_p_initial_mesh.inp')

start_marker = '*Element, type=CAX3'
end_marker = '*Nset, nset=Nucleus'

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
print('The number of nodes to apply displacement are:')
print(r)

###############################################################

# Delete the first term of the list and the free lines

# del l[0]
l = list(filter(None, l))

###############################################################

# Create the new results file and write the conectivity:
outfile = open('connectivity.txt', 'w')

for index in range(len(l)):
    outfile.write(str(l[index]) + '\n')
outfile.close()

print('New connectivity.txt file completed')

with open('connectivity.txt','r') as file:
	filedata=file.read()
filedata=filedata.replace(',','\t')
with open('connectivity.txt','w') as file:
	file.write(filedata)
