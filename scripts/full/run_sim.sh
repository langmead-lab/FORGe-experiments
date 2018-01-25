#!/bin/bash

export VAR_TYPE=snps
./rank_snps.sh

export VAR_TYPE=snps
sbatch build_align.sbatch --export=VAR_TYPE

