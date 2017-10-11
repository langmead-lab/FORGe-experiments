#!/bin/bash
#SBATCH --partition=shared
#SBATCH --time=24:0:0
#SBATCH --nodes=1
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH --array=0,2,4,6,8,10,15,20,30,40,50,60,70,80,90,100

# Pass in argument MODE=[popcov | popcov-blowup | amb]

export PYTHONPATH=/home-3/mpritt4@jhu.edu/work/jacob/software/jellyfish-2.2.6/install-root/lib/python2.7/site-packages
export VIS_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis
export SCRIPT_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis-experiments/scripts

export PCT=$SLURM_ARRAY_TASK_ID
#if [ $PCT = 0 ]; then
#    $SCRIPT_HOME/testMem.py $VIS_HOME/software/hisat2/hisat2-build chr9.fa hisat_indexes/${MODE}${PCT}
#else
#    $VIS_HOME/src/gen_hisat_snps.py --snps snps.1ksnp --out hisat_snps/${MODE}${PCT}.txt --sorted-snps ordered_${MODE}.txt --pct $PCT
#    $SCRIPT_HOME/testMem.py $VIS_HOME/software/hisat2/hisat2-build --snp hisat_snps/${MODE}${PCT}.txt chr9.fa hisat_indexes/${MODE}${PCT}
#fi

export INDEX=hisat_indexes/${MODE}${PCT}

for HAP in A B
do
    export FASTQ=indiv_genomes/$NAME/sim_l${LEN}_hap${HAP}.tagged.fastq
    export SAM=aligned/$NAME/${MODE}${PCT}_hap${HAP}_l${LEN}.sam
    export DESC=$HAP
    $SCRIPT_HOME/align.sh
done
