#!/bin/bash

export VAR_TYPE=vars
./rank_snps.sh

export VAR_TYPE=vars
sbatch unique_perfect.sbatch --export=VAR_TYPE
