#! /usr/bin/env python

'''
Plot chromosome-specific accuracy results
'''

import matplotlib.pyplot as plt
import sys

#####
STRAT_MODE = int(sys.argv[1])

if STRAT_MODE == 0:
    STRAT_PREFIX = 'strat_snp'
    STRAT_LABEL = 'SNPs'
    STRAT_DESC = 'SNPs'
    MAX_STRAT = 3
elif STRAT_MODE == 1:
    STRAT_PREFIX = 'strat_del'
    STRAT_LABEL = 'DelSNPs'
    STRAT_DESC = 'Deleterious SNPs'
    MAX_STRAT = 1
elif STRAT_MODE == 2:
    STRAT_PREFIX = 'strat_rare'
    STRAT_LABEL = 'RareSNPs'
    STRAT_DESC = 'Rare SNPs'
    MAX_STRAT = 1
######
RANK_MODE = int(sys.argv[2])

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
        aligned.append([results[p][i][0] for p in pct])
        correct.append([results[p][i][1] for p in pct])
        overall.append([results[p][i][2] for p in pct])
        incorrect.append([aligned[i][p] * (100-correct[i][p]) / 100 for p in range(len(pct))])
        opt.append(findOptPoint(correct[i], incorrect[i]))

    return pct, aligned, correct, overall, incorrect, opt


#########################

results = read_tsv('../results/chr' + chrom + '_all_' + RANK_NAME + '.' + STRAT_PREFIX + '.tsv')
#results = read_tsv('../results/accuracy_' + RANK_NAME + '_hg19conf.' + STRAT_PREFIX + '.tsv')
pct, aligned, correct, accuracy, incorrect, opt = results_from_dict(results)


#########################

width = 3

plt.figure(figsize=(10,10))

for i in range(MAX_STRAT+1):
    plt.plot(pct, accuracy[i], label=str(i)+' '+STRAT_DESC, linewidth=width)
plt.xlabel('% SNPs')
plt.ylabel('% Correct Overall')
plt.legend(loc=4)
plt.ylim([0.9,0.98])
plt.savefig('chr' + chrom + '_hisat_' + RANK_NAME + '_accuracy.'+STRAT_PREFIX+'.png', bbox_inches='tight')
plt.clf()
exit()

f, axs = plt.subplots(2, 2, figsize=(20,20))
for i in range(MAX_STRAT+1):
    axs[0,0].plot(pct, aligned[i], label=str(i)+' '+STRAT_DESC, linewidth=width)
axs[0,0].set_xlabel('% SNPs')
axs[0,0].set_ylabel('% Reads Aligned')

for i in range(MAX_STRAT+1):
    axs[0,1].plot(pct, correct[i], label=str(i)+' '+STRAT_DESC, linewidth=width)
axs[0,1].set_xlabel('% SNPs')
axs[0,1].set_ylabel('% Correct of Aligned')

for i in range(MAX_STRAT+1):
    axs[1,0].plot(pct, accuracy[i], label=str(i)+' '+STRAT_DESC, linewidth=width)
axs[1,0].set_xlabel('% SNPs')
axs[1,0].set_ylabel('% Correct Overall')

for i in range(MAX_STRAT+1):
    axs[1,1].plot(incorrect[i], correct[i], label=str(i)+' '+STRAT_DESC, linewidth=width)

#plt.legend(bbox_to_anchor=(-1,-0.1), loc='upper left')
plt.legend(bbox_to_anchor=(1,2), loc='upper left')
#plt.suptitle('Reads Stratified by ' + STRAT_LABEL + ', SNPs Ranked by ' + RANK_DESC, fontsize=24)
axs[1,1].set_xlabel('Incorrect')
axs[1,1].set_ylabel('Correct')
plt.savefig('chr' + chrom + '_hisat_' + RANK_NAME + '.'+STRAT_PREFIX+'.png', bbox_inches='tight')
plt.clf()


