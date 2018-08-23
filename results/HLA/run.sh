module load java
module load bwa

list=($(ls -d /net/langmead-bigmem.ib.cluster/storage/forge-data/bams_for_vis/*.bam))
#list=($(ls -d /net/langmead-bigmem.ib.cluster/storage/forge-data/bams_for_vis/*var*.bam))

length=${#list[@]}
for_length=$((length - 1))
for i in $(seq 0 $for_length)
do
    # Pre-processing
    # echo ${list[i]}
    path_split=(${list[i]//\// })
    # echo ${path_split[@]}
    name=${path_split[5]}
    # echo ${name[@]}
    name_split=(${name//./ })
    prefix=${name_split[0]}
    echo ${prefix[@]}
    # Extract reads in HLA region
    extracted_bam=${prefix}_extracted_hla.bam
    # echo $extracted_bam
    if [ ! -e "$extracted_bam" ]; then
        samtools view -b ${list[i]} 6:28477797-33448354 > $extracted_bam
    fi
    # Convert bam to fq
    extracted_fq=${prefix}_extracted_hla.fq
    if [ ! -e "$extracted_fq" ]; then
        samtools bam2fq $extracted_bam > $extracted_fq
    fi
    # Align reads using bwa mem on Kourami HLA panel
    realigned=${prefix}_extracted_hla_realign
    realigned_sam=${realigned}.sam
    if [ ! -e "$realigned_sam" ]; then
        bwa mem -t 8 ../../msa/All_FINAL_with_Decoy.fa.gz $extracted_fq > $realigned_sam
    fi
    # Convert sam to bam as Kourami requires
    realigned_bam=${realigned}.bam
    if [ ! -e "$realigned_bam" ]; then
        samtools view -b $realigned_sam > $realigned_bam
    fi
    # Run Kourami
    if [ ! -e "results/${realigned}.result" ]; then
        java -jar /scratch/groups/blangme2/naechyun/software/kourami-0.9.6/build/Kourami.jar -d ~/scratch/forge_hla/kourami/msa -o results/${realigned} ${realigned_bam}
    fi
done
