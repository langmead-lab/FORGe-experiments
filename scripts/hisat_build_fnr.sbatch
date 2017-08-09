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

$ERG_HOME/software/hisat2/hisat2-build --snp $DIR/hisat_snps/${MODE}${SLURM_ARRAY_TASK_ID}_0.5.txt -p 1 $DIR/chr19.fa $DIR/hisat_indexes/${MODE}${SLURM_ARRAY_TASK_ID}_0.5
