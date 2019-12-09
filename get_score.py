import sys

if len(sys.argv) != 3:
    print 'Usage: ' + sys.argv[0] + ' <case> <docking run>'

CASE = sys.argv[1]
RUN = sys.argv[2]
RUN_DIR = '/Users/ryan/case'+CASE+'/case'+CASE+'_'+RUN
FILE_LIST = RUN_DIR + '/structures/it1/water/file.list'
SCORE_PATH = RUN_DIR + '/assessment/case'+CASE+'_'+RUN+'_haddock_scores.csv'

with open(FILE_LIST, 'r') as file_list, open(SCORE_PATH, 'w+') as score_file:
	rank = 1
	for line in file_list:
		columns = line.split()
		haddock_score = columns[2]
		name = columns[0][8:-5]
		score_file.write(name+', '+haddock_score+', '+str(rank)+'\n')
		rank += 1
