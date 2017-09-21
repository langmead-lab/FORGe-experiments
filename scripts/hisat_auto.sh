#!/bin/bash

export EXP_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis_exp_chr9
export SCRIPT_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis-experiments/scripts
export HISAT_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis/software/hisat2
export VIS_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis

cd $EXP_HOME

#$HISAT_HOME/hisat2_extract_snps_haplotypes_VCF.py hs37d5.fa filtered_ALL.chr9.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf hisat_auto

#$SCRIPT_HOME/testMem.py $HISAT_HOME/hisat2-build --snp hisat_auto.snp --haplotype hisat_auto.haplotype chr9.fa hisat_indexes/hisat_auto

export LEN=100
export NAME=NA12878

for HAP in A B
do
    $SCRIPT_HOME/testMem.py $HISAT_HOME/hisat2 --sam-no-qname-trunc --score-min C,-50 -x hisat_indexes/hisat_auto -U indiv_genomes/$NAME/sim_l${LEN}_hap${HAP}.tagged.fastq -S aligned/$NAME/hisat_auto_hap${HAP}_l${LEN}.sam
    cat aligned/$NAME/hisat_auto_hap${HAP}_l${LEN}.sam | python2.7 $VIS_HOME/src/correctness/correctness.py auto_out Auto $HAP
done
