#!/bin/bash
#SBATCH --partition=shared
#SBATCH --time=36:0:0
#SBATCH --nodes=1
#SBATCH --mem=4G
#SBATCH --ntasks=1
#SBATCH --array=0,10,20,30,40,50,60,70,80,90,100

# Pass in argument MODE=[popcov | popcov-blowup | amb]

export PYTHONPATH=/scratch0/langmead-fs1/shared/jellyfish-2.2.5/install-root/lib/python2.7/site-packages
export VIS_HOME=/scratch0/langmead-fs1/user/jacob/vis

if [ $SLURM_ARRAY_TASK_ID = 0 ]; then
   $VIS_HOME/software/hisat2/hisat2-build chr19.fa hisat_indexes/${MODE}${SLURM_ARRAY_TASK_ID}
else
    $VIS_HOME/src/gen_hisat_snps.py --snps snps.1ksnp --out hisat_snps/${MODE}${SLURM_ARRAY_TASK_ID}.txt --sorted-snps ordered_${MODE}.txt --pct $SLURM_ARRAY_TASK_ID 
    $VIS_HOME/software/hisat2/hisat2-build --snp hisat_snps/${MODE}${SLURM_ARRAY_TASK_ID}.txt chr19.fa hisat_indexes/${MODE}${SLURM_ARRAY_TASK_ID}
fi

for NAME in NA12878
do
    for HAP in A B
    do
        $VIS_HOME/software/hisat2/hisat2 --sam-no-qname-trunc -x hisat_indexes/${MODE}${SLURM_ARRAY_TASK_ID} -U indiv_genomes/$NAME/sim_hap${HAP}.fastq -S aligned/$NAME/${MODE}${SLURM_ARRAY_TASK_ID}_hap${HAP}.sam
        cat aligned/$NAME/${MODE}${SLURM_ARRAY_TASK_ID}_hap${HAP}.sam | /usr/local/bin/python2.7 $VIS_HOME/src/correctness/correctness.py accuracy_${MODE}.txt ${SLURM_ARRAY_TASK_ID} $HAP 
    done
done
