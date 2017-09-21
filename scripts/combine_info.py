#! /usr/bin/env python2.7

import sys
import bisect

with open(sys.argv[1], 'r') as f_all:
    snps = []
    for line in f_all:
        row = line.rstrip().split('\t')
        snps.append((row[7], row[4]))
    snps.sort()
    names = [s[0] for s in snps]
    num_s = len(snps)

with open(sys.argv[2], 'r') as f_in:
    with open(sys.argv[3], 'w') as f_out:
        for line in f_in:
            row = line.rstrip().split('\t')
            name = row[7]

            found = False
            i = bisect.bisect_left(names, name)

            if i < num_s and names[i] == name:
                row[4] = snps[i][1]
            else:
                row[4] = '0'
            f_out.write('\t'.join(row) + '\n')

