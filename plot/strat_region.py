#! /usr/bin/env python

'''
Plot chromosome-specific accuracy results
'''

import matplotlib.pyplot as plt
import sys

names = ['popcov', 'popcov_blowup', 'amb100_max15', 'amb_blowup100_max15']
descs = ['Pop Cov', 'Pop Cov + Blowup', 'Hybrid', 'Hybrid + Blowup']

strat_names = ['Total', 'Exome', 'NonConf', 'Rep', 'Alu']

strat_map = dict()
strat_map['Total'] = 'All'
strat_map['Exome'] = 'Exome'
strat_map['NonConf'] = 'Non-Confident'
strat_map['Rep'] = 'Repetitive'
strat_map['Alu'] = 'Alu'


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
            strat = val(row, 'Region', header)
            num = int(val(row, 'Total', header))

            if strat in results:
                if pct in results[strat]:
                    prev = results[strat][pct]
                    results[strat][pct] = (prev[0]+aligned*num, prev[1]+correct*num, prev[2]+overall*num, prev[3]+num)
                else:
                    results[strat][pct] = (aligned*num, correct*num, overall*num, num)
                    
            else:
                results[strat] = dict()
                results[strat][pct] = (aligned*num, correct*num, overall*num, num)

    #for strat in results.keys():
    for strat in strat_names:
        for pct in results[strat].keys():
            count = results[strat][pct][3]
            results[strat][pct] = (results[strat][pct][0]/count, results[strat][pct][1]/count, results[strat][pct][2]/count)

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

    name, pct, aligned, correct, overall, incorrect, opt = [], [], [], [], [], [], []
    #for strat in results.keys():
    for strat in strat_names:
        name.append(strat)
        curr_pct = sorted(results[strat].keys())
        pct.append(curr_pct)

        aligned.append([100*results[strat][p][0] for p in curr_pct])
        correct.append([100*results[strat][p][1] for p in curr_pct])
        overall.append([100*results[strat][p][2] for p in curr_pct])
        incorrect.append([aligned[-1][p] * (100-correct[-1][p]) / 100 for p in range(len(curr_pct))])
        opt.append(findOptPoint(correct[-1], incorrect[-1]))

    return name, pct, aligned, correct, overall, incorrect, opt


#########################


#########################

width = 3

f, axs = plt.subplots(2, 4, figsize=(12,10))

al_range = [94, 98]
cor_range = [75,96]

for i in range(len(names)):
    results = read_tsv('../results/chr' + chrom + '_all_' + names[i] + '.strat_region.tsv')
    #results = read_tsv('../results/accuracy_' + RANK_NAME + '_hg19conf.' + STRAT_PREFIX + '.tsv')
    strat, pct, aligned, correct, accuracy, incorrect, opt = results_from_dict(results)

    for j in range(len(strat)):
        if strat_map[strat[j]] == 'All':
            axs[0,i].plot(pct[j], aligned[j], label=strat_map[strat[j]], color='black', linestyle='--', linewidth=width)
        else:
            axs[0,i].plot(pct[j], aligned[j], label=strat_map[strat[j]], linewidth=width)
        axs[0,i].set_ylim(al_range)
        axs[0,i].get_xaxis().set_ticklabels([])
        axs[0,i].set_title(descs[i]+'\n')

        if strat_map[strat[j]] == 'All':
            axs[1,i].plot(pct[j], correct[j], label=strat_map[strat[j]], color='black', linestyle='--', linewidth=width)
        else:
            axs[1,i].plot(pct[j], correct[j], label=strat_map[strat[j]], linewidth=width)
        axs[1,i].get_xaxis().set_ticklabels([0,'','','','',100])
        axs[1,i].set_ylim(cor_range)

        if i > 0:
            axs[0,i].get_yaxis().set_ticklabels([])
            axs[1,i].get_yaxis().set_ticklabels([])

    axs[1,i].set_xlabel('% SNPs')

axs[0,0].set_ylabel('% Reads Aligned')
axs[1,0].set_ylabel('% Correct of Aligned')

plt.legend(bbox_to_anchor=(-2,-0.2), loc='upper left')
#plt.legend(bbox_to_anchor=(1,2), loc='upper left')

plt.savefig('strat_region.png', bbox_inches='tight')
plt.clf()

