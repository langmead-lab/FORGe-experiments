#!/bin/bash

export EXP_HOME=$1
export LD_LIBRARY_PATH=/home/langmead/.linuxbrew/lib:$LD_LIBRARY_PATH
export MASON=/scratch0/langmead-fs1/shared/mason/bin
export VIS_HOME=/scratch0/langmead-fs1/user/jacob/vis/src

# $EXP_HOME should contain the following files:
##   hs37d5.fa
##   ALL.chr19.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf
##   outgroup.txt

cd $EXP_HOME
export READLEN=100

for NAME in NA12878
do
    # Generate individual genomes
    mkdir -p indiv_genomes/$NAME
    #$VIS_HOME/update_genome.py --ref hs37d5.fa --vcf ALL.chr19.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf --chrom 19 --out-prefix indiv_genomes/$NAME/chr19 --name $NAME

    # Simulate reads
    cd indiv_genomes/$NAME
    $MASON/mason illumina -N 5000000 -n $READLEN -hn 1 -i -sq -o sim_hapA.fastq chr19_hapA.fa
    $MASON/mason illumina -N 5000000 -n $READLEN -hn 1 -i -sq -o sim_hapB.fastq chr19_hapB.fa

    cd $EXP_HOME
done
