#!/bin/bash

export EXP_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis_exp_chr9/ceu
export SCRIPT_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis-experiments/scripts

cd $EXP_HOME
mkdir -p hisat_snps
mkdir -p hisat_indexes

#export MODE=popcov
#sbatch $SCRIPT_HOME/build_ceu.sbatch --export=MODE

#export MODE=popcov_blowup
#sbatch $SCRIPT_HOME/build_ceu.sbatch --export=MODE

export MODE=amb
sbatch $SCRIPT_HOME/build_ceu.sbatch --export=MODE
