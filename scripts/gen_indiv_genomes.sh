#!/bin/bash

export EXP_HOME=$1
export VIS_HOME=/scratch0/langmead-fs1/user/jacob/vis/src

cd $EXP_HOME
for NAME in NA12878
do
    mkdir -p $NAME
    $VIS_HOME/update_genome.py --ref hs37d5.fa --vcf ALL.chr19.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf --chrom 19 --out-prefix $NAME/chr19 --name $NAME
done
