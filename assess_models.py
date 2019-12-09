from pylab import *
from prody import *
import subprocess
import sys
import os
import shutil

#if len(sys.argv()) != 4:
    #print 'Usage: ' + sys.argv[0] + ' <main directory>  <refcomp chain 1>  <refcomp chain 2>'
try:
    os.path.exists(sys.argv[1])
    os.path.isdir(sys.argv[1])
except:
    print "Not a valid directory"

MAIN_DIR= sys.argv[1]   #directory of docking run
REFCOMP_CHAIN1= sys.argv[2]
REFCOMP_CHAIN2= sys.argv[3]
MODELS_CHAIN1= 'A'
MODELS_CHAIN2= 'B'
REFCOMP_PATH = MAIN_DIR + '/refcomp_struc.ent'
MODEL_DIR = MAIN_DIR + '/structures/it1/water'
ALIGN_SCRIPT_PATH = MAIN_DIR + '/profit_align_script.txt'
PROFIT_OUTPUT_PATH = MAIN_DIR + '/profit_output.txt'
L_RMSD_SCRIPT = MAIN_DIR + '/l-rmsd_script.txt'
I_RMSD_SCRIPT = MAIN_DIR + '/i-rmsd_script.txt'
ASSESSMENT_DIR = MAIN_DIR + '/assessment'
ALIGNMENT_PATH = ASSESSMENT_DIR + '/alignment.txt'
NAMES_PATH = ASSESSMENT_DIR + '/names.txt'
L_RMSD_PATH = ASSESSMENT_DIR + '/l-rmsd.txt'
I_RMSD_PATH = ASSESSMENT_DIR + '/i-rmsd.txt'
FNAT_PATH = ASSESSMENT_DIR + '/fnat.txt'
CAPRI_PATH = ASSESSMENT_DIR + '/capri.txt'
ASSESSMENT_PATH = ASSESSMENT_DIR + '/assessment.csv'
INT_REFCOMP_PATH = ASSESSMENT_DIR + '/interface_refcomp.txt'
INT_REFCOMP_IRMSD_PATH = ASSESSMENT_DIR + '/interface_refcomp_irmsd.txt'
INT_HYPOTHETICAL_PATH = ASSESSMENT_DIR + '/hypothetical_interface.txt'

files = [ALIGN_SCRIPT_PATH, PROFIT_OUTPUT_PATH, L_RMSD_SCRIPT, I_RMSD_SCRIPT]
for file in files:                      #remove output files if they already exist
    if os.path.exists(file):
        os.remove(file)
if os.path.exists(ASSESSMENT_DIR):      #including the assessment and profit output files
    shutil.rmtree(ASSESSMENT_DIR)


def interface_res(pdb_path, chain1, chain2):        #gives a list of the sequential residue numbers that are within 10A of the other chain
    pdb = parsePDB(pdb_path)
    interface1 = pdb.select('chain ' + chain1 + ' and calpha and (same residue as within 10 of chain ' + chain2 + ')').getResindices()
    interface2 = pdb.select('chain ' + chain2 + ' and calpha and (same residue as within 10 of chain ' + chain1 + ')').getResindices()
    interface_list = interface1.tolist() + interface2.tolist()
    return interface_list

def write_profit_align_script():        # writes an alignment script for profit based on the chain names of the reference complex and the models
    with open(ALIGN_SCRIPT_PATH, 'w') as align_script:
        text =  'atoms CA\n'\
                'align ' + REFCOMP_CHAIN1 + '*:' + MODELS_CHAIN1 + '*\n'\
                'align ' + REFCOMP_CHAIN2 + '*:' + MODELS_CHAIN2+ '*\n'\
                'status\nquit'
        align_script.write(text)

def align_profit():     #makes an alignment using profit and gives a list of this alignment (format: sequential numbering, aligned zones, [start zone refcomp, end zone refcomp, start zone model, end zone model])
    mobile_path= MODEL_DIR + '/complex1w.pdb'
    subprocess.check_call(['bash', 'profit', '-f', ALIGN_SCRIPT_PATH, '-h', REFCOMP_PATH, mobile_path])
    renamed_profit_output = ASSESSMENT_DIR + '/profit_output/alignment.txt'
    os.renames(PROFIT_OUTPUT_PATH, renamed_profit_output)
    align_list = []
    with open(renamed_profit_output, 'r') as profit_output:
            for line in profit_output:
                if 'with' in line:
                    columns = line.split()
                    zone = [ columns[0], columns[2], columns[4],columns[6] ]
                    align_list.append(zone)
    return align_list

def convert_numbering(align_list, interface_refcomp):       #finds the residues in the interface of the reference complex that have a homolog in the model structure. writes those residue numbers to a new list, converts those numbers to the residue numbers found in the model and writes those to a new list
    interface_converted = []
    interface_refcomp_irmsd = []
    for zone in align_list:
        for i in interface_refcomp:
                    if int(zone[2])>=int(i)>=int(zone[1]):
                        new = int(i)+int(zone[3])-int(zone[4])
                        interface_converted.append(new)
                        interface_refcomp_irmsd.append(i)
    return interface_converted, interface_refcomp_irmsd

def write_rmsd_scripts(interface_refcomp_irmsd, interface_hypothetical):        #writes l-rmsd script and i-rmsd script for profit based on the alignment and hypothetical interface
    text1=  'atoms CA\n'\
            'align ' + REFCOMP_CHAIN1 + '*:' + MODELS_CHAIN1 + '*\n'\
            'fit\nratoms CA\nnumber sequential'
    with open(L_RMSD_SCRIPT, 'w') as lrmsd:
        lrmsd.write(text1)
        for zone in ALIGNMENT_LIST:
            text2 = 'rzone ' + zone[0] + '-' + zone[1] + ':' + zone[2] + '-' + zone[3] + '\n'
            lrmsd.write(text2)
        lrmsd.write('quit')
    with open(I_RMSD_SCRIPT, 'w') as irmsd:
        text3 = 'atoms CA\n' \
                'align ' + REFCOMP_CHAIN1 + '*:' + MODELS_CHAIN1 + '*\n' \
                'align ' + REFCOMP_CHAIN2 + '*:' + MODELS_CHAIN2 + '* append\n' \
                'fit\nratoms CA\nnumber sequential'
        irmsd.write(text3)
        for index in range(len(interface_refcomp_irmsd)):
            text4 = 'rzone ' + interface_refcomp_irmsd[index] + ':' + interface_hypothetical[index] + '\n'
            irmsd.write(text4)
        irmsd.write('quit')

def calculate_rmsd():       #executes a bash file which runs profit to calculate the l-rmsd and i-rmsd of all models and writes those into two files
    subprocess.check_call(['bash', 'rmsd.sh', REFCOMP_PATH, MODEL_DIR, ASSESSMENT_DIR])

def calculate_fnat(interface_hypothetical):     #calculates the fnat (= percentage of residues in the hypothetical interface that are in the interface of the model) of each model and writes those into a file
    with open(FNAT_PATH, 'w') as fnat_file:
        for i in range(1, 201):
            pdb_path = MODEL_DIR + '/complex_' + str(i) + 'w.pdb'
            interface_model = interface_res(pdb_path, MODELS_CHAIN1,MODELS_CHAIN1)
            amount = 0
            for res in interface_hypothetical:
                if res in interface_model:
                    amount += 1
            fnat = float(amount) / float(len(interface_hypothetical))
            fnat_file.write(str(fnat))
            fnat_file.write('\n')
            with open(ASSESSMENT_DIR + '/interface_complex_' + str(i) + 'w.pdb', 'w') as interface_file:
                for residue in interface_model:
                    interface_file.write(residue)
                    interface_file.write(', ')

def capri_asses():      #assesses the quality of each model based on the CAPRI criteria and writes the quality into a new file
    with open(L_RMSD_PATH, 'r') as l_rmsd_file, open(I_RMSD_PATH, 'r') as i_rmsd_file, \
         open(FNAT_PATH, 'r') as fnat_file, open(CAPRI_PATH, 'w') as capri_file:
                for l_rmsd, i_rmsd, fnat in zip(l_rmsd_file, i_rmsd_file, fnat_file):
                    if fnat >= 0.50 and (l_rmsd <= 1.0 or i_rmsd <= 1.0):
                        quality = 'high'
                    elif fnat >= 0.30 and (l_rmsd <= 5.0 or i_rmsd <= 2.0):
                        quality = 'medium'
                    elif fnat >= 0.10 and (l_rmsd <= 10.0 or i_rmsd <= 4.0):
                        quality = 'acceptable'
                    else:
                        quality = 'incorrect'
                    capri_file.write(quality + '\n')

def merge_results():        #writes all the different values into a csv file
    with open(L_RMSD_PATH, 'r') as l_rmsd_file, open(I_RMSD_PATH, 'r') as i_rmsd_file,\
         open(FNAT_PATH, 'r') as fnat_file, open(CAPRI_PATH, 'w') as capri_file, \
         open(NAMES_PATH, 'r') as names_file, open(ASSESSMENT_PATH, 'r') as asses_file:
            for tuple in zip(name_file, l_rmsd_file, i_rmsd_file, fnat_file, capri_file):
                for l_rmsd, i_rmsd, fnat, capri in tuple:
                    line = str(name) + ' , ' + str(l_rmsd) + ' , ' + str(i_rmsd) + ' , ' + str(fnat) + ' , ' + capri
                    asses_file.write(line)

def write_files():      #writes the alignment and the interfaces (refcomp, refcomp_irmsd and hypothetical) to files
    with open(ALIGNMENT_PATH, 'w') as align_file:
        for zone in ALIGNMENT_LIST:
            line = zone[0] + '-' + zone[1] + ':' + zone[3] + '-' + zone[4] + '\n'
            align_file.write(line)
    with open(INT_REFCOMP_PATH, 'w') as int_refcomp:
        for residue in int_refcomp:
            int_refcomp.write(residue)
            int_refcomp.write(', ')
    with open(INT_REFCOMP_IRMSD_PATH, 'w') as int_refcomp_irmsd:
        for residue in int_refcomp_irmsd:
            int_refcomp_irmsd.write(residue)
            int_refcomp_irmsd.write(', ')
    with open(INT_HYPOTHETICAL_PATH, 'w') as int_hypo:
        for residue in int_hypo:
            int_hypo.write(residue)
            int_hypo.write(', ')

write_profit_align_script()
INTERFACE_REFCOMP = interface_res(REFCOMP_PATH, REFCOMP_CHAIN1, REFCOMP_CHAIN2)
ALIGNMENT_LIST = align_profit()
INTERFACE_HYPOTHETICAL, INTERFACE_REFCOMP_IRMSD = convert_numbering(ALIGNMENT_LIST, INTERFACE_REFCOMP)
write_rmsd_scripts(INTERFACE_REFCOMP_IRMSD, INTERFACE_HYPOTHETICAL)
calculate_rmsd()
calculate_fnat(INTERFACE_HYPOTHETICAL)
capri_asses()
merge_results()
write_files()