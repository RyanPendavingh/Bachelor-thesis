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
RSA_PATH_1 = MAIN_DIR + '/case' + CASE + '_prot1_struc.rsa'
RSA_PATH_2 = MAIN_DIR + '/case' + CASE + '_prot2_struc.rsa'
ACCESSIBLE_PATH = MAIN_DIR + '/case' + CASE + '_accessible.txt'
THRESHOLD = 40.0


# writes all residues numbers with an all-atom accessibility of >= the threshold in a new file
def accessible_res():
	with open(RSA_PATH_1,'r') as rsa1, open(RSA_PATH_2,'r') as rsa2, open(ACCESSIBLE_PATH,'w') as output:
		for line in rsa1:
			columns= line.split()		# 3 = residue number, 5 = all-atom relative accessibility
			if columns[0]=='RES' and float(columns[5])>=THRESHOLD:
				output.write(columns[3]+' ')
		output.write('\n')
		for line in rsa2:
			columns= line.split()		# 3 = residue number, 5 = all-atom relative accessibility
			if columns[0]=='RES' and float(columns[5])>=THRESHOLD:
				output.write(columns[3]+' ')
			
accessible_res()