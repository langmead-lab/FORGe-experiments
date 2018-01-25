#! /usr/bin/env python

'''
Plot chromosome-specific accuracy results
'''

import matplotlib.pyplot as plt
import math

chrom = '9'

font = {'size': 18}
plt.rc('font', **font)

PLOT_POP_COV = True
PLOT_AMB = True
PLOT_BLOWUP = False
PLOT_POP_COV_COMBINED = True
PLOT_AMB_COMBINED = True
PLOT_POP_COV_PC = False
PLOT_AMB_PC = False
PLOT_VARGAS = False

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

length = '25'

if PLOT_POP_COV:
    popcov = read_tsv('../results/chr9_all_bowtie_popcov_l'+length+'.tsv')
    pct_pc, aligned_pc, correct_pc, accuracy_pc, incorrect_pc, opt_pc = results_from_dict(popcov)

if PLOT_POP_COV_COMBINED:
    popcov_blowup = read_tsv('../results/chr9_all_bowtie_popcov_blowup_l'+length+'.tsv')
    pct_pcb, aligned_pcb, correct_pcb, accuracy_pcb, incorrect_pcb, opt_pcb = results_from_dict(popcov_blowup)

if PLOT_AMB:
    amb = read_tsv('../results/chr9_all_bowtie_amb_l'+length+'.tsv')
    pct_amb, aligned_amb, correct_amb, accuracy_amb, incorrect_amb, opt_amb = results_from_dict(amb)
#print(aligned_amb)

if PLOT_AMB_COMBINED:
    amb_blowup = read_tsv('../results/chr9_all_bowtie_amb_blowup_l'+length+'.tsv')
    pct_amb_combined, aligned_amb_combined, correct_amb_combined, accuracy_amb_combined, incorrect_amb_combined, opt_amb_combined = results_from_dict(amb_blowup)


#########################

'''
if PLOT_POP_COV:
    plt.plot(pct_pc, accuracy_pc, color='blue', label='Pop Cov', linewidth=2)
    #plt.plot(pct_pc[opt_pc], accuracy_pc[opt_pc], color='blue', marker='D', ms=10)
if PLOT_AMB:
    plt.plot(pct_amb, accuracy_amb, color='red', label='Hybrid', linewidth=2)
    #plt.plot(pct_amb[opt_amb], accuracy_amb[opt_amb], color='red', marker='D', ms=10)
plt.xlabel('% SNPs')
plt.ylabel('% Correct')

plt.legend(loc=4)
plt.xlabel('% SNPs')
plt.ylabel('% Correct')
plt.savefig('chr' + chrom + '_hisat_accuracy.png', bbox_inches='tight')
plt.clf()
exit()
'''

width = 3

f, axs = plt.subplots(2, 2, figsize=(20,20))
if PLOT_POP_COV:
    axs[0,0].plot(pct_pc, aligned_pc, color='blue', label='Pop Cov', linewidth=width)
    axs[0,0].plot(pct_pc[opt_pc], aligned_pc[opt_pc], color='blue', marker='D', ms=10)
if PLOT_AMB:
    axs[0,0].plot(pct_amb, aligned_amb, color='red', label='Hybrid', linewidth=width)
    axs[0,0].plot(pct_amb[opt_amb], aligned_amb[opt_amb], color='red', marker='D', ms=10)
if PLOT_POP_COV_COMBINED:
    axs[0,0].plot(pct_pcb, aligned_pcb, color='blue', linestyle='--', label='Combined (Pop Cov + Blowup)', linewidth=width)
    axs[0,0].plot(pct_pcb[opt_pcb], aligned_pcb[opt_pcb], color='blue', marker='D', ms=10)
if PLOT_AMB_COMBINED:
    axs[0,0].plot(pct_amb_combined, aligned_amb_combined, color='red', linestyle='--', label='Combined (Hybrid + Blowup)', linewidth=width)
    axs[0,0].plot(pct_amb_combined[opt_amb_combined], aligned_amb_combined[opt_amb_combined], color='red', marker='D', ms=10)
axs[0,0].set_xlabel('% SNPs')
axs[0,0].set_ylabel('% Reads Aligned')
axs[0,0].get_yaxis().get_major_formatter().set_useOffset(False)

if PLOT_POP_COV:
    axs[0,1].plot(pct_pc, correct_pc, color='blue', label='Pop Cov', linewidth=width)
    axs[0,1].plot(pct_pc[opt_pc], correct_pc[opt_pc], color='blue', marker='D', ms=10)
if PLOT_AMB:
    axs[0,1].plot(pct_amb, correct_amb, color='red', label='Hybrid', linewidth=width)
    axs[0,1].plot(pct_amb[opt_amb], correct_amb[opt_amb], color='red', marker='D', ms=10)
if PLOT_POP_COV_COMBINED:
    axs[0,1].plot(pct_pcb, correct_pcb, color='blue', linestyle='--', label='Combined (Pop Cov + Blowup)', linewidth=width)
    axs[0,1].plot(pct_pcb[opt_pcb], correct_pcb[opt_pcb], color='blue', marker='D', ms=10)
if PLOT_AMB_COMBINED:
    axs[0,1].plot(pct_amb_combined, correct_amb_combined, color='red', linestyle='--', label='Combined (Hybrid + Blowup)', linewidth=width)
    axs[0,1].plot(pct_amb_combined[opt_amb_combined], correct_amb_combined[opt_amb_combined], color='red', marker='D', ms=10)
axs[0,1].set_xlabel('% SNPs')
axs[0,1].set_ylabel('% Correct of Aligned')

axs[0,1].get_yaxis().get_major_formatter().set_useOffset(False)


if PLOT_POP_COV:
    axs[1,0].plot(pct_pc, accuracy_pc, color='blue', label='Pop Cov', linewidth=width)
    axs[1,0].plot(pct_pc[opt_pc], accuracy_pc[opt_pc], color='blue', marker='D', ms=10)
if PLOT_AMB:
    axs[1,0].plot(pct_amb, accuracy_amb, color='red', label='Hybrid', linewidth=width)
    axs[1,0].plot(pct_amb[opt_amb], accuracy_amb[opt_amb], color='red', marker='D', ms=10)
if PLOT_POP_COV_COMBINED:
    axs[1,0].plot(pct_pcb, accuracy_pcb, color='blue', linestyle='--', label='Combined (Pop Cov + Blowup)', linewidth=width)
    axs[1,0].plot(pct_pcb[opt_pcb], accuracy_pcb[opt_pcb], color='blue', marker='D', ms=10)
if PLOT_AMB_COMBINED:
    axs[1,0].plot(pct_amb_combined, accuracy_amb_combined, color='red', linestyle='--', label='Combined (Hybrid + Blowup)', linewidth=width)
    axs[1,0].plot(pct_amb_combined[opt_amb_combined], accuracy_amb_combined[opt_amb_combined], color='red', marker='D', ms=10)
axs[1,0].set_xlabel('% SNPs')
axs[1,0].set_ylabel('% Correct Overall')
axs[1,0].get_yaxis().get_major_formatter().set_useOffset(False)

# Print optimum SNP percentages
#print(pct_pc[opt_pc])
#print(pct_pcb[opt_pcb])
#print(pct_amb[opt_amb])
#print(pct_amb_combined[opt_amb_combined])

xlim = [15.4, 16.6]
ylim = [77.4, 78.4]
if PLOT_POP_COV:
    axs[1,1].plot(incorrect_pc, accuracy_pc, color='blue', label='Pop Cov', linewidth=width)
    axs[1,1].plot(incorrect_pc[opt_pc], accuracy_pc[opt_pc], color='blue', marker='D', ms=10)

    dy = (accuracy_pc[-1] - accuracy_pc[-2]) / (ylim[1]-ylim[0])
    dx = (incorrect_pc[-1] - incorrect_pc[-2]) / (xlim[1]-xlim[0])
    axs[1,1].plot(incorrect_pc[-1], accuracy_pc[-1], color='blue', marker=(3, 1, -90+math.degrees(math.atan2(dy,dx))), ms=18)

    dy = (accuracy_pc[1] - accuracy_pc[0]) / (ylim[1]-ylim[0])
    dx = (incorrect_pc[1] - incorrect_pc[0]) / (xlim[1]-xlim[0])
    axs[1,1].plot(incorrect_pc[0], accuracy_pc[0], color='blue', marker='o', ms=12)

if PLOT_AMB:
    axs[1,1].plot(incorrect_amb, accuracy_amb, color='red', label='Hybrid', linewidth=width)
    axs[1,1].plot(incorrect_amb[opt_amb], accuracy_amb[opt_amb], color='red', marker='D', ms=10)

    dy = (accuracy_amb[-1] - accuracy_amb[-2]) / (ylim[1]-ylim[0])
    dx = (incorrect_amb[-1] - incorrect_amb[-2]) / (xlim[1]-xlim[0])
    axs[1,1].plot(incorrect_amb[-1], accuracy_amb[-1], color='red', marker=(3, 1, -90+math.degrees(math.atan2(dy,dx))), ms=18)

    dy = (accuracy_amb[1] - accuracy_amb[0]) / (ylim[1]-ylim[0])
    dx = (incorrect_amb[1] - incorrect_amb[0]) / (xlim[1]-xlim[0])
    axs[1,1].plot(incorrect_amb[0], accuracy_amb[0], color='red', marker='o', ms=10)

if PLOT_POP_COV_COMBINED:
    axs[1,1].plot(incorrect_pcb, accuracy_pcb, color='blue', linestyle='--', label='Pop Cov + Blowup', linewidth=width)
    axs[1,1].plot(incorrect_pcb[opt_pcb], accuracy_pcb[opt_pcb], color='blue', marker='D', ms=10)

if PLOT_AMB_COMBINED:
    axs[1,1].plot(incorrect_amb_combined, accuracy_amb_combined, color='red', linestyle='--', label='Hybrid + Blowup', linewidth=width)
    axs[1,1].plot(incorrect_amb_combined[opt_amb_combined], accuracy_amb_combined[opt_amb_combined], color='red', marker='D', ms=10)

#axs[1,1].plot([5.116], [78.994], marker='o', label='Outgroup SNPs')
#axs[1,1].plot([5.354], [78.576], marker='o', label='SNPs in all outgroup')
#plt.legend(bbox_to_anchor=(-1,-0.1), loc='upper left')
plt.legend(bbox_to_anchor=(1,2), loc='upper left')
axs[1,1].set_xlabel('% Incorrect')
axs[1,1].set_ylabel('% Correct')
axs[1,1].get_yaxis().get_major_formatter().set_useOffset(False)
axs[1,1].get_xaxis().get_major_formatter().set_useOffset(False)
plt.savefig('chr' + chrom + '_erg.png', bbox_inches='tight')
plt.clf()


