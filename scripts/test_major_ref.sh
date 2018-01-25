#!/bin/bash

export EXP_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis_exp_chr9
export SCRIPT_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis-experiments/scripts
export VIS_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis

cd $EXP_HOME
#$SCRIPT_HOME/gen_major_allele_ref.py hs37d5.fa snps.1ksnp chr9_major.fa

export PCT=0
export LEN=100
export NAME=NA12878
export PREFIX=chr9_major
export INDEX=hisat_indexes/major

$SCRIPT_HOME/testMem.py $VIS_HOME/software/hisat2/hisat2-build chr9_major.fa $INDEX
for HAP in A B
do
    export FASTQ=indiv_genomes/$NAME/sim_l${LEN}_hap${HAP}.tagged.fastq
    export SAM=aligned/$NAME/major_hap${HAP}_l${LEN}.sam
    export DESC=$HAP
    $SCRIPT_HOME/align.sh
done

