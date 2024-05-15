import numpy as np  #NumPy is a general-purpose array-processing package
                    #designed to efficiently manipulate large
                    #multi-dimensional arrays

from odbAccess import *
# module to have access to odb output files of Abaqus simulations

import os

import sys
#This module provides a number of functions and variables that can
#be used to manipulate different parts of the Python runtime environment

name=sys.argv[-1]; # sys.argv, contains the command-line arguments passed to the script

StepName = 'Step-3'         #Name of the step of interest

Variable = 'NT11'             #Name of the Variable 1


PartName = 'CELL-1'       #Name of the Part
nodeSetName= 'cCONCENTRATION'		# If the node set is 'all nodes', we do not need to call the nodes 
							# in the instance PartName
							


odb = openOdb(name)
Steps=odb.steps[StepName]

stepFrame=Steps.frames[-1] # last step

subset=odb.rootAssembly.instances[PartName].nodes[0]

Field=stepFrame.fieldOutputs[Variable].getSubset(position = NODAL)

fieldValues=Field.values


NameOfFile = 'temperature.txt'
FileResults = open(NameOfFile,'w')


for val in fieldValues:
	FileResults.write('%1.0f\t %10.4E\n' %(val.nodeLabel , val.data))

FileResults.close()
