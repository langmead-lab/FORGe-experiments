#! /usr/bin/env python

'''
Plot # Unique vs # Perfect mappings for experimental reads aligned against the full genome
'''

import matplotlib.pyplot as plt
import math

font = {'size': 18}
plt.rc('font', **font)

def val(row, label, header):
    if label in header:
        return row[header[label]]
    else:
        return None

unique_labels = ['UniqueA', 'UniqueB']
perfect_labels = ['PerfectA', 'PerfectB']

pct = []
unique = []
perfect = []
unique_auto = 0
perfect_auto = 0
with open('../results/full_genome/unique_perfect_vars.tsv', 'r') as f:
    header_line = f.readline()
    while header_line[0] == '#':
        header_line = f.readline()
    header_line = header_line.rstrip().split('\t')
    header = dict()
    for i in range(len(header_line)):
        header[header_line[i]] = i

    for line in f:
        row = line.rstrip('\n').split('\t')
        curr_pct = val(row, 'Pct', header)

        if curr_pct == 'Auto':
            for h in unique_labels:
                v = val(row, h, header)
                if v:
                    unique_auto += float(v) / 1000000000
            for h in perfect_labels:
                v = val(row, h, header)
                if v:
                    perfect_auto += float(v) / 1000000000
        else:
            pct.append(curr_pct)

            unique.append(0)
            for h in unique_labels:
                v = val(row, h, header)
                if v:
                    unique[-1] += float(v) / 1000000000

            perfect.append(0)
            for h in perfect_labels:
                v = val(row, h, header)
                if v:
                    perfect[-1] += float(v) / 1000000000

width = 3
plt.plot(unique, perfect, color='blue')
plt.scatter(unique[1:-1], perfect[1:-1], facecolors='blue', marker='o', s=20)
index10 = pct.index('10')
plt.scatter(unique[index10], perfect[index10], marker='*', s=150, facecolors='b')
plt.scatter(unique_auto, perfect_auto, marker='*', s=150, facecolors='r')

xlim = [0.7215, 0.7245]
ylim = [0.7, 0.77]
dx = (unique[-1] - unique[-2]) / (xlim[1]-xlim[0])
dy = (perfect[-1] - perfect[-2]) / (ylim[1]-ylim[0])
plt.plot(unique[-1], perfect[-1], color='blue', marker=(3, 1, -90+math.degrees(math.atan2(dy,dx))), ms=10)
plt.plot(unique[0], perfect[0], color='blue', marker='o', ms=6)

plt.xlabel('# Unique Mappings (Billions)')
plt.ylabel('# Perfect Mappings (Billions)')
ax = plt.gca()
ax.get_xaxis().get_major_formatter().set_useOffset(False)
plt.draw()
plt.savefig('full_unique_perfect.png', bbox_inches='tight')
plt.clf()
