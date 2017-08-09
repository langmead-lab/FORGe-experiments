#!/bin/bash

export ERG_HOME=/scratch0/langmead-fs1/user/jacob/enhanced_reference_genome/src
export DIR=/scratch0/langmead-fs1/user/jacob/1000genomes/chr19

#export MODE=fnr
#export PCT=10
#/scratch0/langmead-fs1/shared/pypy3-2.4-linux_x86_64-portable/bin/pypy $ERG_HOME/gen_hisat_snps.py --snps ingroup_snps.1ksnp --out $DATA/experiments/01_sim_yoruban_chr1/hisat_snps/${MODE}${PCT}.txt --sorted-snps snps_sorted_by_${MODE}_added.tsv --pct $PCT

#for MODE in fnr fpr blowup
export THR=0.5
for MODE in pop_cov
do
    echo $MODE
    for PCT in 10 20 30 40 50 60 70 80 90
    do
        /scratch0/langmead-fs1/shared/pypy3-2.4-linux_x86_64-portable/bin/pypy $ERG_HOME/gen_hisat_snps.py --snps $DIR/ingroup_snps.1ksnp --out $DIR/hisat_snps/combined_${MODE}${PCT}_${THR}.txt --sorted-snps $DIR/snps_sorted_by_${MODE}_combo_${THR}.tsv --pct $PCT
    done
done
