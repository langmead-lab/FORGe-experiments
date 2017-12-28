
To run the FORGe experiments, you must have Mason and HISAT2 installed.
Jellyfish should also be installed with python bindings.
Before running, modify the following path variables in run_all.sh, simulate.sh, rank_snps.sh, and add_read_info.sh

EXP_HOME - Experiment directory. Initially,$EXP_HOME should contain the following files:
##   hs37d5.fa
##   ALL.chr19.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf
##   outgroup.txt
MASON - Directory containing Mason executable
VIS_HOME - FORGe src directory
SCRIPT_HOME - vis-experiments/scripts directory

To run FORGe, build HISAT indexes, and align reads, execute
> ./run_all.sh
This script will simulate reads from NA12878, parse SNPs and rank them with FORGe, generate HISAT indexes and align the simulated reads to them for various percentages of SNPs. The resulting accuracies will be written to files chr9_all_[RANK_METHOD]_l100.tsv with accompanying stratified results.

To run the same pipeline for only CEU SNPs, execute:
> ./rank_snps_ceu.sh
> ./build_all_ceu.sh

To run the build and align with the ERG instead of HISAT2, run:
> sbatch ceu/build.sbatch
> ./ceu/align_all.sh


