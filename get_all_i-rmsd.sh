#!/bin/bash

for i in `seq 1 200`
do
	profit -f i-rmsd.txt -h /Users/ryan/Documents/Data/case10_refcomp_struc.ent \
	/Users/ryan/Documents/case10_XL/structures/it1/water/complex_${i}w.pdb \
	| grep "RMS:" | cut -f5 -d' ' | tail -n1 >> \
	/Users/ryan/Documents/case10_XL/results/all_i-rmsd.txt
done