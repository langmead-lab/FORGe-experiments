#! /usr/bin/env python2.7

import sys

with open(sys.argv[1], 'r') as f:
    length = 0
    for line in f:
        if line[0] == '>':
            continue

        length += len(line.rstrip())

print('%d bases long' % length)
