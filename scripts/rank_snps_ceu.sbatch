#!/bin/bash
#SBATCH --partition=lrgmem
#SBATCH --time=48:0:0
#SBATCH --nodes=1
#SBATCH --mem=1000G
#SBATCH --ntasks=1

export EXP_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis_exp_chr9/ceu
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
$VIS_HOME/vcf_to_1ksnp.py --reference ../hs37d5.fa --vcf ../ALL.chr${CHR}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf --out ceu_snps.1ksnp --individuals ceu_haplotypes.txt --ingroup ceu.txt

# Rank SNPs
$VIS_HOME/rank.py --method popcov --reference ../hs37d5.fa --vars ceu_snps.1ksnp --chrom $CHR --window-size 35 --phasing ceu_haplotypes.txt
mv ordered.txt ordered_popcov.txt

$VIS_HOME/rank.py --method popcov-blowup --reference ../hs37d5.fa --vars ceu_snps.1ksnp --chrom $CHR --window-size 35 --phasing ceu_haplotypes.txt
mv ordered.txt ordered_popcov_blowup.txt

echo 'Ranking ambiguity, r=35'
$VIS_HOME/rank.py --method amb --reference ../hs37d5.fa --vars ceu_snps.1ksnp --chrom $CHR --window-size 35 --phasing ceu_haplotypes.txt
mv ordered.txt ordered_amb35.txt
mv ordered.txt.blowup ordered_amb_blowup35.txt

echo 'Ranking ambiguity, r=100'
$VIS_HOME/rank.py --method amb --reference ../hs37d5.fa --vars ceu_snps.1ksnp --chrom $CHR --window-size 100 --phasing ceu_haplotypes.txt
mv ordered.txt ordered_amb100.txt
mv ordered.txt.blowup ordered_amb_blowup100.txt
