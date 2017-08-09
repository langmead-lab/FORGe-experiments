#!/bin/bash

export EXP_HOME=/scratch0/langmead-fs1/user/jacob/vis_exp
export SCRIPT_HOME=/scratch0/langmead-fs1/user/jacob/vis-experiments/scripts

#./simulate.sh $EXP_HOME
#./rank_all.sh $EXP_HOME

cd $EXP_HOME
mkdir -p hisat_snps
mkdir -p hisat_indexes

export MODE=popcov
sbatch $SCRIPT_HOME/build.sbatch --export=MODE

export MODE=popcov_blowup
sbatch $SCRIPT_HOME/build.sbatch --export=MODE
