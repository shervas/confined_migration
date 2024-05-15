#-------------------------------------------------------------------------------
#
# File      : Script_v1_130218.py
# Date      : February 13, 2018
# Created by: Silvia Hervas Raluy
#
#-------------------------------------------------------------------------------

import numpy as np
from abaqus import *
from abaqusConstants import *
backwardCompatibility.setValues(includeDeprecated=True,reportDeprecated=False)
 
contour=np.genfromtxt('SortedContour.inp')
# contour=np.genfromtxt('contour.inp')
contour_y=contour[:,1]
max_y=contour_y.max()
min_y=contour_y.min()
medio=(max_y+min_y)/2
contour_Nucleus=np.genfromtxt('SortedContourNucleus.inp')
contour_yn=contour_Nucleus[:,1]
max_yn=contour_yn.max()
min_yn=contour_yn.min()
medio_n=(max_yn+min_yn)/2
zeta=np.zeros((contour.shape[0],1))
contour_zeta =np.concatenate((contour, zeta),axis=1)


#Create a model
#
myModel = mdb.Model(name='Model-1')

#
#Create a  new viewport
#
myViewport = session.Viewport(name='Cell_test1', origin=(0.0, 0.0), width=150, height=120)
myViewport.makeCurrent()
myViewport.maximize()
#
#------------------------------------
# T U B E   P A R T
#------------------------------------
#
mySketch = myModel.Sketch(name='Tube', sheetSize=500.0)
mySketch.sketchOptions.setValues(viewStyle=AXISYM)
mySketch.setPrimaryObject(option=STANDALONE)

mySketch.ObliqueConstructionLine(point1=(0.0, -250.0),   point2=(0.0, 250.0))
mySketch.Line(point1=(5.98,-50.), point2=(5.98,50.))

myPartTube = myModel.Part(name='tube', dimensionality=AXISYMMETRIC, type=DISCRETE_RIGID_SURFACE)
myPartTube.BaseWire(sketch=mySketch)
mySketch.unsetPrimaryObject()
myViewport.setValues(displayedObject=myPartTube)

v1=myPartTube.vertices
myPartTube.ReferencePoint(point=v1.findAt(coordinates=(5.98, -50.0, 0.0)))
#
#------------------------------------
# C E L L   P A R T
#------------------------------------
#
import part
#
#Create sketch
#
myModel.convertAllSketches()

mySketch = myModel.Sketch(name='CellProfile', sheetSize=500.0)
mySketch.sketchOptions.setValues(viewStyle=AXISYM)
mySketch.setPrimaryObject(option=STANDALONE)

mySketch.ObliqueConstructionLine(point1=(0.0, -250.0),   point2=(0.0, 250.0))
mySketch.Line(point1=contour[0,:], point2=contour[-1,:])
for i in range (0, len(contour)-1):
	mySketch.Line(point1=contour[i,:], point2=contour[i+1,:])


myPart = myModel.Part(name='cell', dimensionality=AXISYMMETRIC, type=DEFORMABLE_BODY)
# ########## To check the sketch in case there is an error uncomment the following line
#myModel.convertAllSketches()

myPart.BaseShell(sketch=mySketch)
mySketch.unsetPrimaryObject()
myViewport.setValues(displayedObject=myPart)

e = myPart.edges
x_0 = contour[0,0]; y_0 = contour[0,1]
x_1 = contour[1,0]; y_1 = contour[1,1]
x = (x_1 - x_0)/2 + x_0
if (x_1 - x_0 !=0):
	y = y_0+((y_1-y_0)/(x_1-x_0))*(x-x_0)
	edges = e.findAt(((x, y, 0.0), ),)
	edges = edges + e.findAt(((contour[0,0], contour[0,1], 0.0), ),)
	
else:
	edges = e.findAt(((contour[0,0], contour[0,1], 0.0), ),)

for i in range (1,len(contour)):
	edges = edges + e.findAt(((contour[i,0], contour[i,1], 0.0), ),)
myPart.Set(edges=edges, name='contour')

s = myPart.edges
side1Edges = s.findAt(((contour[0,0], contour[0,1], 0.0), ), )
for i in range (0,len(contour)-1):
	side1Edges = side1Edges + s.findAt(((contour[i,0], contour[i,1], 0.0), ),)
myPart.Surface(side1Edges=side1Edges, name='Exterior_surface')
#
#------------------------------------
# C E L L   P A R T	I T I O N S
#------------------------------------
#
#-----------------------------------------------------------------
#Medio
#-----------------------------------------------------------------
f = myPart.faces.findAt((3.0,medio_n,0.0))
t = myPart.MakeSketchTransform(sketchPlane=f,
    sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
mySketch = myModel.ConstrainedSketch(name='medio', sheetSize=848.52, 
    gridSpacing=21.21, transform=t)
mySketch.setPrimaryObject(option=SUPERIMPOSE)
myPart.projectReferencesOntoSketch(sketch=mySketch,
    filter=COPLANAR_EDGES)
mySketch.sketchOptions.setValues(gridOrigin=(0.0, 0.0))
mySketch.Line(point1=(0.0,medio_n),point2=(6.0,medio_n))
pickedFaces = myPart.faces.findAt((3.0,medio_n,0.0))
f = myPart.faces

myPart.PartitionFaceBySketch(faces=f, sketch=mySketch)
mySketch.unsetPrimaryObject()
del myModel.sketches['medio']

#------------------------------------------------------------------
#Nucleus
#------------------------------------------------------------------
#
f = myPart.faces.findAt((0.2,medio,0.0))
t = myPart.MakeSketchTransform(sketchPlane=f,
    sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
mySketch = myModel.ConstrainedSketch(name='Nucleus', sheetSize=848.52, 
    gridSpacing=21.21, transform=t)
mySketch.setPrimaryObject(option=SUPERIMPOSE)
myPart.projectReferencesOntoSketch(sketch=mySketch,
    filter=COPLANAR_EDGES)
mySketch.sketchOptions.setValues(gridOrigin=(0.0, 0.0))
mySketch.Spline(points=(contour_Nucleus[:,:]))
mySketch.Line(point1=contour_Nucleus[0,:], point2=contour_Nucleus[-1,:])
pickedFaces = myPart.faces.findAt((3.0,medio,0.0))
f = myPart.faces

myPart.PartitionFaceBySketch(faces=f, sketch=mySketch)
mySketch.unsetPrimaryObject()
del myModel.sketches['Nucleus']

puntonx=contour_Nucleus[4,0]; puntony=contour_Nucleus[4,1]
puntonx2=contour_Nucleus[len(contour_Nucleus)-5,0]; puntony2=contour_Nucleus[len(contour_Nucleus)-5,1]
e = myPart.edges
edges = e.findAt(((puntonx, puntony, 0.0), ),((puntonx2, puntony2, 0.0), ), )
myPart.Set(edges=edges, name='contourNucleus')
#-------------------------------------------------------------------
#Front
#-------------------------------------------------------------------
#
f = myPart.faces.findAt((0.05,max_y-1,0.0))
t = myPart.MakeSketchTransform(sketchPlane=f,
    sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
mySketch = myModel.ConstrainedSketch(name='Front', sheetSize=848.52, 
    gridSpacing=21.21, transform=t)
mySketch.setPrimaryObject(option=SUPERIMPOSE)
myPart.projectReferencesOntoSketch(sketch=mySketch,
    filter=COPLANAR_EDGES)
mySketch.sketchOptions.setValues(gridOrigin=(0.0, 0.0))
mySketch.Line(point1=(0.0, max_y-2.0), point2=(6.0, max_y-2))
pickedFaces = myPart.faces.findAt((0.2,max_y-0.01,0.0))
f = myPart.faces

myPart.PartitionFaceBySketch(faces=f, sketch=mySketch)
mySketch.unsetPrimaryObject()
del myModel.sketches['Front']
#
#-------------------------------------------------------------------
#Adherent
#-------------------------------------------------------------------
#
#I make a contour of the Adherent at 0.5 of the normal contour on the x-axis.
#I leave only the nodes where the Adherent will go (above).

contour_Adherent=np.zeros((len(contour),2))
contour_Adherent[:,0]=contour[:,0]-0.3
contour_Adherent[:,1]=contour[:,1]
delete = np.zeros(len(contour_Adherent))

f = myPart.faces.findAt((2,max_yn+2,0.0))
t = myPart.MakeSketchTransform(sketchPlane=f,
    sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
mySketch = myModel.ConstrainedSketch(name='Adherent', sheetSize=848.52, 
    gridSpacing=21.21, transform=t)
mySketch.setPrimaryObject(option=SUPERIMPOSE)
myPart.projectReferencesOntoSketch(sketch=mySketch,
    filter=COPLANAR_EDGES)
mySketch.sketchOptions.setValues(gridOrigin=(0.0, 0.0))

for i in range (0, len(contour_Adherent)-1):
	mySketch.Line(point1=(contour_Adherent[i,:]), point2=(contour_Adherent[i+1,:]))

a = len(contour_Adherent)/4
pickedFaces = myPart.faces.findAt(((contour_Adherent[a,0]+0.15,contour_Adherent[a,1],0.0),),)
f = myPart.faces
myModel.convertAllSketches()
myPart.PartitionFaceBySketch(faces=pickedFaces, sketch=mySketch)
mySketch.unsetPrimaryObject()
#
#
#-------------------------------------------------------------------
#Front2
#-------------------------------------------------------------------
#
f = myPart.faces.findAt((0.05,max_y-1,0.0))
t = myPart.MakeSketchTransform(sketchPlane=f,
    sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
mySketch = myModel.ConstrainedSketch(name='Front2', sheetSize=848.52, 
    gridSpacing=21.21, transform=t)
mySketch.setPrimaryObject(option=SUPERIMPOSE)
myPart.projectReferencesOntoSketch(sketch=mySketch,
    filter=COPLANAR_EDGES)
mySketch.sketchOptions.setValues(gridOrigin=(0.0, 0.0))
mySketch.Line(point1=(0.0, max_y-6.5), point2=(6.0, max_y-6.5))
pickedFaces = myPart.faces.findAt((0.2,max_y-1.,0.0))
f = myPart.faces

myPart.PartitionFaceBySketch(faces=f, sketch=mySketch)
mySketch.unsetPrimaryObject()
del myModel.sketches['Front2']

#-------------------------------------------------------------------
#Myosin
#-------------------------------------------------------------------
#
f = myPart.faces.findAt((0.1,min_yn-2,0.0))
t = myPart.MakeSketchTransform(sketchPlane=f,
    sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
mySketch = myModel.ConstrainedSketch(name='Myosin', sheetSize=848.52, 
    gridSpacing=21.21, transform=t)
mySketch.setPrimaryObject(option=SUPERIMPOSE)
myPart.projectReferencesOntoSketch(sketch=mySketch,
    filter=COPLANAR_EDGES)
mySketch.sketchOptions.setValues(gridOrigin=(0.0, 0.0))
mySketch.Line(point1=(0.0, min_yn), point2=(6.0, min_yn))
pickedFaces = myPart.faces.findAt((0.1,min_yn-2,0.0))
f = myPart.faces

myPart.PartitionFaceBySketch(faces=f, sketch=mySketch)
mySketch.unsetPrimaryObject()
del myModel.sketches['Myosin']
#
#-------------------------------------------------------------------
#g-actin-0
#-------------------------------------------------------------------
#
f = myPart.faces.findAt((3, max_yn-0.1,0.0))
t = myPart.MakeSketchTransform(sketchPlane=f,
    sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
mySketch = myModel.ConstrainedSketch(name='g-actin-0', sheetSize=848.52, 
    gridSpacing=21.21, transform=t)
mySketch.setPrimaryObject(option=SUPERIMPOSE)
myPart.projectReferencesOntoSketch(sketch=mySketch,
    filter=COPLANAR_EDGES)
mySketch.sketchOptions.setValues(gridOrigin=(0.0, 0.0))
mySketch.Line(point1=(0.0, max_yn), point2=(6.0, max_yn))
pickedFaces = myPart.faces.findAt((3,max_yn-0.1,0.0))
f = myPart.faces

myPart.PartitionFaceBySketch(faces=f, sketch=mySketch)
mySketch.unsetPrimaryObject()
del myModel.sketches['g-actin-0']
#
#-------------------------------------------------------------------
##g-actin-source
#-------------------------------------------------------------------
#
f = myPart.faces.findAt((3.,max_yn+1,0.0))
t = myPart.MakeSketchTransform(sketchPlane=f,
    sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
mySketch = myModel.ConstrainedSketch(name='#g-actin-source', sheetSize=848.52, 
    gridSpacing=21.21, transform=t)
mySketch.setPrimaryObject(option=SUPERIMPOSE)
myPart.projectReferencesOntoSketch(sketch=mySketch,
    filter=COPLANAR_EDGES)
mySketch.sketchOptions.setValues(gridOrigin=(0.0, 0.0))
mySketch.Line(point1=(0.0, max_yn+3.2), point2=(6.0, max_yn+3.2))
pickedFaces = myPart.faces.findAt((3.,max_yn+1,0.0))
f = myPart.faces

myPart.PartitionFaceBySketch(faces=f, sketch=mySketch)
mySketch.unsetPrimaryObject()
del myModel.sketches['#g-actin-source']
#
#-------------------------------------------------------------------
#g-actin-rounded
#-------------------------------------------------------------------
#
f = myPart.faces.findAt((0.1,max_yn+1.,0.0))
t = myPart.MakeSketchTransform(sketchPlane=f,
    sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
mySketch = myModel.ConstrainedSketch(name='#g-actin-rounded', sheetSize=848.52, 
    gridSpacing=21.21, transform=t)
mySketch.setPrimaryObject(option=SUPERIMPOSE)
myPart.projectReferencesOntoSketch(sketch=mySketch,
    filter=COPLANAR_EDGES)
mySketch.sketchOptions.setValues(gridOrigin=(0.0, 0.0))
mySketch.Line(point1=(5.0, max_yn), point2=(2.5, max_yn+3.2))
pickedFaces = myPart.faces.findAt((0.1,max_yn+1,0.0))


myPart.PartitionFaceBySketch(faces=pickedFaces, sketch=mySketch)
mySketch.unsetPrimaryObject()
del myModel.sketches['#g-actin-rounded']
#
#------------------------------------
# M A T E R I A L 
#------------------------------------
#
import material
myMaterialNucleus = myModel.Material(name='mat_Nucleus')
elasticProperties_n=(8.,0.38)
myMaterialNucleus.Elastic(table=(elasticProperties_n,))
myMaterialcytoplasmIso = myModel.Material(name='mat_cito_iso')
elasticProperties_c=(0.8,0.38)
myMaterialcytoplasmIso.Elastic(table=(elasticProperties_c,))
myMaterialcytoplasmIso.Expansion(table=((1.0, ), ))
myMaterialcytoplasmOrto = myModel.Material(name='mat_cito_orto')
elasticProperties_c=(0.8,0.38)
myMaterialcytoplasmOrto.Elastic(table=(elasticProperties_c,))
myMaterialcytoplasmOrto.Expansion(type=ORTHOTROPIC, table=((0.0, 1.0, 0.0), ))
#
#------------------------------------
# S E C C I O N
#------------------------------------
#
import section

mySection=myModel.HomogeneousSolidSection(name='cytoplasm_iso',material='mat_cito_iso',thickness=1.0)
mySection=myModel.HomogeneousSolidSection(name='cytoplasm_orto',material='mat_cito_orto',thickness=1.0)
mySection=myModel.HomogeneousSolidSection(name='Nucleus',material='mat_Nucleus',thickness=1.0)
#
#------------------------------------
# S E C C I O N   A S S I G N M E N T
#------------------------------------
#
myFaces=myPart.faces
all = myPart.Set(faces=myFaces, name='all')

f = myPart.faces
faces1 = f.findAt(((0.1,medio_n+1,0.),),((0.1,medio_n-1,0.),),)
Nucleus = myPart.Set(faces=faces1, name='Nucleus')
myPart.SectionAssignment(region=Nucleus, sectionName='Nucleus')
#
f = myPart.faces
faces2 = f.findAt(((2.0,max_yn + 4.,0.),),((2.0,max_y -1,0.),),((1.0,max_y -5,0.),))
Front = myPart.Set(faces=faces2, name='FreeActin')
myPart.SectionAssignment(region=Front, sectionName='cytoplasm_orto')
#
for i in range(0,len(contour_Adherent)):
	if ((contour_Adherent[i,1] < medio_n) or (contour_Adherent[i,1] > max_y-2.0)):
		delete[i] = i 
delete = np.delete(delete, np.argwhere(delete==0.0),0)
contour_Adherent = np.delete(contour_Adherent, delete, 0)		
contour_Adherent = np.delete(contour_Adherent, 0, 0)	
f = myPart.faces
faces3 = f.findAt(((contour_Adherent[0,0]+0.1,contour_Adherent[0,1],0.0),),)
for i in range (1,len(contour_Adherent)):
	if (contour_Adherent[i,0] > 5.5) and (contour_Adherent[i,1]>medio_n):
		faces3 = faces3 + f.findAt(((contour_Adherent[i,0]+0.1,contour_Adherent[i,1],0.0),),)
Adherent = myPart.Set(faces=faces3, name='AdherentActin')
myPart.SectionAssignment(region=Adherent, sectionName='cytoplasm_iso')
#
f = myPart.faces
faces4 = f.findAt(((2.0,min_yn-1.0,0.),),((5.97, min_yn-1.0,0.),),)
Myosin = myPart.Set(faces=faces4, name='Myosin')
myPart.SectionAssignment(region=Myosin, sectionName='cytoplasm_iso')
#
f = myPart.faces
faces5 = f.findAt(((2.0,max_yn + 1.,0.),),((4.0,max_yn + 3.1,0.),),)
resto = myPart.Set(faces=faces5, name='GActinSource')
myPart.SectionAssignment(region=resto, sectionName='cytoplasm_iso')
#
f = myPart.faces
faces5 = f.findAt(((3,max_yn-0.1,0.0),),)
resto = myPart.Set(faces=faces5, name='GActinaNull')
myPart.SectionAssignment(region=resto, sectionName='cytoplasm_orto')
#
f = myPart.faces
faces5 = f.findAt(((0.1,max_yn+1.,0.0),),)
resto = myPart.Set(faces=faces5, name='GActinRounded')
#
f = myPart.faces
faces5 = f.findAt(((0.1,max_y-5.,0.0),),)
resto = myPart.Set(faces=faces5, name='Front2')
#
f = myPart.faces
faces5 = f.findAt(((0.1,max_y-1.,0.0),),((5.97, max_y-0.1,0.),),)
resto = myPart.Set(faces=faces5, name='Front1')
#
Front=myPart.SetByBoolean(name='Front', operation=UNION, sets=(myPart.sets['Front1'], myPart.sets['Front2'],))		
#Resto
resto2=myPart.SetByBoolean(name='all_iso', operation=DIFFERENCE, sets=(myPart.sets['all'], 
	myPart.sets['AdherentActin'], myPart.sets['FreeActin'], myPart.sets['contour'], 
	myPart.sets['contourNucleus'], myPart.sets['GActinaNull'], 
	myPart.sets['GActinSource'], myPart.sets['Myosin'], myPart.sets['Nucleus'],
	myPart.sets['Front']))
myPart.SectionAssignment(region=resto2, sectionName='cytoplasm_iso')
concent=myPart.SetByBoolean(name='concentration', operation=UNION, sets=(myPart.sets['FreeActin'], myPart.sets['GActinSource'],))
mat_orto=myPart.SetByBoolean(name='mat_orto', operation=DIFFERENCE, sets=(myPart.sets['concentration'], myPart.sets['Front']))
#
#Assign Material Orientation
#
region = myPart.sets['all']
orientation=None
myPart.MaterialOrientation(region=region, 
    orientationType=GLOBAL, axis=AXIS_3, 
	additionalRotationType=ROTATION_NONE, localCsys=None, fieldName='', 
	stackDirection=STACK_3)
#
#------------------------------------
# A S S E M B L Y 
#------------------------------------
#
import assembly
myAssembly = myModel.rootAssembly
myInstance = myAssembly.Instance(name='Cell-1', part=myPart, dependent=ON)

myInstanceTube = myAssembly.Instance(name='tube', part=myPartTube, dependent=ON)

#--------------------------------------
# M E S H
#--------------------------------------
#
import mesh
# Assign an element type to the part instance

# MeshTube
myPartTube.seedPart(size=2.0, deviationFactor=0.1, minSizeFactor=0.1)
myPartTube.generateMesh()

p1 = mdb.models['Model-1'].parts['tube']
e = p1.edges
edges = e.findAt(((5.98, -25.0, 0.0), ))
r = p1.referencePoints
refPoints=(r[2], )
p1.Set(edges=edges, referencePoints=refPoints, name='Master')

p1 = mdb.models['Model-1'].parts['tube']
session.viewports['Cell_test1'].setValues(displayedObject=p1)
p1 = mdb.models['Model-1'].parts['tube']
s = p1.edges
side1Edges = s.findAt(((5.98, -25.0, 0.0), ))
p1.Surface(side1Edges=side1Edges, name='Master_surface')

# Mesh cell
elemType2 = mesh.ElemType(elemCode=CAX3, elemLibrary=STANDARD, 
	secondOrderAccuracy=OFF, distortionControl=DEFAULT)

f = myPart.faces
faces = f.findAt(((2., max_y-1, 0.0), ), ((5.75, max_y-1.5, 0.0), ), 
	((2., max_y-2.5, 0.0), ),((5.75, max_y-2.5, 0.0), ), ((2., medio_n+0.1, 0.0), ), 
	((5.5, max_yn-0.1, 0.0), ), ((5.75, medio_n+1.0, 0.0), ),((2., medio_n-1, 0.0), ),
	((5.5, min_yn+0.1, 0.0), ),((5.75, medio_n-1, 0.0), ), ((2., min_y+1, 0.0), ),
	((5.75, min_yn-0.1, 0.0), ),((2., max_yn+0.5, 0.0), ),((5.75, max_yn+0.5, 0.0), ),((2., max_yn+4.1, 0.0), ), 
	((5.97,max_y-3.0,0.),),((5.97,medio+3.0,0.),),((5.97,max_yn+1.0,0.),),((5.97,max_yn-1.0,0.),),((4,max_yn+3.1,0.),)) 

for i in range (1,len(contour_Adherent)):
	faces = faces + f.findAt(((contour_Adherent[i,0]+0.2,contour_Adherent[i,1],0.0),),)
pickedRegions =(faces, )
myPart.setElementType(regions=pickedRegions, elemTypes=(elemType2, ))
f = myPart.faces
pickedRegions = f.findAt(((2., max_y-1, 0.0), ), ((5.75, max_y-1.5, 0.0), ), 
	((2., max_y-2.5, 0.0), ),((5.75, max_y-2.5, 0.0), ), ((2., medio_n+0.1, 0.0), ), 
	((5.5, max_yn-0.1, 0.0), ), ((5.75, medio_n+1.0, 0.0), ),((2., medio_n-1, 0.0), ),
	((5.5, min_yn+0.1, 0.0), ),((5.75, medio_n-1, 0.0), ), ((2., min_y+1, 0.0), ),
	((5.75, min_yn-0.1, 0.0), ),((2., max_yn+0.5, 0.0), ),((5.75, max_yn+0.5, 0.0), ),((2., max_yn+4.1, 0.0), ), 
	((5.97,max_y-3.0,0.),),((5.97,medio+3.0,0.),),((5.97,max_yn+1.0,0.),),((5.97,max_yn-1.0,0.),),((3,max_yn-0.1,0.0),),)   
for i in range (1,len(contour_Adherent)):
	pickedRegions = pickedRegions + f.findAt(((contour_Adherent[i,0]+0.2,contour_Adherent[i,1],0.0),),((4,max_yn+3.1,0.),)) 
myPart.setMeshControls(regions=pickedRegions, elemShape=TRI, allowMapped=False)

myPart.seedPart(size=0.25, deviationFactor=0.1, minSizeFactor=0.1)

myPart.generateMesh()
#------------------------------------
# J O B 
#------------------------------------
#
import job
#Create an analysis job for the model
jobName = 'Polymerization_1'
myJob = mdb.Job(name=jobName, model='Model-1')
myJob.writeInput(consistencyChecking=OFF)
session.viewports['Cell_test1'].setValues(displayedObject=myPart)
session.viewports['Cell_test1'].partDisplay.meshOptions.setValues(meshTechnique=ON)
