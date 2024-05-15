"""
Created on Mon Mar 12 12:34:06 2018

@author: shervas
"""
import sys
import os

# ###########################################################################
# G-ACTIN DIFFUSION
# ###########################################################################

abaqus job=1_diffusion.inp interactive

# Extract new G-Actin concentrations
abaqus viewer noGUI=2_Extract_nnc.py -- 1_diffusion.odb 

#Transform concentrations to change in volume
abaqus python 3_conc-temp.py 

# ###########################################################################
# F-ACTIN POLYMERIZATION
# ###########################################################################
abaqus python 4_0_Myosin.py

abaqus job=4_Polymerization.inp interactive

# ###########################################################################
# REMESH
# ###########################################################################

abaqus python 6_0_ExtractConectivityINP.py

abaqus python 6_1_ExtractContourDAT.py

abaqus python 6_2_SplitContours.py

abaqus python 6_3_SortNodes.py

abaqus python 6_3_SortNodesNuclei.py 

abaqus cae noGUI=7_P_Script_v4_150218.py

abaqus python 8_0_ExtractMeshINP.py

abaqus python 8_0_DiffusionMesh.py

abaqus python 12_FinalMesh.py

abaqus viewer noGUI=5_0_Extract_TEMP.py -- 4_Polymerization.odb ; then

python 9_Temp-conc.py

# ###########################################################################
# Start the loop
# ###########################################################################
for i in range(0,2):
    del 10_Diffusion.dat
    del 10_Diffusion.odb
    del 10_Diffusion.msg
    del 10_Diffusion.sta
    del 10_Diffusion.com
    del 10_Diffusion.prt
    del 10_Diffusion.sim
    abaqus job=10_Diffusion.inp interactive

    copy 10_Diffusion.odb z10_Diffusion_%d.odb %(i)
    copy 10_Diffusion.odb z10_Diffusion%d.dat %(i)
    copy 10_Diffusion.odb z10_Diffusion_%d.msg %(i)
    abaqus viewer noGUI=2_Extract_nnc.py -- 10_Diffusion.odb

    python 11_UpdateTemp.py

    abaqus python 11_0_Myosin.py

    del 11_Polymerization.dat
    del 11_Polymerization.odb
    del 11_Polymerization.msg
    del 11_Polymerization.sta
    del 11_Polymerization.com
    del 11_Polymerization.prt
    del 11_Polymerization.sim
    abaqus job=11_Polymerization.inp interactive

    copy 11_Polymerization.odb z11_Polymerization_%d.odb %(i)
    copy 11_Polymerization.odb z11_Polymerization_%d.dat %(i)
    copy 11_Polymerization.odb z11_Polymerization_%d.msg %(i)

    abaqus python 12_SaveInitialMesh.py

    abaqus python 6i_0_ExtractConectivityINP.py

    abaqus python 6i_1_ExtractContourDAT.py

    abaqus python 6_2_SplitContours.py

    abaqus python 6_3_SortNodes.py

    abaqus python 6_3_SortNodesNuclei.py

    abaqus cae noGUI=7_P_Script_v4_150218.py

    abaqus python 8_0_ExtractMeshINP.py

    abaqus python 12_FinalMesh.py

    abaqus python 8_0_DiffusionMesh.py

    abaqus viewer noGUI=15_0_Extract_TEMP.py -- 11_Polymerization.odb

    python 9_Temp-conc.py
    
    i=i+1
