#assessment part 1 (pc, profit, Mac)

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
ALIGN_SCRIPT1_PATH = ASSESSMENT_DIR + '/align_script1.txt'
ALIGN_SCRIPT2_PATH = ASSESSMENT_DIR + '/align_script2.txt'
ALIGNMENT1_PATH = ASSESSMENT_DIR + '/alignment1.txt'
ALIGNMENT2_PATH = ASSESSMENT_DIR + '/alignment2.txt'
PROFIT_OUTPUT1_PATH = ASSESSMENT_DIR + '/alignment1.log'
PROFIT_OUTPUT2_PATH = ASSESSMENT_DIR + '/alignment2.log'

os.mkdir(ASSESSMENT_DIR)


def write_profit_align_script():        # writes an alignment script for profit based on the chain names of the reference complex and the models
    with open(ALIGN_SCRIPT1_PATH, 'wb+') as align_script1:
        text =  'atoms CA\n'\
                'align ' + REFCOMP_CHAIN1 + '*:' + MODELS_CHAIN1 + '*\n'\
                'status\nquit'
        align_script1.write(text)
    with open(ALIGN_SCRIPT2_PATH, 'wb+') as align_script2:
        text =  'atoms CA\n'\
                'align ' + REFCOMP_CHAIN2 + '*:' + MODELS_CHAIN2 + '*\n'\
                'status\nquit'
        align_script2.write(text)

def align_profit():     #makes an alignment using profit and gives a list of this alignment (format: sequential numbering, aligned zones, [start zone refcomp, end zone refcomp, start zone model, end zone model])
    mobile_path= MODEL_DIR + '/complex_1w.pdb'
    f= open(PROFIT_OUTPUT1_PATH, 'wb+')
    subprocess.check_call(['bash', 'profit', '-f', ALIGN_SCRIPT1_PATH, REFCOMP_PATH, mobile_path], stdout=f)
    f.close()
    align_list1 = []
    with open(PROFIT_OUTPUT1_PATH, 'r') as profit_output1:
        for line in profit_output1:
            if 'with' in line:
                columns = line.split()
                zone = [ columns[0], columns[2], columns[4], columns[6] ]
                align_list1.append(zone)
    f= open(PROFIT_OUTPUT2_PATH, 'wb+')
    subprocess.check_call(['bash', 'profit', '-f', ALIGN_SCRIPT2_PATH, REFCOMP_PATH, mobile_path], stdout=f)
    f.close()
    align_list2 = []
    with open(PROFIT_OUTPUT2_PATH, 'r') as profit_output2:
        for line in profit_output2:
            if 'with' in line:
                columns = line.split()
                zone = [ columns[0], columns[2], columns[4], columns[6] ]
                align_list2.append(zone)
    return align_list1, align_list2

def write_alignment_file():      #writes the alignment to a file
    with open(ALIGNMENT1_PATH, 'wb+') as align_file1:
        for zone in ALIGNMENT_LIST1:
            line = zone[0] + '-' + zone[1] + ':' + zone[2] + '-' + zone[3] + '\n'
            align_file1.write(line)
    with open(ALIGNMENT2_PATH, 'wb+') as align_file2:
        for zone in ALIGNMENT_LIST2:
            line = zone[0] + '-' + zone[1] + ':' + zone[2] + '-' + zone[3] + '\n'
            align_file2.write(line)


    
write_profit_align_script()
ALIGNMENT_LIST1, ALIGNMENT_LIST2 = align_profit()
write_alignment_file()


