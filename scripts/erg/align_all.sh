#!/bin/bash

export EXP_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis_exp_chr9
export SCRIPT_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis-experiments/scripts

#./simulate.sh $EXP_HOME
#./rank_snps.sh $EXP_HOME
#./add_read_info.sh $EXP_HOME

cd $EXP_HOME
mkdir -p hisat_snps
mkdir -p hisat_indexes

mkdir -p aligned/$NAME

export LEN=25
export NAME=NA12878

export MODE=popcov
export PREFIX=accuracy_bowtie_${MODE}_l${LEN}_v0
rm -f ${PREFIX}.tsv
printf "Pct\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.tsv
rm -f ${PREFIX}.strat_snp.tsv
printf "Pct\tSNPs\tTotal\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_snp.tsv
rm -f ${PREFIX}.strat_rare.tsv
printf "Pct\tRareSNPs\tTotal\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_rare.tsv
rm -f ${PREFIX}.strat_snp.tsv
printf "Pct\tDelSNPs\tTotal\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_del.tsv
rm -f ${PREFIX}.strat_conf.tsv
printf "Pct\tConf\tTotal\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_conf.tsv
rm -f ${PREFIX}.strat_rep.tsv
printf "Pct\tConf\tTotal\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_rep.tsv
sbatch $SCRIPT_HOME/erg/align.sbatch --export=MODE,LEN,NAME,PREFIX

export MODE=popcov_blowup
export PREFIX=accuracy_bowtie_${MODE}_l${LEN}_v0
rm -f ${PREFIX}.tsv
printf "Pct\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.tsv
rm -f ${PREFIX}.strat_snp.tsv
printf "Pct\tSNPs\tTotal\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_snp.tsv
rm -f ${PREFIX}.strat_rare.tsv
printf "Pct\tRareSNPs\tTotal\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_rare.tsv
rm -f ${PREFIX}.strat_snp.tsv
printf "Pct\tDelSNPs\tTotal\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_del.tsv
rm -f ${PREFIX}.strat_conf.tsv
printf "Pct\tConf\tTotal\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_conf.tsv
rm -f ${PREFIX}.strat_rep.tsv
printf "Pct\tConf\tTotal\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_rep.tsv
sbatch $SCRIPT_HOME/erg/align.sbatch --export=MODE,LEN,NAME,PREFIX

export MODE=amb
export PREFIX=accuracy_bowtie_${MODE}_l${LEN}_v0
rm -f ${PREFIX}.tsv
printf "Pct\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.tsv
rm -f ${PREFIX}.strat_snp.tsv
printf "Pct\tSNPs\tTotal\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_snp.tsv
rm -f ${PREFIX}.strat_rare.tsv
printf "Pct\tRareSNPs\tTotal\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_rare.tsv
rm -f ${PREFIX}.strat_snp.tsv
printf "Pct\tDelSNPs\tTotal\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_del.tsv
rm -f ${PREFIX}.strat_conf.tsv
printf "Pct\tConf\tTotal\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_conf.tsv
rm -f ${PREFIX}.strat_rep.tsv
printf "Pct\tConf\tTotal\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_rep.tsv
sbatch $SCRIPT_HOME/erg/align.sbatch --export=MODE,LEN,NAME,PREFIX

export MODE=amb_blowup
export PREFIX=accuracy_bowtie_${MODE}_l${LEN}_v0
rm -f ${PREFIX}.tsv
printf "Pct\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.tsv
rm -f ${PREFIX}.strat_snp.tsv
printf "Pct\tSNPs\tTotal\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_snp.tsv
rm -f ${PREFIX}.strat_rare.tsv
printf "Pct\tRareSNPs\tTotal\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_rare.tsv
rm -f ${PREFIX}.strat_snp.tsv
printf "Pct\tDelSNPs\tTotal\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_del.tsv
rm -f ${PREFIX}.strat_conf.tsv
printf "Pct\tConf\tTotal\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_conf.tsv
rm -f ${PREFIX}.strat_rep.tsv
printf "Pct\tConf\tTotal\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_rep.tsv
sbatch $SCRIPT_HOME/erg/align.sbatch --export=MODE,LEN,NAME,PREFIX

