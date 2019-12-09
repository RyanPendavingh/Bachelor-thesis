#!/bin/bash

# makes three files with: all names, all l-rmsd, and all i-rmsd

#if ! [[ $# -eq 4 ]]
#then
    #echo "usage: $0 <reference file> <model directory> <results directory>"
    #exit 1
#fi

# input
REFERENCE_FILE=$1
MODEL_DIR=$2
ASSESSMENT_DIR=$3

# output
NAMES_FILE=${ASSESSMENT_DIR}/names.txt
L_RMSD_FILE=${ASSESSMENT_DIR}/l-rmsd.txt
I_RMSD_FILE=${ASSESSMENT_DIR}/i-rmsd.txt
PROFIT_OUTPUT_FILE=profit_output.txt

# delete output files if they already exist
rm -f "${NAMES_FILE}" "${L_RMSD_FILE}" "${I_RMSD_FILE}"


for i in `seq 1 200`
do
	echo complex_${i}w >> "${NAMES_FILE}"

	profit -f l-rmsd.txt -h "${REFERENCE_FILE}"	"${MODEL_DIR}/complex_${i}w.pdb"
	>> "${ASSESSMENT_DIR}/l-rmsd_complex_${i}w.log"
	grep "RMS:" "${ASSESSMENT_DIR}/l-rmsd_complex_${i}w.log" \
	| cut -f5 -d' ' | tail -n1 >> "${L_RMSD_FILE}"
	

	profit -f i-rmsd.txt -h "${REFERENCE_FILE}" "${MODEL_DIR}/complex_${i}w.pdb"
	>> "${ASSESSMENT_DIR}/i-rmsd_complex_${i}w.log"
	grep "RMS:" "${ASSESSMENT_DIR}/i-rmsd_complex_${i}w.log" \
	| cut -f5 -d' ' | tail -n1 >> "${I_RMSD_FILE}"
	

done

