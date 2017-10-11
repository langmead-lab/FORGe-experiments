#!/bin/bash
#SBATCH --partition=shared
#SBATCH --time=24:0:0
#SBATCH --nodes=1
#SBATCH --mem=16G
#SBATCH --ntasks=1

# Pass in argument MODE=[popcov | popcov-blowup | amb]

export PYTHONPATH=/home-3/mpritt4@jhu.edu/work/jacob/software/jellyfish-2.2.6/install-root/lib/python2.7/site-packages
export VIS_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis
export SCRIPT_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis-experiments/scripts

export LEN=100
export NAME=NA12878
export INDEX=hisat_indexes/hisat_auto

export PREFIX=hisat_auto
export PCT=Auto
export DESC=HISAT

for HAP in A B
do
    export FASTQ=indiv_genomes/$NAME/sim_l${LEN}_hap${HAP}.conf.tagged.fastq
    export SAM=aligned/$NAME/hisat_auto_hap${HAP}_l${LEN}.sam
    export DESC=$HAP
    $SCRIPT_HOME/align.sh
done
