import sys
import os

if len(sys.argv) != 3:
	print 'Usage: ' + sys.argv[0] + ' <main directory>  <case number>'
try:
    os.path.exists(sys.argv[1])
    os.path.isdir(sys.argv[1])
except:
    print "Not a valid directory"


MAIN_DIR = sys.argv[1]
CASE = sys.argv[2]
PROT1_PATH = MAIN_DIR + '/receptor_interactions.txt'
PROT2_PATH = MAIN_DIR + '/ligand_interactions.txt'
OUTPUT_PATH = MAIN_DIR + '/case' + CASE + '_active_residues_correct.txt'
THRESHOLD = 0.5


# writes all residues with an interaction fraction of >=threshold (=active residues) in a new file
def active_res():
	with open(PROT1_PATH, 'r') as prot1:
		with open(PROT2_PATH, 'r') as prot2:
			with open(OUTPUT_PATH, 'w') as output:
				for line in prot1:
					columns= line.split()
					if float(columns[-1])>=0.5 and columns[0]!='#resi':
						output.write(columns[0]+',')
				output.write('\n')
				for line in prot2:
					columns= line.split()
					if float(columns[-1])>=0.5 and columns[0]!='#resi':
						output.write(columns[0]+',')

active_res()
