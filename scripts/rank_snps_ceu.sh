#!/bin/bash

export EXP_HOME=$1
export PYTHONPATH=/home-3/mpritt4@jhu.edu/work/jacob/software/jellyfish-2.2.6/install-root/lib/python2.7/site-packages
export VIS_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis/src

# $EXP_HOME should contain the following files:
##   hs37d5.fa
##   ALL.chr19.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf
##   yoruban_ingroup.txt

cd $EXP_HOME
export CHR=9

cd ceu

# Filter SNPs
#$VIS_HOME/vcf_to_1ksnp.py --reference ../hs37d5.fa --vcf ../ALL.chr${CHR}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf --out ceu_snps.1ksnp --individuals ceu_haplotypes.txt --ingroup ceu.txt

# Rank SNPs
$VIS_HOME/rank.py --method popcov --reference ../hs37d5.fa --vars ceu_snps.1ksnp --chrom $CHR --window-size 35 --phasing ceu_haplotypes.txt
mv ordered.txt ordered_popcov.txt

#$VIS_HOME/rank.py --method popcov-blowup --reference ../hs37d5.fa --vars ceu_snps.1ksnp --chrom $CHR --window-size 35 --phasing ceu_haplotypes.txt
#mv ordered.txt ordered_popcov_blowup.txt

$VIS_HOME/rank.py --method amb --reference ../hs37d5.fa --vars ceu_snps.1ksnp --chrom $CHR --window-size 35 --phasing ceu_haplotypes.txt
mv ordered.txt ordered_amb.txt
