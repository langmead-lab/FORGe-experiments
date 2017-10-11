#!/bin/bash

export EXP_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis_exp_chr9/ceu
export SCRIPT_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis-experiments/scripts

cd $EXP_HOME
mkdir -p hisat_snps
mkdir -p hisat_indexes

mkdir -p aligned/$NAME

export LEN=100
export NAME=NA12878

export MODE=popcov
export PREFIX=accuracy_${MODE}_l${LEN}
rm -f ${PREFIX}.tsv
printf "Pct\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.tsv
rm -f ${PREFIX}.strat_snp.tsv
printf "Pct\tSNPs\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_snp.tsv
rm -f ${PREFIX}.strat_rare.tsv
printf "Pct\tRareSNPs\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_rare.tsv
rm -f ${PREFIX}.strat_snp.tsv
printf "Pct\tDelSNPs\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_del.tsv
sbatch $SCRIPT_HOME/build_ceu.sbatch --export=MODE,LEN,NAME,PREFIX

export MODE=popcov_blowup
export PREFIX=accuracy_${MODE}_l${LEN}
rm -f ${PREFIX}.tsv
printf "Pct\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.tsv
rm -f ${PREFIX}.strat_snp.tsv
printf "Pct\tSNPs\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_snp.tsv
rm -f ${PREFIX}.strat_rare.tsv
printf "Pct\tRareSNPs\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_rare.tsv
rm -f ${PREFIX}.strat_snp.tsv
printf "Pct\tDelSNPs\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_del.tsv
sbatch $SCRIPT_HOME/build_ceu.sbatch --export=MODE,LEN,NAME,PREFIX

export MODE=amb
export PREFIX=accuracy_${MODE}_l${LEN}
rm -f ${PREFIX}.tsv
printf "Pct\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.tsv
rm -f ${PREFIX}.strat_snp.tsv
printf "Pct\tSNPs\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_snp.tsv
rm -f ${PREFIX}.strat_rare.tsv
printf "Pct\tRareSNPs\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_rare.tsv
rm -f ${PREFIX}.strat_snp.tsv
printf "Pct\tDelSNPs\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_del.tsv
sbatch $SCRIPT_HOME/build_ceu.sbatch --export=MODE,LEN,NAME,PREFIX

export MODE=amb_blowup
export PREFIX=accuracy_${MODE}_l${LEN}
rm -f ${PREFIX}.tsv
printf "Pct\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.tsv
rm -f ${PREFIX}.strat_snp.tsv
printf "Pct\tSNPs\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_snp.tsv
rm -f ${PREFIX}.strat_rare.tsv
printf "Pct\tRareSNPs\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_rare.tsv
rm -f ${PREFIX}.strat_snp.tsv
printf "Pct\tDelSNPs\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_del.tsv
sbatch $SCRIPT_HOME/build_ceu.sbatch --export=MODE,LEN,NAME,PREFIX
