#!/bin/bash
#SBATCH --partition=shared
#SBATCH --time=24:0:0
#SBATCH --nodes=1
#SBATCH --mem=16G
#SBATCH --ntasks=1

export EXP_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis_exp_chr9
export LD_LIBRARY_PATH=/home/langmead/.linuxbrew/lib:$LD_LIBRARY_PATH
export MASON=/scratch0/langmead-fs1/shared/mason/bin
export VIS_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis/src
export SCRIPT_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis-experiments/scripts

# $EXP_HOME should contain the following files:
##   hs37d5.fa
##   ALL.chr19.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf
##   outgroup.txt

cd $EXP_HOME
export CHR=9
export READLEN=100

for NAME in NA12878
do
    # Generate individual genomes
    mkdir -p indiv_genomes/$NAME
    #$VIS_HOME/update_genome.py --ref hs37d5.fa --vcf ALL.chr${CHR}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf --chrom $CHR --out-prefix indiv_genomes/$NAME/chr$CHR --name $NAME

    # Simulate reads
    cd indiv_genomes/$NAME
    for HAP in A B
    do
        #$MASON/mason illumina -N 5000000 -n $READLEN -hn 1 -i -sq -o sim_l${READLEN}_hap${HAP}.fastq chr9_hap${HAP}.fa

        $SCRIPT_HOME/add_read_info.py $EXP_HOME/NA12878_hap${HAP}.1ksnp $EXP_HOME/clinvar_20170801.vcf $EXP_HOME/ConfidentRegions_hg19.bed $EXP_HOME/chr9_repeats.bed sim_l${READLEN}_hap${HAP}.fastq sim_l${READLEN}_hap${HAP}.tagged.fastq
        #$SCRIPT_HOME/intersect_bed.py $EXP_HOME/ConfidentRegions_hg19.bed sim_l${READLEN}_hap${HAP}.tagged.fastq sim_l${READLEN}_hap${HAP}.conf.tagged.fastq $CHR
    done

    cd $EXP_HOME
done
