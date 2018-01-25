#!/bin/bash


./chr9_hisat.py
./chr9_hisat_mem.py

./chr9_erg.py
./chr9_erg_mem.py

./strat_snp.py 0
./strat_rare.py 0
./strat_region.py

./compare_populations.py
