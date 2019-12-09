import sys

if len(sys.argv) != 3:
    print 'Usage: ' + sys.argv[0] + ' <case> <docking run>'


CASE = sys.argv[1]
RUN = sys.argv[2]
RUN_DIR = '/Users/ryan/case'+CASE+'/case'+CASE+'_'+RUN
CLUSTERS_PATH = RUN_DIR + '/structures/it1/water/clusters_haddock-sorted.stat'
RANK_PATH = RUN_DIR + '/assessment/clustered_ranks.csv'

cluster = 0
complexes = set()
with open(CLUSTERS_PATH, 'r') as clusters, open(RANK_PATH, 'wb+') as rank:
	for line in clusters:
		columns = line.split()
		if 'file' in columns[0]:
			names_path = RUN_DIR + '/structures/it1/water/' + columns[0]
			cluster += 1
			with open(names_path, 'r') as names:
				complex = 0
				for line in names:
					name = line[0:-5]
					complexes.add(name)
					complex +=1
					rank.write(name+', '+str(cluster)+', '+str(complex)+'\n')
	for i in range(1,201):
		name = 'complex_' + str(i) + 'w'
		if name not in complexes:
			rank.write(name+', -, -\n')



