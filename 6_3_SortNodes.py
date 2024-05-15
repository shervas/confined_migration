import numpy as np;

connectivity= np.genfromtxt('connectivity.txt');
conec=np.delete(connectivity,0,1);
nodes_1= np.genfromtxt('nodesContour.txt');
nodes=nodes_1[:,0];
nodes_array=np.array(nodes);
coordinates=nodes_1;
final=np.zeros((len(nodes),3))


#Looking for the highest and closest to the x-axis.
max_y=coordinates[:,2].max()
max=max_y-1
highest = np.zeros((len(nodes),3))
for i in range (0, len(nodes)):
    if nodes_1[i,2] > max:
        highest[i]=nodes_1[i,:]

delete_null=np.argwhere(highest==0)
highest=np.delete(highest,delete_null,0)        
ind= np.argwhere(coordinates == highest[:,1].min())

ending_node=coordinates[ind[0,0],0]
final[0,0]=ending_node
final[0,1]=coordinates[ind[0,0],1]
final[0,2]=coordinates[ind[0,0],2]
print('first node', final[0,0])

#We found the corner

#looks for which node has connectivity to the first node:
for i in range (0,len(nodes)-1):
	node=final[i,0]
	index=np.argwhere(conec==node)
	index_fila=index[:,0]
	matrix_potential=conec[index_fila]
	 #which appears in another row with the first one and appears in vector_potential
	 #of the possible_vector has to be the one that appears in vector
	distances = np.zeros((np.size(matrix_potential),2))
	index0=np.argwhere(coordinates[:,0]==node)
	coord_x0 = coordinates[index0,1]		
	coord_y0 = coordinates[index0,2]
	counter=0
	for j in range (0,np.size(matrix_potential,0)):
		for k in range (0,np.size(matrix_potential,1)):
			counter=counter+1            			
			if (matrix_potential[j,k] in nodes and np.logical_not(matrix_potential[j,k] in final[:,0])):
				node_next = matrix_potential[j,k]
				index_n = np.argwhere(coordinates[:,0]==node_next)
				coord_x = coordinates[index_n,1]		
				coord_y = coordinates[index_n,2]
				distance = ((coord_x-coord_x0)**2+(coord_y-coord_y0)**2)**0.5   
				distances[counter-1,0]=node_next
				distances[counter-1,1]=distance
	distances = distances[~np.all(distances == 0, axis=1)]
	if ((len(distances) > 1)):
		index_c = np.argwhere(distances == np.min(distances[:,1]))
		node_next = distances[index_c[0,0],0]
	else:  
		node_next = node_next  
	index_next = np.argwhere(np.unique(node_next) == coordinates[:,0])
	final[i+1,0]=coordinates[index_next[0,0],0]
	final[i+1,1]=coordinates[index_next[0,0],1]
	final[i+1,2]=coordinates[index_next[0,0],2]
				
#stores it in the final matrix
#we bring to 5.98 anything that may have stood out
for i in range (0, len(final)):
	if final[i,1] > 5.98:
		final[i,1] = 5.98

#We bring everything that may have been moved to the axis.		
for i in range (0, len(final)):
	if final[i,1] < 0.00:
		final[i,1] = 0.000

contour = np.delete(final,0,1)	
contour = contour[~np.all(contour == 0, axis=1)]

f = open ('SortedContour.inp', 'wb') 
for j in range (0,len(contour)):
	f.write("%1.3f\t%1.3f\n" % (contour[j,0],contour[j,1]))
f.close()

#We check if there is a node that does not connect with the one below in the vertical.
vertical = np.argwhere(contour[:,0]>5.7)
if len(vertical)!=0:
    for i in range (vertical[0],vertical[-1]):
        coord_y = contour[i,1]
        coord_y2 = contour[i+1,1]
        if (coord_y2>coord_y):
            contour = np.delete(contour, np.s_[i],axis=0)

#Avoid the wrinkles
#To do this we will only look at the area where the x is less than 5.5 and there we will order the nodes according to their Euclidean distance.

location = np.argwhere(contour[:,0]<5.3)
#Donde esta nuestro intervalo? donde hay un salto de los nodes
zone = np.zeros(len(location))
for i in range (0,len(location)-1):
    node1=location[i]
    node2=location[i+1]
    if node2-node1>1:
        zone[i] = i+1
for i in range (0,len(zone)):
    if zone[i]!=0:
        zone[i] = location[(zone[i].astype(np.int64))]
locations = np.argwhere(zone[:]!=0)
if len(locations)>1:
    a = locations[1].astype(np.int64)+1-locations[0].astype(np.int64)
    wrinkl = np.zeros((a[0]+1,2))
    for i in range (0,len(wrinkl)):
        wrinkl[i] = contour[zone[locations[0]].astype(np.int64)+i-1,:]

    if (len(wrinkl)<2):
        a=1
    else:
        #Only enter if there is a point deep inside
        if ((wrinkl[:,0]<5.3).any()):
            filas_contour=len(wrinkl) 
            wrinkl = np.c_[ np.arange(len(wrinkl)),wrinkl]
            for i in range (0,len(wrinkl)-1):
                distances = np.zeros((100,3)) 
                node = wrinkl[i,0]
                for j in range (0,len(wrinkl)):
                    node2 = wrinkl[j,0]
                    distance = ((wrinkl[j,1]-wrinkl[i,1])**2+(wrinkl[j,2]-wrinkl[i,2])**2)**0.5  
                    distances [j,0] = node
                    distances [j,1] = node2
                    distances [j,2] = distance
                distances = np.delete(distances, np.s_[0:i+1],axis=0)    
                distances = distances[~(distances==0).all(1)]

                wrinkl = wrinkl[~((wrinkl[i,2]<wrinkl[:,2]))]
                a = np.argwhere(distances[:,2]==(distances[:,2].min()))
                if (a!=0):
                    wrinkl = np.delete(wrinkl, np.s_[i+1:np.asscalar(a-1)], axis=0)
                    break 
            
            #contour without wrinkls
            wrinkl = np.delete(wrinkl,0,1)
            start = zone[locations[0]].astype(np.int64)
            fin = filas_contour
            for i in range(0,len(wrinkl)):
                contour[i+start,0]=wrinkl[i,0]
                contour[i+start,1]=wrinkl[i,1]
            contour = np.delete(contour, np.s_[np.asscalar(start+len(wrinkl)):np.asscalar(start+fin)],axis=0)
            
            f = open ('SortedContour.inp', 'wb') 
            for j in range (0,len(contour)):
            	f.write("%1.3f\t%1.3f\n" % (contour[j,0],contour[j,1]))
            f.close()	
