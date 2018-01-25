#!/bin/bash
#SBATCH --partition=lrgmem
#SBATCH --time=72:0:0
#SBATCH --nodes=1
#SBATCH --mem=1000G
#SBATCH --ntasks=1
#SBATCH --array=0,2,4,6,8,10,15,20,30,40,50,60,70,80

export EXP_HOME=/home-3/mpritt4@jhu.edu/work/jacob/NA12878
export SCRIPT_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis-experiments/scripts
export VIS_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis

export PCT=$SLURM_ARRAY_TASK_ID

cd $EXP_HOME
export INDEX=hisat_indexes/${VAR_TYPE}_${MODE}${PCT}
if [ $PCT = 0 ]; then
    $VIS_HOME/software/hisat2/hisat2-build ../vis_exp_chr9/hs37d5.fa  hisat_indexes/${VAR_TYPE}_${MODE}${PCT}
else
    $VIS_HOME/src/gen_hisat_snps.py --snps ${VAR_TYPE}_all.1ksnp --out hisat_snps/${VAR_TYPE}_${MODE}${PCT}.txt --sorted-snps ordered_${VAR_TYPE}_${MODE}.txt --pct $PCT
    $VIS_HOME/software/hisat2/hisat2-build --snp hisat_snps/${VAR_TYPE}_${MODE}${PCT}.txt hs37d5.fa $INDEX
fi

$VIS_HOME/software/hisat2/hisat2 --sam-no-qname-trunc -k 10 -x $INDEX -U ERR194147_1.fastq -S ERR194147_${PCT}.sam
$SCRIPT_HOME/unique_perfect.sh ERR194147_${PCT}.sam

$VIS_HOME/software/hisat2/hisat2 --sam-no-qname-trunc -k 10 -x $INDEX -U ERR194147_2.fastq -S ERR194147_${PCT}.sam
$SCRIPT_HOME/unique_perfect.sh ERR194147_${PCT}.sam

# For space reasons, remove SAM files
rm ERR194147_${PCT}.sam

