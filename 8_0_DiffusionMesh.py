# #########################################
# I first change the type of elements
# #########################################

with open('mesh.inp', 'r') as file:
	filedata=file.read()

filedata=filedata.replace('CAX','DCAX')

with open('mesh_diffusion_1.inp', 'wb') as file:
  file.write(filedata)


# #########################################
# Now I remove the surface elements
# #########################################
f= open('mesh_diffusion_1.inp',"r")
lines = f.readlines()
inicio1 = 0

for i in range (0, len(lines)):

	if (lines[i] == '*Elset, elset=_Exterior_surface_S1, internal\n'):
		inicio1 = i
	else:
		i=i+1

# print inicio1
f = open('mesh_diffusion_1.inp',)
n = open('mesh_diffusion.inp', 'wb')
for j, text in enumerate (f):
	if j<inicio1:
		n.write(text)
	else:
		pass
n.close()
