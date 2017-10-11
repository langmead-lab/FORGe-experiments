#! /usr/bin/env python2.7

import sys
import bisect

bed = sys.argv[1]
fastq = sys.argv[2]
out = sys.argv[3]
chrom = sys.argv[4]

conf = []
with open(bed, 'r') as f:
  for line in f:
    row = line.rstrip().split('\t')
    if row[0] == 'chr'+chrom:
      conf.append((int(row[1]), int(row[2])))
numc = len(conf)

with open(fastq, 'r') as f_in:
    with open(out, 'w') as f_out:
        include = False
        line_id = 0
        for line in f_in:
            if not line_id % 4 == 0:
                if include:
                    f_out.write(line)
                line_id += 1
                continue
            else:
                include = False
                line_id += 1

            row = line.rstrip().split(' ')
            chrom = None
            start = -1
            end = -1
            for r in row:
                if r[:7] == 'contig=':
                    chrom = r[7:]
                if r[:11] == 'orig_begin=':
                    start = int(r[11:])
                elif r[:9] == 'orig_end=':
                    end = int(r[9:])
                elif r[:5] == 'snps=':
                    snps = int(r[5:])

            if not chrom or start == -1 or end == -1:
                print('Error! Couldn\'t parse line: ' + line.rstrip())
                include = False
                continue

            conf_i = bisect.bisect_left(conf, (start,start))-1
            #print('(%d, %d)' % (start, end))
            #print(conf[conf_i-1:conf_i+2])

            while conf_i < numc and conf[conf_i][0] <= start:
                if conf[conf_i][1] >= end:
                    include = True
                    f_out.write(line)
                    break
                conf_i += 1
