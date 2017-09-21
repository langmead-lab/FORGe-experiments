#!/bin/bash

# Add info to simulated reads on # total, rare, and deleterious variants

export EXP_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis_exp_chr9
export SCRIPT_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis-experiments/scripts

cd $EXP_HOME
#wget ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar_20170801.vcf.gz
#gunzip clinvar_20170801.vcf.gz

for HAP in A B
do
    $SCRIPT_HOME/add_read_info.py NA12878_adjusted.1ksnp clinvar_20170801.vcf indiv_genomes/NA12878/sim_l100_hap${HAP}.fastq indiv_genomes/NA12878/sim_l100_hap${HAP}.tagged.fastq
done
