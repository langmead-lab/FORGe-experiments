#!/bin/bash

export EXP_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis_exp_chr9
export PYTHONPATH=/home-3/mpritt4@jhu.edu/work/jacob/software/jellyfish-2.2.6/install-root/lib/python2.7/site-packages
export VIS_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis/src

cd $EXP_HOME
mkdir -p erg
for MODE in popcov popcov_blowup
do
    for PCT in 2 4 6 8 10 15 20 30 40 50 60 70 80 90 100
    do
        $VIS_HOME/build.py --reference hs37d5.fa --vars snps.1ksnp --window-size 35 --erg erg/chr9_segments_${MODE}${PCT}.fa --sorted ordered_${MODE}.txt --pct $PCT
        cat chr9.fa erg/chr9_segments_${MODE}${PCT}.fa > erg/chr9_${MODE}${PCT}.fa
    done
done
