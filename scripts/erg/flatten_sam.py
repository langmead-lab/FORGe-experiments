#! /usr/bin/env python

import sys

with open(sys.argv[1], 'r') as f_in:
    with open(sys.argv[2], 'w') as f_out:
        for line in f_in:
            row = line.rstrip().split('\t')

            # Header line
            if line[0] == '@':
                if line[1:3] == 'SQ' and len(row[1].split(':')) > 2:
                    continue
                else:
                    f_out.write(line)
            else:
                mapping = row[2].split(':')
                if len(mapping) > 1:
                    row[2] = mapping[0]
                    row[3] = str(int(row[3]) + int(mapping[1]))
                    # Can't figure out how Satya's original mapping script uses variant number (mapping[2])
                    f_out.write('\t'.join(row) + '\n')
                else:
                    f_out.write(line)
