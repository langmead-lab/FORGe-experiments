#!/bin/bash

export EXP_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis_exp_genome_size
export SCRIPT_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis-experiments/scripts/genome_size

cd $EXP_HOME
for i in 1
do
    echo 'Experiment ' $i:
    cd exp$i

    for NCHROM in 1 6 12 17 23
    do
        echo $NCHROM chroms:
        $SCRIPT_HOME/get_genome_lens.py chroms${NCHROM}.fa        
    done
done
