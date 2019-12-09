from pymol import cmd
from collections import defaultdict

CASE = ''
RUN = ''
REFCOMP_CHAIN1 = ''
REFCOMP_CHAIN2 = ''
EXCESSIVE_CHAINS = []
MAIN_DIR = '/Users/ryan/case' + CASE
REFCOMP_PATH = MAIN_DIR + '/case' + CASE + '_refcomp_struc.ent'
ACT_RES_PATH = MAIN_DIR + '/case' + CASE + '_active_residues.txt'
XL_PATH = MAIN_DIR + '/case' + CASE + '_restraints_DisVis.txt'
RUN_DIR = MAIN_DIR + '/case' + CASE + '_' + RUN
MODEL_DIR = RUN_DIR + '/structures/it1/water/'
CLUSTERED_RANKS = RUN_DIR + '/assessment/clustered_ranks.csv'


# in order of quality/rank!
MEDIUM = []
ACCEPTABLE = []
BEST_L_RMSD = []
BEST_I_RMSD = []



CLUSTERS = defaultdict(list)
with open(CLUSTERED_RANKS, 'r') as clustered_ranks:
	for line in clustered_ranks:
		model, cluster, rank = line.split(', ')
		rank = rank.strip()
		if rank.isdigit():
			if int(rank) < 5:
				groupname = 'cluster' + cluster
				CLUSTERS[groupname].append(model)

with open(ACT_RES_PATH, 'r') as act_res:
	act_res1 = act_res.readline()
	act_res1 = act_res1[:-2].replace(',', '+')
	act_res2 = act_res.readline()
	act_res2 = act_res2[:-2].replace(',', '+') 
with open(XL_PATH, 'r') as restraints:
	xls = []
	for line in restraints:
		columns = line.split()
		res1 = columns[1]
		res2 = columns[4]
		xls.append([res1,res2])



def load_model(model, name):
	cmd.load(MODEL_DIR+model+'.pdb', 'struc.'+name)
	cmd.color('cyan', 'chain A and struc.'+name)
	cmd.color('green', 'chain B and struc.'+name)
	cmd.select('act_res1', 'resid '+act_res1+' and chain A and struc.'+name)
	cmd.color('blue', 'act_res1')
	cmd.select('act_res2', 'resid '+act_res2+' and chain B and struc.'+name)
	cmd.color('yellow', 'act_res2')
	cmd.super('struc.'+name+' and chain B', 'refcomp and chain '+REFCOMP_CHAIN2)
	j = 0
	for xl in xls:
		j += 1
		cmd.distance('xl'+str(j)+'.'+name,\
					 'name CA and resi '+xl[0]+' and chain A and struc.'+name,\
					 'name CA and resi '+xl[1]+' and chain B and struc.'+name)
		cmd.color('yellow', 'xl'+str(j)+'.'+name)
	cmd.group(name, '*.'+name)

	
def group2(models, groupname):
	if len(models) > 0:
		i = 0
		selection = ''
		for model in models:
			i += 1
			name = str(i)+'.'+groupname
			load_model(model, name)
			selection += name+' '
		cmd.group(groupname, selection)



cmd.reinitialize()

cmd.load(REFCOMP_PATH, 'refcomp')
cmd.color('magenta', 'refcomp')
cmd.remove('(not polymer)')
for i in EXCESSIVE_CHAINS:
	cmd.remove('chain '+i+' and refcomp')

group2(MEDIUM, 'medium')
group2(ACCEPTABLE, 'acceptable')
group2(BEST_L_RMSD, 'best_l-rmsd')
group2(BEST_I_RMSD, 'best_i-rmsd')

for groupname in CLUSTERS:
	group2(CLUSTERS[groupname], groupname)		

cmd.show('cartoon')
cmd.center('vis')
cmd.set_view(\
    [0.528545737,    0.037218191,    0.848089755,\
     0.825324774,   -0.256363481,   -0.503107190,\
     0.198694482,    0.965864182,   -0.166216984,\
     0.000000000,    0.000000000, -246.176239014,\
    32.624721527,   63.801486969,   64.972671509,\
   194.087219238,  298.265258789,  -20.000000000] )


