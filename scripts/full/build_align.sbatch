#!/bin/bash
#SBATCH --partition=lrgmem
#SBATCH --time=24:0:0
#SBATCH --nodes=1
#SBATCH --mem=1000G
#SBATCH --ntasks=1
#SBATCH --array=0,2,4,6,8,10,15,20,30,40,50,60,70,80

export EXP_HOME=/home-3/mpritt4@jhu.edu/work/jacob/NA12878
export VIS_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis

export MODE=popcov_blowup
export PCT=$SLURM_ARRAY_TASK_ID
export VAR_TYPE=vars

cd $EXP_HOME
export INDEX=hisat_indexes/${VAR_TYPE}_${MODE}${PCT}
if [ $PCT = 0 ]; then
    $VIS_HOME/software/hisat2/hisat2-build ../vis_exp_chr9/hs37d5.fa  hisat_indexes/${VAR_TYPE}_${MODE}${PCT}
else
    $VIS_HOME/src/gen_hisat_snps.py --snps ${VAR_TYPE}_all.1ksnp --out hisat_snps/${VAR_TYPE}_${MODE}${PCT}.txt --sorted-snps ordered_${VAR_TYPE}_${MODE}.txt --pct $PCT
    $VIS_HOME/software/hisat2/hisat2-build --snp hisat_snps/${VAR_TYPE}_${MODE}${PCT}.txt hs37d5.fa $INDEX
fi

for HAP in A B
do
    export FASTQ=sim_hap${HAP}_l100.fastq
    export SAM=aligned/${VAR_TYPE}_${MODE}${PCT}.sam
    export DESC=$HAP

    $VIS_HOME/software/hisat2/hisat2 --sam-no-qname-trunc -k 10 -x $INDEX -U $FASTQ -S $SAM
    cat $SAM | python2.7 $VIS_HOME/src/correctness/correctness.py ${VAR_TYPE}_accuracy $PCT $DESC 
done
