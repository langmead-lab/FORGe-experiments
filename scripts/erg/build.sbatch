#!/bin/bash
#SBATCH --partition=lrgmem
#SBATCH --time=2:0:0
#SBATCH --nodes=1
#SBATCH --mem=100G
#SBATCH --ntasks=1
#SBATCH --array=2,4,6,8,10,15,20,30,40,50,60,70,80,90

export EXP_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis_exp_chr9
export PYTHONPATH=/home-3/mpritt4@jhu.edu/work/jacob/software/jellyfish-2.2.6/install-root/lib/python2.7/site-packages
export VIS_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis/src
export SCRIPT_HOME=/home-3/mpritt4@jhu.edu/work/jacob/vis-experiments/scripts

cd $EXP_HOME
mkdir -p erg
export PCT=$SLURM_ARRAY_TASK_ID
module load bowtie
for MODE in amb_blowup
do
        $VIS_HOME/build.py --reference hs37d5.fa --vars snps.1ksnp --window-size 25 --erg erg/chr9_segments_${MODE}${PCT}.fa --sorted ordered_${MODE}25.txt --pct $PCT
        echo 'Finished generating fasta'
        cat chr9.fa erg/chr9_segments_${MODE}${PCT}.fa > erg/chr9_${MODE}${PCT}.fa
        rm erg/chr9_segments_${MODE}${PCT}.fa
        $SCRIPT_HOME/testMem.py bowtie-build erg/chr9_${MODE}${PCT}.fa erg/${MODE}${PCT}
        rm erg/chr9_${MODE}${PCT}.fa
done
