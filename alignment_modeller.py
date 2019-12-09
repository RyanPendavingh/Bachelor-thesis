from modeller import *
import sys
import os


if len(sys.argv) != 5:
    print 'Usage: ' + sys.argv[0] + ' <main directory>  <case number>  <protein number>  <refprot chain>'
try:
    os.path.exists(sys.argv[1])
    os.path.isdir(sys.argv[1])
except:
    print "Not a valid directory"


MAIN_DIR = sys.argv[1]   #C:/Users/Ryan/Documents/Bachelorscriptie2.0/data
CASE = sys.argv[2]
PROT = sys.argv[3]
REF_STRUC_CHAIN = sys.argv[4]
REFPROT_NAME = 'case' + CASE + '_refprot' + PROT
PROT_NAME = 'case' + CASE + '_prot' + PROT
PROT_FASTA_PATH = MAIN_DIR + '/' + PROT_NAME + '_seq.fasta'
PROT_PIR_PATH = MAIN_DIR + '/' + PROT_NAME + '_seq.pir'
REF_STRUC_PATH = MAIN_DIR + '/' + REFPROT_NAME + '_struc.ent'
ALI_PATH = MAIN_DIR + '/case' + CASE + '_ref-prot' + PROT + '_align.ali'
PAP_PATH = MAIN_DIR + '/case' + CASE + '_ref-prot' + PROT + '_align.pap'

def fasta_to_pir():
    with open(PROT_FASTA_PATH, 'r') as fasta:
        with open(PROT_PIR_PATH, 'w') as pir:
            for line in fasta:
                if line.startswith('>'):
                    text = '>P1;case' + CASE + '_prot' + PROT + '\nsequence:case' + CASE+ '_prot' + PROT + '::::::::\n'
                    pir.write(text)
                else:
                    pir.write(line)
            pir.write('*')


def align():
    env = environ()
    mdl = model(env, file=REF_STRUC_PATH, model_segment=('FIRST:'+REF_STRUC_CHAIN, 'LAST:'+REF_STRUC_CHAIN))
    aln = alignment(env)
    aln.append_model(mdl, align_codes=REFPROT_NAME)
    aln.append(file=PROT_PIR_PATH, align_codes=PROT_NAME)
    aln.align2d()
    aln.write(file=ALI_PATH, alignment_format='PIR')
    aln.write(file=PAP_PATH, alignment_format='PAP',
              alignment_features='INDICES HELIX BETA')

fasta_to_pir()
align()