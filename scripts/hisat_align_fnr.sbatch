#!/bin/bash
#SBATCH --partition=shared
#SBATCH --time=36:0:0
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --array=10,20,30,40,50,60,70,80,90

export PYTHONPATH=/scratch0/langmead-fs1/shared/jellyfish-2.2.5/install-root/lib/python2.7/site-packages
export ERG_HOME=/scratch0/langmead-fs1/user/jacob/enhanced_reference_genome
export DIR=/scratch0/langmead-fs1/user/jacob/1000genomes/chr19

export MODE=combined_pop_cov
echo $MODE, ${SLURM_ARRAY_TASK_ID}
export THR=0.5
echo $THR

#for NAME in NA18510 NA18879 NA19153 NA19201 NA19235
for NAME in NA18510
do
    $ERG_HOME/software/hisat2/hisat2 --sam-no-qname-trunc -t -k 1 -x $DIR/hisat_indexes/${MODE}${SLURM_ARRAY_TASK_ID}_$THR -U $DIR/indiv_genomes/$NAME/sim_l35_hapA_vars.fastq -S $DIR/aligned/$NAME/hapA_${MODE}${SLURM_ARRAY_TASK_ID}_${THR}.sam
    #cat $DIR/aligned/$NAME/hapA_combined_${MODE}${SLURM_ARRAY_TASK_ID}_${THR}.sam | /usr/local/bin/python2.7 $ERG_HOME/src/correctness/correctness.py

    $ERG_HOME/software/hisat2/hisat2 --sam-no-qname-trunc -t -k 1 -x $DIR/hisat_indexes/${MODE}${SLURM_ARRAY_TASK_ID}_$THR -U $DIR/indiv_genomes/$NAME/sim_l35_hapB_vars.fastq -S $DIR/aligned/$NAME/hapB_${MODE}${SLURM_ARRAY_TASK_ID}_${THR}.sam
    #cat $DIR/aligned/$NAME/hapB_combined_${MODE}${SLURM_ARRAY_TASK_ID}_${THR}.sam | /usr/local/bin/python2.7 $ERG_HOME/src/correctness/correctness.py
done

