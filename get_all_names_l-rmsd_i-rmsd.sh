#!/bin/bash

# makes three files with: all names, all l-rmsd, and all i-rmsd

for i in `seq 1 200`
do
	echo complex_${i}w >> /Users/ryan/Documents/case10_DisVis/results/all_names.txt
	profit -f l-rmsd.txt -h /Users/ryan/Documents/Data/case10_refcomp_struc.ent \
	/Users/ryan/Documents/case10_DisVis/structures/it1/water/complex_${i}w.pdb \
	| grep "RMS:" | cut -f5 -d' ' | tail -n1 >> \
	/Users/ryan/Documents/case10_DisVis/results/all_l-rmsd.txt
	profit -f i-rmsd.txt -h /Users/ryan/Documents/Data/case10_refcomp_struc.ent \
	/Users/ryan/Documents/case10_DisVis/structures/it1/water/complex_${i}w.pdb \
	| grep "RMS:" | cut -f5 -d' ' | tail -n1 >> \
	/Users/ryan/Documents/case10_DisVis/results/all_i-rmsd.txt
done

# paste -d, /Users/ryan/Documents/case10_DisVis/results/all_names.txt \
# /Users/ryan/Documents/case10_DisVis/results/all_l-rmsd.txt \
# /Users/ryan/Documents/case10_DisVis/results/all_i-rmsd.txt \
# /Users/ryan/Documents/case10_DisVis/results/all_fnat.txt \
# > /Users/ryan/Documents/case10_DisVis/results/all_results.txt
