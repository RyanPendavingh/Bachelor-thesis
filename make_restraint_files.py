#The format used by DisVis to represent the cross-links: each cross-link definition consists of eight fields
#   chainID of the 1st molecule
#   residue number
#   atom name
#   chainID of the 2nd molecule
#   residue number
#   atom name
#   lower distance limit
#   upper distance limit

#HADDOCK distance restraints are defined as:
#assi (segid <chain 1> and resid <residue number> and name <atom name>) \
# (segid <chain 2> and resid <residue number> and name <atom name>) \
# <distance>, <lower-bound correction>, <upper-bound correction>
#The lower limit for the distance is calculated as: distance minus lower-bound correction and
# the upper limit as: distance plus upper-bound correction

chain1 = 'A'
chain2 = 'A'
atom = 'CA'
min_distance = '0'
max_distance = '40'
segid1 = 'A'
segid2 = 'B'

with open('all_restraints.txt', 'r') as restraints:
    previous_case = ''
    for line in restraints:
        if line.startswith('#'):
            pass
        else:
            case, res_prot1, res_prot2, euclidean_dis, voidvol_dis = line.split(' ')
            with open('case'+case+'_restraints_DisVis.txt', 'a') as disvis:
                line_disvis = ' '.join([chain1, res_prot1, atom, chain2, res_prot2, atom, min_distance, max_distance]) + '\n'
                disvis.write(line_disvis)
            with open('case'+case+'_restraints_Haddock.tbl', 'a') as haddock:
                line_haddock = ' '.join(['assi (segid', segid1, 'and resid', res_prot1, 'and name', atom, ')', \
                                         '(segid', segid2, 'and resid', res_prot2, 'and name', atom, ')', \
                                        max_distance, max_distance, min_distance]) + '\n'
                haddock.write(line_haddock)