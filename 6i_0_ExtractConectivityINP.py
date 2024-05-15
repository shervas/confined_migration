import shutil
import fileinput

# Var that saves the input reactions
l = []

fileToSearch = open('mesh.inp')

start_marker = '*Element, type=CAX3\n'
end_marker = '*Nset, nset=Contour'

started = False
for line in fileToSearch:
    if end_marker in line:
        started = False
    if started:
        l.append(line.strip(' \t\n\r'))
    if start_marker in line:
        started = True
fileToSearch.close()


r = len(l)


# ##############################################################

# Delete the first term of the list and the free lines

# del l[0]
l = list(filter(None, l))

# ##############################################################

# Create the new results file and write the conectivity:
outfile = open('conectivities.txt', 'w')

for index in range(len(l)):
    outfile.write(str(l[index]) + '\n')
outfile.close()

print('New conectivities.txt file completed')

with open('conectivities.txt','r') as file:
	filedata=file.read()
filedata=filedata.replace(',','\t')
with open('conectivities.txt','w') as file:
	file.write(filedata)
	
