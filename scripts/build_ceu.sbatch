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

if [ $SLURM_ARRAY_TASK_ID = 0 ]; then
   $VIS_HOME/software/hisat2/hisat2-build ../chr9.fa hisat_indexes/${MODE}${SLURM_ARRAY_TASK_ID}
else
    $VIS_HOME/src/gen_hisat_snps.py --snps ceu_snps.1ksnp --out hisat_snps/${MODE}${SLURM_ARRAY_TASK_ID}.txt --sorted-snps ordered_${MODE}.txt --pct $SLURM_ARRAY_TASK_ID 
    $VIS_HOME/software/hisat2/hisat2-build --snp hisat_snps/${MODE}${SLURM_ARRAY_TASK_ID}.txt ../chr9.fa hisat_indexes/${MODE}${SLURM_ARRAY_TASK_ID}
fi

export LEN=100
export NAME=NA12878

export PREFIX=accuracy_${MODE}_l${LEN}
rm -f ${PREFIX}.tsv
printf "Pct\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.tsv
rm -f ${PREFIX}.strat_snp.tsv
printf "Pct\tSNPs\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_snp.tsv
rm -f ${PREFIX}.strat_rare.tsv
printf "Pct\tRareSNPs\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_rare.tsv
rm -f ${PREFIX}.strat_snp.tsv
printf "Pct\tDelSNPs\tHap\tAligned\tCorrect\tOverall\n" > ${PREFIX}.strat_del.tsv
mkdir -p aligned/$NAME
for HAP in A B
do
    $SCRIPT_HOME/testMem.py $VIS_HOME/software/hisat2/hisat2 --sam-no-qname-trunc --score-min C,-50 -x hisat_indexes/${MODE}${SLURM_ARRAY_TASK_ID} -U ../indiv_genomes/$NAME/sim_l${LEN}_hap${HAP}.tagged.fastq -S aligned/$NAME/${MODE}${SLURM_ARRAY_TASK_ID}_hap${HAP}_l${LEN}.sam
    cat aligned/$NAME/${MODE}${SLURM_ARRAY_TASK_ID}_hap${HAP}_l${LEN}.sam | python2.7 $VIS_HOME/src/correctness/correctness.py $PREFIX ${SLURM_ARRAY_TASK_ID} $HAP 
done
