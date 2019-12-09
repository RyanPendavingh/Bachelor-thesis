# refine a loop
from modeller import *
from modeller.automodel import *
import sys

if len(sys.argv) != 9:
    print 'Usage: ' + sys.argv[0] + ' <initial model> <protein name> <first aa of loop1> <last aa of loop1> <first aa of loop2> <last aa of loop2> <start number> <end number>'

INI_MODEL_PATH = sys.argv[1]
PROT_NAME = sys.argv[2]
FIRST_AA_1 = sys.argv[3]
LAST_AA_1 = sys.argv[4]
FIRST_AA_2 = sys.argv[5]
LAST_AA_2 = sys.argv[6]
START = sys.argv[7]
END = sys.argv[8]

env = environ()
env.io.hetatm = True
class MyLoopmodel(loopmodel):
	def select_loop_atoms(self):
		return selection(self.residue_range(FIRST_AA_1+':A', LAST_AA_1+':A'), self.residue_range(FIRST_AA_2+':A',LAST_AA_2+':A'))

a = MyLoopmodel(env, inimodel=INI_MODEL_PATH,
                sequence=PROT_NAME,
                loop_assess_methods=(assess.DOPE, assess.normalized_dope, assess.GA341))

a.loop.starting_model = int(START)
a.loop.ending_model = int(END)
a.loop.md_level = refine.slow

a.make()