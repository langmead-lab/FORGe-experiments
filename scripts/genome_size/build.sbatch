#!/bin/bash
#SBATCH --partition=lrgmem
#SBATCH --time=24:0:0
#SBATCH --nodes=1
#SBATCH --mem=100G
#SBATCH --ntasks=1
#SBATCH --array=7,8

# Pass in argument MODE=[popcov | popcov-blowup | amb]

export PYTHONPATH=/home-3/mpritt4@jhu.edu/work/jacob/software/jellyfish-2.2.6/install-root/lib/python2.7/site-packages
export VIS_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis
export SCRIPT_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis-experiments/scripts

if [ $SLURM_ARRAY_TASK_ID = 0 ]; then
    $VIS_HOME/software/hisat2/hisat2-build ../chroms${NCHROM}.fa ${SLURM_ARRAY_TASK_ID}pct
else
    $VIS_HOME/src/gen_hisat_snps.py --snps ../snps_${NCHROM}.1ksnp --out ${SLURM_ARRAY_TASK_ID}.5pct_snps.txt --sorted-snps ordered.txt --pct ${SLURM_ARRAY_TASK_ID}.5 
    $VIS_HOME/software/hisat2/hisat2-build --snp ${SLURM_ARRAY_TASK_ID}.5pct_snps.txt ../chroms${NCHROM}.fa ${SLURM_ARRAY_TASK_ID}.5pct
fi

$VIS_HOME/software/hisat2/hisat2 --sam-no-qname-trunc --score-min C,-50 -x ${SLURM_ARRAY_TASK_ID}.5pct -U ../sim_chroms${NCHROM}.fastq -S aligned${SLURM_ARRAY_TASK_ID}.5.sam
cat aligned${SLURM_ARRAY_TASK_ID}.5.sam | python2.7 $VIS_HOME/src/correctness/correctness.py accuracy ${SLURM_ARRAY_TASK_ID}.5 A

