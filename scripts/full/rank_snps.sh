#!/bin/bash

export EXP_HOME=/home-3/mpritt4@jhu.edu/work/jacob/NA12878
export PYTHONPATH=/home-3/mpritt4@jhu.edu/work/jacob/software/jellyfish-2.2.6/install-root/lib/python2.7/site-packages
export VIS_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis/src

cd $EXP_HOME

# VAR_TYPE should be set to either snps or vars
$VIS_HOME/rank.py --method popcov-blowup --reference ../vis_exp_chr9/hs37d5.fa --vars ${VAR_TYPE}_all.1ksnp --window-size 100 --output ordered_${VAR_TYPE}_popcov_blowup.txt

