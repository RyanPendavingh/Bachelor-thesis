#assessment part 2 (laptop, prody, windows)

from pylab import *
from prody import *
import subprocess
import sys
import os
import shutil

if len(sys.argv) != 6:
    print 'Usage: ' + sys.argv[0] + ' <case> <docking run> <refcomp chain 1> <refcomp chain 2> <shortest chain [1 or 2]>'
if sys.argv[5] != '1' and sys.argv[5] != '2':
    print 'Shortest chain must be either 1 or 2'


CASE = sys.argv[1]
RUN = sys.argv[2]
REFCOMP_CHAIN1 = sys.argv[3]
REFCOMP_CHAIN2 = sys.argv[4]
SHORT_CHAIN = sys.argv[5]
MODELS_CHAIN1 = 'A'
MODELS_CHAIN2 = 'B'
REFCOMP_PATH = 'C:\\Users\\Ryan\\Documents\\Bachelorscriptie2.0\\case'+CASE+'\\case'+CASE+'_refcomp_struc.ent'
RUN_DIR= 'C:\\Users\\Ryan\\Documents\\Bachelorscriptie2.0\\case'+CASE+'\\case'+CASE+'_'+RUN
MODEL_DIR = RUN_DIR + '\\structures\\it1\\water'
ASSESSMENT_DIR = RUN_DIR + '\\assessment'
ALIGNMENT1_PATH = ASSESSMENT_DIR + '\\alignment1.txt'
ALIGNMENT2_PATH = ASSESSMENT_DIR + '\\alignment2.txt'
L_RMSD_SCRIPT = ASSESSMENT_DIR + '\\l-rmsd_script.txt'
I_RMSD_SCRIPT = ASSESSMENT_DIR + '\\i-rmsd_script.txt'
FNAT_PATH = ASSESSMENT_DIR + '\\fnat.txt'
INT_REFCOMP_10_PATH = ASSESSMENT_DIR + '\\interface_refcomp_10A.txt'
INT_REFCOMP_IRMSD_10_PATH = ASSESSMENT_DIR + '\\interface_refcomp_irmsd_10A.txt'
INT_HYPOTHETICAL_10_PATH = ASSESSMENT_DIR + '\\interface_hypothetical_10A.txt'
INT_REFCOMP_5_PATH = ASSESSMENT_DIR + '\\interface_refcomp_5A.txt'
INT_REFCOMP_IRMSD_5_PATH = ASSESSMENT_DIR + '\\interface_refcomp_irmsd_5A.txt'
INT_HYPOTHETICAL_5_PATH = ASSESSMENT_DIR + '\\interface_hypothetical_5A.txt'


def interface_res_10A(pdb_path, chain1, chain2):        #gives a list of the sequential residue numbers that are within 10A of the other chain
    pdb = parsePDB(pdb_path)
    interface1 = pdb.select('chain ' + chain1 + ' and calpha and (same residue as within 10 of chain ' + chain2 + ')').getResindices()
    interface2 = pdb.select('chain ' + chain2 + ' and calpha and (same residue as within 10 of chain ' + chain1 + ')').getResindices()
    interface_list = interface1.tolist() + interface2.tolist()
    return interface_list

def interface_res_5A(pdb_path, chain1, chain2):        #gives a list of the sequential residue numbers that are within 5A of the other chain
    pdb = parsePDB(pdb_path)
    interface1 = pdb.select('chain ' + chain1 + ' and calpha and (same residue as within 5 of chain ' + chain2 + ')').getResindices()
    interface2 = pdb.select('chain ' + chain2 + ' and calpha and (same residue as within 5 of chain ' + chain1 + ')').getResindices()
    interface_list = interface1.tolist() + interface2.tolist()
    return interface_list

def convert_numbering(interface_refcomp):       #converts the numbering of the interface residues of the refcomp into the numbering of the model
    interface_converted = []
    interface_refcomp_irmsd = []
    with open(ALIGNMENT1_PATH, 'r') as alignment1:
        for line in alignment1:
            ref, model = line.split(':')
            start_ref, end_ref = ref.split('-')
            start_model, end_model = model.split('-')
            for i in interface_refcomp:
                if int(end_ref)>=int(i)>=int(start_ref):    #if residue in the interface of refcomp is in an aligned zone (and thus has an equivilant residue in the model)
                    new = int(i)-int(start_ref)+int(start_model)  #convert numbering to that of the corresponding residue in the model
                    interface_converted.append(new)
                    interface_refcomp_irmsd.append(i)       #list of all interface residues of refcomp that have an equivilant residue in the model which is needed for calculating the irmsd
    with open(ALIGNMENT2_PATH, 'r') as alignment2:
        for line in alignment2:
            ref, model = line.split(':')
            start_ref, end_ref = ref.split('-')
            start_model, end_model = model.split('-')
            for i in interface_refcomp:
                if int(end_ref)>=int(i)>=int(start_ref):    
                    new = int(i)-int(start_ref)+int(start_model)  
                    interface_converted.append(new)
                    interface_refcomp_irmsd.append(i)
	return interface_converted, interface_refcomp_irmsd


def write_rmsd_scripts(interface_refcomp_irmsd, interface_hypothetical):        #writes l-rmsd script and i-rmsd script for profit based on the alignment and hypothetical interface, smallest protein is the ligand
    if SHORT_CHAIN =='1':
        refcomp_receptor = REFCOMP_CHAIN2
        models_receptor = MODELS_CHAIN2
        alignment_ligand = ALIGNMENT1_PATH
    else:
        refcomp_receptor = REFCOMP_CHAIN1
        models_receptor = MODELS_CHAIN1
        alignment_ligand = ALIGNMENT2_PATH
    with open(L_RMSD_SCRIPT, 'wb+') as lrmsd, open(alignment_ligand, 'r') as alignment_ligand:
        text1 = 'atoms CA\n' \
            'align ' + refcomp_receptor + '*:' + models_receptor + '*\n' \
            'fit\nratoms CA\nnumber sequential\n'
        lrmsd.write(text1)
        for line in alignment_ligand:
            text2 = 'rzone ' + line
            lrmsd.write(text2)
        lrmsd.write('quit')
    with open(I_RMSD_SCRIPT, 'wb+') as irmsd:          
        irmsd.write('atoms CA\nnumber sequential\n')
        for index in range(len(interface_refcomp_irmsd)):
            text4 = 'zone ' + str(interface_refcomp_irmsd[index]) + '-' + str(interface_refcomp_irmsd[index]) + ':' + str(interface_hypothetical[index]) + '-' + str(interface_hypothetical[index]) + '\n'
            irmsd.write(text4)
        irmsd.write('fit\nquit')

def calculate_fnat(interface_hypothetical):     #determines interface of each model and calculates the fnat, and writes those into seperate files
    with open(FNAT_PATH, 'wb+') as fnat_file:
        for i in range(1, 201):
            pdb_path = MODEL_DIR + '\\complex_' + str(i) + 'w.pdb'
            interface_model = interface_res_5A(pdb_path, MODELS_CHAIN1, MODELS_CHAIN2)
            amount = 0
            for res in interface_hypothetical:
                if res in interface_model:
                    amount += 1
            fnat = float(amount) / float(len(interface_hypothetical))
            fnat_file.write(str(fnat))
            fnat_file.write('\n')
            with open(ASSESSMENT_DIR + '\\interface_complex_' + str(i) + 'w.txt', 'w+') as interface_file:
                for residue in interface_model:
                    interface_file.write(str(residue))
                    interface_file.write(', ')

def write_files():      #writes the interfaces (refcomp, refcomp_irmsd and hypothetical) to files
    with open(INT_REFCOMP_10_PATH, 'wb+') as int_refcomp:
        for residue in INTERFACE_REFCOMP_10:
            int_refcomp.write(str(residue))
            int_refcomp.write(', ')
    with open(INT_REFCOMP_IRMSD_10_PATH, 'wb+') as int_refcomp_irmsd:
        for residue in INTERFACE_REFCOMP_IRMSD_10:
            int_refcomp_irmsd.write(str(residue))
            int_refcomp_irmsd.write(', ')
    with open(INT_HYPOTHETICAL_10_PATH, 'wb+') as int_hypo:
        for residue in INTERFACE_HYPOTHETICAL_10:
            int_hypo.write(str(residue))
            int_hypo.write(', ')
    with open(INT_REFCOMP_5_PATH, 'wb+') as int_refcomp:
        for residue in INTERFACE_REFCOMP_5:
            int_refcomp.write(str(residue))
            int_refcomp.write(', ')
    with open(INT_REFCOMP_IRMSD_5_PATH, 'wb+') as int_refcomp_irmsd:
        for residue in INTERFACE_REFCOMP_IRMSD_5:
            int_refcomp_irmsd.write(str(residue))
            int_refcomp_irmsd.write(', ')
    with open(INT_HYPOTHETICAL_5_PATH, 'wb+') as int_hypo:
        for residue in INTERFACE_HYPOTHETICAL_5:
            int_hypo.write(str(residue))
            int_hypo.write(', ')

INTERFACE_REFCOMP_10 = interface_res_10A(REFCOMP_PATH, REFCOMP_CHAIN1, REFCOMP_CHAIN2)
INTERFACE_HYPOTHETICAL_10, INTERFACE_REFCOMP_IRMSD_10 = convert_numbering(INTERFACE_REFCOMP_10)   #hypothetical interface= predicted interface of model based on the interface of the refcomp
INTERFACE_REFCOMP_5 = interface_res_5A(REFCOMP_PATH, REFCOMP_CHAIN1, REFCOMP_CHAIN2)
INTERFACE_HYPOTHETICAL_5, INTERFACE_REFCOMP_IRMSD_5 = convert_numbering(INTERFACE_REFCOMP_5)
write_rmsd_scripts(INTERFACE_REFCOMP_IRMSD_10, INTERFACE_HYPOTHETICAL_10)
calculate_fnat(INTERFACE_HYPOTHETICAL_5)
write_files()

