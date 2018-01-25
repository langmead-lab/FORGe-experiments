#!/bin/bash

echo $PREFIX
echo $PCT
echo $HAP

$VIS_HOME/software/hisat2/hisat2 --sam-no-qname-trunc -k 10 -x $INDEX -U $FASTQ -S $SAM
cat $SAM | python2.7 $VIS_HOME/src/correctness/correctness.py $PREFIX $PCT $DESC 
