#!/bin/bash
#SBATCH --partition=lrgmem
#SBATCH --time=48:0:0
#SBATCH --nodes=1
#SBATCH --mem=1000G
#SBATCH --ntasks=1
#SBATCH --array=100

# Pass in argument MODE=[popcov | popcov-blowup | amb]

export PYTHONPATH=/home-3/mpritt4@jhu.edu/work/jacob/software/jellyfish-2.2.6/install-root/lib/python2.7/site-packages
export VIS_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis
export SCRIPT_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis-experiments/scripts

if [ $SLURM_ARRAY_TASK_ID = 0 ]; then
   $VIS_HOME/software/hisat2/hisat2-build chr9.fa hisat_indexes/${MODE}${SLURM_ARRAY_TASK_ID}
else
    #$VIS_HOME/src/gen_hisat_snps.py --snps snps.1ksnp --out hisat_snps/${MODE}${SLURM_ARRAY_TASK_ID}.txt --sorted-snps ordered_${MODE}.txt --pct $SLURM_ARRAY_TASK_ID 
    $SCRIPT_HOME/testMem.py $VIS_HOME/software/hisat2/hisat2-build --snp hisat_snps/${MODE}${SLURM_ARRAY_TASK_ID}.txt chr9.fa hisat_indexes/${MODE}${SLURM_ARRAY_TASK_ID}
fi

#for NAME in NA12878
#do
#    mkdir -p aligned/$NAME
#    for HAP in A B
#    do
#        $VIS_HOME/software/hisat2/hisat2 --sam-no-qname-trunc -x hisat_indexes/${MODE}${SLURM_ARRAY_TASK_ID} -U indiv_genomes/$NAME/sim_hap${HAP}.fastq -S aligned/$NAME/${MODE}${SLURM_ARRAY_TASK_ID}_hap${HAP}.sam
#        cat aligned/$NAME/${MODE}${SLURM_ARRAY_TASK_ID}_hap${HAP}.sam | python2.7 $VIS_HOME/src/correctness/correctness.py accuracy_${MODE}.txt ${SLURM_ARRAY_TASK_ID} $HAP 
#    done
#done
