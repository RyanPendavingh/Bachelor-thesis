#assessment part 1 (pc, profit, Mac)

from pylab import *
from prody import *
import subprocess
import sys
import os
import shutil

if len(sys.argv) != 5:
    print 'Usage: ' + sys.argv[0] + ' <case> <docking run> <refcomp chain 1> <refcomp chain 2>'


CASE = sys.argv[1]
RUN = sys.argv[2]
REFCOMP_CHAIN1 = sys.argv[3]
REFCOMP_CHAIN2 = sys.argv[4]
MODELS_CHAIN1 = 'A'
MODELS_CHAIN2 = 'B'
REFCOMP_PATH = '/Users/ryan/case'+CASE+'/case'+CASE+'_refcomp_struc.ent'
RUN_DIR = '/Users/ryan/case'+CASE+'/case'+CASE+'_'+RUN
MODEL_DIR = RUN_DIR + '/structures/it1/water'
ASSESSMENT_DIR = RUN_DIR + '/assessment'
L_RMSD_SCRIPT = ASSESSMENT_DIR + '/l-rmsd_script.txt'
I_RMSD_SCRIPT = ASSESSMENT_DIR + '/i-rmsd_script.txt'
NAMES_PATH = ASSESSMENT_DIR + '/names.txt'
L_RMSD_PATH = ASSESSMENT_DIR + '/l-rmsd.txt'
I_RMSD_PATH = ASSESSMENT_DIR + '/i-rmsd.txt'
FNAT_PATH = ASSESSMENT_DIR + '/fnat.txt'
CAPRI_PATH = ASSESSMENT_DIR + '/capri.txt'
ASSESSMENT_PATH = ASSESSMENT_DIR + '/case'+CASE+'_'+RUN+'_assessment.csv'

def calculate_rmsd():       #executes a bash file which runs profit to calculate the l-rmsd and i-rmsd of all models and writes those into two files
    with open(L_RMSD_PATH, 'w+') as l_rmsd, open(I_RMSD_PATH, 'w+') as i_rmsd, open(NAMES_PATH, 'w+') as names:
        for i in range(1,201):
            names.write('complex_'+str(i)+'w\n')
            mobile_path = MODEL_DIR + '/complex_' + str(i)+ 'w.pdb'
            output1 = open(ASSESSMENT_DIR+'/l-rmsd_complex_'+str(i)+'w.log', 'w+')
            subprocess.check_call(['bash', 'profit', '-f', L_RMSD_SCRIPT, REFCOMP_PATH, mobile_path], stdout=output1)
            output1.close()
            output1 = open(ASSESSMENT_DIR+'/l-rmsd_complex_'+str(i)+'w.log', 'r')
            rmsd = ''
            for line in output1:
                if 'RMS:' in line:
                    text, rmsd = line.split()
            l_rmsd.write(rmsd+'\n')
            output1.close()
            output2 = open(ASSESSMENT_DIR+'/i-rmsd_complex_'+str(i)+'w.log', 'w+')
            subprocess.check_call(['bash', 'profit', '-f', I_RMSD_SCRIPT, REFCOMP_PATH, mobile_path], stdout=output2)
            output2.close()
            output2 = open(ASSESSMENT_DIR+'/i-rmsd_complex_'+str(i)+'w.log', 'r')
            rmsd = ''
            for line in output2:
                if 'RMS:' in line:
                    text, rmsd = line.split()
            i_rmsd.write(rmsd+'\n')
            output2.close()

def capri_asses():      #assesses the quality of each model based on the CAPRI criteria, writes the quality into a new file, and makes a csv
    with open(L_RMSD_PATH, 'r') as l_rmsd_file, open(I_RMSD_PATH, 'r') as i_rmsd_file, \
         open(FNAT_PATH, 'r') as fnat_file, open(CAPRI_PATH, 'w+') as capri_file, \
         open(NAMES_PATH, 'r') as names_file, open(ASSESSMENT_PATH, 'wb+') as assess_file:
            for name, l_rmsd, i_rmsd, fnat in zip(names_file, l_rmsd_file, i_rmsd_file, fnat_file):
                l_rmsd = float(l_rmsd)
                i_rmsd = float(i_rmsd)
                fnat = float(fnat)
                if fnat >= 0.50 and (l_rmsd <= 1.0 or i_rmsd <= 1.0):
                    quality = 'high'
                elif fnat >= 0.30 and (l_rmsd <= 5.0 or i_rmsd <= 2.0):
                    quality = 'medium'
                elif fnat >= 0.10 and (l_rmsd <= 10.0 or i_rmsd <= 4.0):
                    quality = 'acceptable'
                else:
                    quality = 'incorrect'
                capri_file.write(quality + '\n')
                line = name.rstrip() + ', ' + str(l_rmsd) + ', ' + str(i_rmsd) + ', ' + str(fnat) + ', ' + quality + '\n'
                assess_file.write(line)


calculate_rmsd()
capri_asses()
