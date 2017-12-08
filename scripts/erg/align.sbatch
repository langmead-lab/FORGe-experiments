#!/bin/bash
#SBATCH --partition=shared
#SBATCH --time=24:0:0
#SBATCH --nodes=1
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH --array=0,2,4,6,8,10,15,20,30,40,50,60,70,80,90

export EXP_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis_exp_chr9
export PYTHONPATH=/home-3/mpritt4@jhu.edu/work/jacob/software/jellyfish-2.2.6/install-root/lib/python2.7/site-packages
export VIS_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis
export SCRIPT_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis-experiments/scripts

echo $MODE

cd $EXP_HOME
export PCT=$SLURM_ARRAY_TASK_ID
module load bowtie
for HAP in A B
do
    $SCRIPT_HOME/testMem.py bowtie -v 0 --sam-no-qname-trunc erg/${MODE}${PCT} indiv_genomes/$NAME/sim_l${LEN}_hap${HAP}.tagged.fastq -S erg/aligned_${MODE}${PCT}_hap${HAP}.sam
    python2.7 $SCRIPT_HOME/erg/flatten_sam.py erg/aligned_${MODE}${PCT}_hap${HAP}.sam erg/aligned_${MODE}${PCT}_hap${HAP}_remapped.sam
    rm erg/aligned_${MODE}${PCT}_hap${HAP}.sam
    cat erg/aligned_${MODE}${PCT}_hap${HAP}_remapped.sam | python2.7 $VIS_HOME/src/correctness/correctness.py $PREFIX $PCT $HAP
    rm erg/aligned_${MODE}${PCT}_hap${HAP}_remapped.sam
done
