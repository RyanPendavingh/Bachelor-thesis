# doesn't work on this pc. same code does work on my own laptop.

#import matplotlib
#matplotlib.use('TkAgg')
from prody import *
from pylab import *
ion()

output = open('Documents/Data/case10_interface.txt','w')

refcomp = 'Documents/Data/case10_refcomp_struc.ent'
pdb = parsePDB(refcomp)
chainligand = 'B'
chainreceptor = 'A'

output.write(pdb.select('chain'+chainligand+'and calpha and (same residue as within 10 of chain'+chainreceptor).getResindices())
output.close()
