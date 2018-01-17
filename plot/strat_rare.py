#! /usr/bin/env python

'''
Plot chromosome-specific accuracy results
'''

import matplotlib.pyplot as plt
import sys
import math

STRAT_PREFIX = 'strat_rare'
STRAT_LABEL = 'RareSNPs'
STRAT_DESC = ['1 Common SNP', '1 Rare SNP']
MAX_STRAT = 1
COLORS = ['blue', 'green']

######

RANK_MODE = int(sys.argv[1])
if RANK_MODE == 0:
    RANK_NAME = 'popcov'
    RANK_DESC = 'Population Coverage'
elif RANK_MODE == 1:
    RANK_NAME = 'popcov_blowup'
    RANK_DESC = 'Population Coverage + Blowup'
elif RANK_MODE == 2:
    RANK_NAME = 'amb'
    RANK_DESC = 'Ambiguity'
elif RANK_MODE == 3:
    RANK_NAME = 'amb_blowup'
    RANK_DESC = 'Ambiguity + Blowup'

######


chrom = '9'

font = {'size': 18}
plt.rc('font', **font)

def val(row, label, header):
    if label in header:
        return row[header[label]]
    else:
        return None

def read_tsv(filename):
    with open(filename, 'r') as f:
        header_line = f.readline()
        while header_line[0] == '#':
            header_line = f.readline()
        header_line = header_line.rstrip().split('\t')
        header = dict()
        for i in range(len(header_line)):
            header[header_line[i]] = i

        results = dict()
        for line in f:
            row = line.rstrip().split('\t')
            pct = int(val(row, 'Pct', header))
            aligned = float(val(row, 'Aligned', header))
            correct = float(val(row, 'Correct', header))
            overall = float(val(row, 'Overall', header))
            strat = int(val(row, STRAT_LABEL, header))
            num = int(val(row, 'Total', header))

            if strat > MAX_STRAT:
                continue

            if pct in results:
                prev = results[pct][strat]
                if not prev:
                    results[pct][strat] = (aligned*num, correct*num, overall*num, num)
                else:
                    results[pct][strat] = (prev[0]+aligned*num, prev[1]+correct*num, prev[2]+overall*num, prev[3]+num)
            else:
                results[pct] = [None] * (MAX_STRAT+1)
                results[pct][strat] = (aligned*num, correct*num, overall*num, num)

    for res in results.values():
        for i in range(MAX_STRAT+1):
            if not res[i]:
                res[i] = (0,0,0,0)
            else:
                count = res[i][3]
                res[i] = (res[i][0]/count, res[i][1]/count, res[i][2]/count)

    return results

def findOptPoint(correct, incorrect):
    num = len(correct)
    #p = [correct[i]/aligned[i] for i in range(num)]
    #r = [correct[i]/(100-aligned[i]+correct[i]) for i in range(num)]
    #score = [2*p[i]*r[i]/(p[i]+r[i]) for i in range(num)]

    # correct - incorrect
    score = [correct[i] - incorrect[i] for i in range(num)]

    max_id = 0
    for i in range(1,num):
        if score[i] > score[max_id]:
            max_id = i
    return max_id

def results_from_dict(results):
    pct = sorted(results.keys())
    
    aligned = []
    correct = []
    overall = []
    incorrect = []
    opt = []

    for i in range(MAX_STRAT+1):
        aligned.append([100*results[p][i][0] for p in pct])
        correct.append([100*results[p][i][1] for p in pct])
        overall.append([100*results[p][i][2] for p in pct])
        incorrect.append([aligned[i][p] * (100-correct[i][p]) / 100 for p in range(len(pct))])
        opt.append(findOptPoint(overall[i], incorrect[i]))

    return pct, aligned, correct, overall, incorrect, opt


#########################

results = read_tsv('../results/chr9_all_'+RANK_NAME+'_safe.strat_rare.tsv')
pct, aligned, correct, accuracy, incorrect, opt = results_from_dict(results)


#########################

width = 3

plt.figure(figsize=(10,10))

xlim = [0.2, 0.45]
ylim = [93, 97]

f, axs = plt.subplots(2, 2, figsize=(20,20))
for i in range(MAX_STRAT+1):
    lab = STRAT_DESC[i]
    axs[0,0].plot(pct, aligned[i], label=lab, linewidth=width, color=COLORS[i])
    axs[0,0].plot(pct[opt[i]], aligned[i][opt[i]], color=COLORS[i], marker='D', ms=10)

axs[0,0].set_xlabel('% SNPs')
axs[0,0].set_ylabel('% Reads Aligned')

for i in range(MAX_STRAT+1):
    lab = STRAT_DESC[i]
    axs[0,1].plot(pct, correct[i], label=lab, linewidth=width, color=COLORS[i])
    axs[0,1].plot(pct[opt[i]], correct[i][opt[i]], color=COLORS[i], marker='D', ms=10)
axs[0,1].set_xlabel('% SNPs')
axs[0,1].set_ylabel('% Correct of Aligned')

for i in range(MAX_STRAT+1):
    lab = STRAT_DESC[i]
    axs[1,0].plot(pct, accuracy[i], label=lab, linewidth=width, color=COLORS[i])
    axs[1,0].plot(pct[opt[i]], accuracy[i][opt[i]], color=COLORS[i], marker='D', ms=10)
axs[1,0].set_xlabel('% SNPs')
axs[1,0].set_ylabel('% Correct Overall')

for i in range(MAX_STRAT+1):
    lab = STRAT_DESC[i]
    axs[1,1].plot(incorrect[i], accuracy[i], label=lab, linewidth=width, color=COLORS[i])
    axs[1,1].plot(incorrect[i][opt[i]], accuracy[i][opt[i]], color=COLORS[i], marker='D', ms=10)

    dy = (accuracy[i][-1] - accuracy[i][-2]) / (ylim[1]-ylim[0])
    dx = (incorrect[i][-1] - incorrect[i][-2]) / (xlim[1]-xlim[0])
    axs[1,1].plot(incorrect[i][-1], accuracy[i][-1], color=COLORS[i], marker=(3, 1, -90+math.degrees(math.atan2(dy,dx))), ms=18)

    dy = (accuracy[i][1] - accuracy[i][0]) / (ylim[1]-ylim[0])
    dx = (incorrect[i][1] - incorrect[i][0]) / (xlim[1]-xlim[0])
    axs[1,1].plot(incorrect[i][0], accuracy[i][0], color=COLORS[i], marker='o', ms=12)

#plt.legend(bbox_to_anchor=(-1,-0.1), loc='upper left')
plt.legend(bbox_to_anchor=(1,2), loc='upper left')
#plt.suptitle('Reads Stratified by ' + STRAT_LABEL + ', SNPs Ranked by ' + RANK_DESC, fontsize=24)
axs[1,1].set_xlabel('Incorrect')
axs[1,1].set_ylabel('Correct')
plt.savefig(STRAT_PREFIX+'_'+RANK_NAME+'.png', bbox_inches='tight')
plt.clf()

