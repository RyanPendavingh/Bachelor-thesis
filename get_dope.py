from modeller import *
from modeller.scripts import *
import sys

if len(sys.argv) != 3:
    print 'Usage: ' + sys.argv[0] + ' <pdf file> <result file 1>'

MODEL_PATH = sys.argv[1]
RESULT_PATH1 = sys.argv[2]
#RESULT_PATH2 = sys.argv[3]


# writes the per residue DOPE score into a file
def DOPE_score():
    env = environ()
    env.libs.topology.read(file='$(LIB)/top_heav.lib')
    env.libs.parameters.read(file='$(LIB)/par.lib')
    m = complete_pdb(env, MODEL_PATH)
    s = selection(m)
    s.get_dope_profile().write_to_file(RESULT_PATH1)
    with open(RESULT_PATH1, 'a') as results:
    	results.write(str(s.assess_dope()))

def trim_file():
	list = []
	with open(RESULT_PATH1, 'r') as dope:
		for line in dope:
			columns = line.split()
			list.append(columns[-1])
	with open(RESULT_PATH1, 'w') as new:
		for item in list:
			new.write(item+'\n')


DOPE_score()
trim_file()