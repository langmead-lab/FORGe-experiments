#!/bin/bash
#SBATCH --partition=lrgmem
#SBATCH --time=96:0:0
#SBATCH --nodes=1
#SBATCH --mem=1000G
#SBATCH --ntasks=1

export EXP_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis_exp_chr9
export PYTHONPATH=/home-3/mpritt4@jhu.edu/work/jacob/software/jellyfish-2.2.6/install-root/lib/python2.7/site-packages
export VIS_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis/src

cd $EXP_HOME

$VIS_HOME/rank.py --method amb --reference hs37d5.fa --vars snps.1ksnp --chrom 9 --window-size 100 --phasing haplotypes.txt
