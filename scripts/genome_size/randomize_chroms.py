#! /usr/bin/env python2.7

import sys
import random

chroms = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', 'X']

out_file = sys.argv[1]
with open(out_file, 'w') as f:
    random.shuffle(chroms)
    f.write('\n'.join(chroms) + '\n')
