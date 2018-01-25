#! /usr/bin/env python

'''
Plot accuracy results for simulated reads from the full human genome
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
            pct = val(row, 'Pct', header)
            aligned = float(val(row, 'Aligned', header))
            correct = float(val(row, 'Correct', header))
            overall = float(val(row, 'Overall', header))

            if pct in results:
                prev = results[pct]
                results[pct] = (prev[0]+aligned, prev[1]+correct, prev[2]+overall, prev[3]+1)
            else:
                results[pct] = (aligned, correct, overall, 1)

    for pct, res in results.items():
        count = res[3]
        results[pct] = (res[0]/count, res[1]/count, res[2]/count)

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
    pct = sorted([int(p) for p in results.keys()])
    aligned = [results[str(p)][0] for p in pct]
    correct = [results[str(p)][1] for p in pct]
    overall = [results[str(p)][2] for p in pct]
    incorrect = [aligned[p] * (100-correct[p]) / 100 for p in range(len(pct))]
    opt = findOptPoint(correct, incorrect)

    return pct, aligned, correct, overall, incorrect, opt


#########################

snp_results = read_tsv('../results/full_genome/popcov_blowup_sim.tsv')
pct_snps, aligned_snps, correct_snps, accuracy_snps, incorrect_snps, opt_snps = results_from_dict(snp_results)

#########################

width = 3

f, axs = plt.subplots(2, 2, figsize=(20,20))
axs[0,0].plot(pct_snps, aligned_snps, color='blue', label='SNPs', linewidth=width)
axs[0,0].plot(pct_snps[opt_snps], aligned_snps[opt_snps], color='blue', marker='D', ms=10)
axs[0,0].set_xlabel('% SNPs')
axs[0,0].set_ylabel('% Reads Aligned')

axs[0,1].plot(pct_snps, correct_snps, color='blue', label='SNPs', linewidth=width)
axs[0,1].plot(pct_snps[opt_snps], correct_snps[opt_snps], color='blue', marker='D', ms=10)
axs[0,1].set_xlabel('% SNPs')
axs[0,1].set_ylabel('% Correct of Aligned')
axs[0,1].get_yaxis().get_major_formatter().set_useOffset(False)


axs[1,0].plot(pct_snps, accuracy_snps, color='blue', label='SNPs', linewidth=width)
axs[1,0].plot(pct_snps[opt_snps], accuracy_snps[opt_snps], color='blue', marker='D', ms=10)
axs[1,0].set_xlabel('% SNPs')
axs[1,0].set_ylabel('% Correct Overall')

xlim = [1.98, 2.06]
ylim = [91.1, 91.5]

axs[1,1].plot(incorrect_snps, accuracy_snps, color='blue', label='SNPs', linewidth=width)
axs[1,1].plot(incorrect_snps[opt_snps], accuracy_snps[opt_snps], color='blue', marker='D', ms=10)
dy = (accuracy_snps[-1] - accuracy_snps[-2]) / (ylim[1]-ylim[0])
dx = (incorrect_snps[-1] - incorrect_snps[-2]) / (xlim[1]-xlim[0])
axs[1,1].plot(incorrect_snps[-1], accuracy_snps[-1], color='blue', marker=(3, 1, -90+math.degrees(math.atan2(dy,dx))), ms=18)
axs[1,1].plot(incorrect_snps[0], accuracy_snps[0], color='blue', marker='o', ms=12)

#axs[1,1].plot([5.116], [78.994], marker='o', label='Outgroup SNPs')
#axs[1,1].plot([5.354], [78.576], marker='o', label='SNPs in all outgroup')
#plt.legend(bbox_to_anchor=(-1,-0.1), loc='upper left')
axs[1,1].set_xlabel('% Incorrect')
axs[1,1].set_ylabel('% Correct')
plt.savefig('full_popcov_blowup.png', bbox_inches='tight')
plt.clf()

# Print optimum SNP percentages
print(pct_snps[opt_snps])
#print(pct_vars[opt_vars])
