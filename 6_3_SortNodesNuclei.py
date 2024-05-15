import numpy as np

connectivities= np.genfromtxt('connectivities.txt')
conec=np.delete(connectivities,0,1)
nodes_1= np.genfromtxt('nodesNucleo.txt')
nodes=nodes_1[:,0]
nodes_array=np.array(nodes)
coordinates=nodes_1
final=np.zeros((len(nodes),3))

b=np.argwhere(coordinates[:,1]<=0.01)
node_final=nodes[b[0]]
final[0,0]=nodes[b[0]]
final[0,1]=coordinates[b[0],1]
final[0,2]=coordinates[b[0],2]
print('primer node', final[0,0])

for i in range (0,len(nodes)):
	node=final[i,0]
	index=np.argwhere(conec==node) 
	index_row=index[:,0]
	matrix_potentials=conec[index_row]
	for j in range (0,np.size(matrix_potentials,0)):
		for k in range (0,np.size(matrix_potentials,1)):
			if (matrix_potentials[j,k] in nodes and np.logical_not(matrix_potentials[j,k] in final[:,0])):
				node_next=matrix_potentials[j,k]
				index_next=np.argwhere(node_next==coordinates[:,0])
				final[i+1,0]=coordinates[index_next[0,0],0]
				final[i+1,1]=coordinates[index_next[0,0],1]
				final[i+1,2]=coordinates[index_next[0,0],2]
				break

for i in range (0, len(final)):
	if final[i,1] > 5.98:
		final[i,1] = 5.98
final[0,1] = 0.0
final[-1,1] = 0.0		
print ('final', final[3,:])

f = open ('SrotedContourNucleus.inp', 'wb') 
for j in range (0,nodes.size):
	f.write("%1.3f\t%1.3f\n" % (final[j,1],final[j,2]))
f.close()	
