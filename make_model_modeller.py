from modeller import *
from modeller.automodel import *
import sys
import os

if len(sys.argv) != 4:
    print 'Usage: ' + sys.argv[0] + ' <main directory>  <case number>  <protein number>'
try:
    os.path.exists(sys.argv[1])
    os.path.isdir(sys.argv[1])
except:
    print "Not a valid directory"


MAIN_DIR = sys.argv[1]   #C:/Users/Ryan/Documents/Bachelorscriptie2.0/data
CASE = sys.argv[2]
PROT = sys.argv[3]
REF_PROT_NAME = 'case' + CASE + '_refprot' + PROT
PROT_NAME = 'case' + CASE + '_prot' + PROT
ALI_PATH = MAIN_DIR + '/homology_models/case' + CASE + '_ref-prot' + PROT + '_align_edited.ali'
START = 11
END = 20

def make_automodel():
    env = environ()
    env.io.hetatm = True
    a = automodel(env,
        alnfile = ALI_PATH,     # PIR format alignment
        knowns = REF_PROT_NAME,
        sequence = PROT_NAME,
        assess_methods = (assess.DOPE, assess.GA341))
    a.starting_model = START
    a.ending_model = END
    a.make()

make_automodel()
#os.rename('Users/ryan/make_model_modeller(new).log', 'Users/ryan/case2A/homology_models/case2A_prot2_make_model.log')
