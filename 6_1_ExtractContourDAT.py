import shutil
import sys
import fileinput
#try:
# Var that saves the input reactions
l = []

# File to read displacements in the gel domain
# P.D. Not taking into account the nodes of the cell contour
fileToSearch = open('4_Polymerization.dat')

start_marker = '       NODE FOOT-   COOR1       COOR2'
end_marker = 'MAXIMUM'
print start_marker, end_marker
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
print('The number of nodes is:')
print(r)

# ##############################################################

# Delete the first term of the list and the free lines

del l[0]
l = list(filter(None, l))

# ###############################################################

# Create the new results file and write:
outfile = open('nodes1.txt', 'w')

for index in range(len(l)):
    outfile.write(str(l[index]) + '\n')
outfile.close()

print('New nodes1.txt file completed')
