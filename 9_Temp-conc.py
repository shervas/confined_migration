
import numpy as np
import scipy
from scipy.interpolate import griddata

mesh00=np.genfromtxt('initial_mesh.inp')
mesh0=np.zeros((len(mesh00),2))
mesh0[:,0]=mesh00[:,1]
mesh0[:,1]=mesh00[:,2]
mesh01=np.genfromtxt('final_mesh.inp')
mesh1=np.zeros((len(mesh01),2))
mesh1[:,0]=mesh01[:,1]
mesh1[:,1]=mesh01[:,2]


data=np.genfromtxt("temperature.txt")
temperature = data[0:len(mesh0), 1]

initial_concentration = np.genfromtxt('concentration.txt')

data = data[0:len(initial_concentration), :]
concentration_final = initial_concentration - data
concentration_final = concentration_final[:,1]


sorted_concentration = scipy.interpolate.griddata(mesh0, concentration_final, mesh1)

for i in range (0, sorted_concentration.size):
	if sorted_concentration[i]<0.00000:
		sorted_concentration[i]=0.0

f = open ('conc1.inp', 'wb')
for j in range (0,sorted_concentration.size):
	f.write("Cell-1.%i, 11, 11, %10.5E\n" % (mesh01[j,0],sorted_concentration[j]*0.5))
f.close()	

with open('conc1.inp', 'r') as file:
	filedata=file.read()
filedata=filedata.replace('NAN','0.00000E+00')
with open('conc.inp', 'w') as file:
  file.write(filedata)

interpolated_temperature = scipy.interpolate.griddata(mesh0, temperature, mesh1)
f = open ('temp1.inp', 'wb')
for j in range (0,interpolated_temperature.size):
	f.write("%i\t%10.5E\n" % (mesh01[j,0],interpolated_temperature[j]))
f.close()	

with open('temp1.inp', 'r') as file:
	filedata=file.read()
filedata=filedata.replace('NAN','0.00000E+00')
with open('interpolated_temperature.inp', 'w') as file:
  file.write(filedata)
