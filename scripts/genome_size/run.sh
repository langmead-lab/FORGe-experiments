#!/bin/bash

export EXP_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis_exp_genome_size
export SCRIPT_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis-experiments/scripts/genome_size
export PYTHONPATH=/home-3/mpritt4@jhu.edu/work/jacob/software/jellyfish-2.2.6/install-root/lib/python2.7/site-packages
export VIS_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis/src

cd $EXP_HOME

for i in 1
do
    #mkdir -p exp$i
    cd exp$i
    #$SCRIPT_HOME/randomize_chroms.py order.txt

    # Manually cat 1ksnp files because it's easier than writing a script


    for NCHROM in 1 6 12 17 23
    do
        mkdir -p chroms$NCHROM
        cd chroms$NCHROM
        $VIS_HOME/rank.py --method popcov-blowup --reference ../../../vis_exp_chr9/hs37d5.fa --vars ../snps_${NCHROM}.1ksnp --window-size 35
        cd ../
    done
    cd ../
done
