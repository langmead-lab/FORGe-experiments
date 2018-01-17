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
PLOT_POP_COV_COMBINED = False
PLOT_AMB_COMBINED = False

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
            mem = 0#float(val(row, 'AlignMem', header))

            if pct in results:
                prev = results[pct]
                results[pct] = (prev[0]+aligned, prev[1]+correct, prev[2]+overall, prev[3]+mem, prev[4]+1)
            else:
                results[pct] = (aligned, correct, overall, mem, 1)

    for pct, res in results.items():
        count = res[4]
        results[pct] = (res[0]/count, res[1]/count, res[2]/count, res[3]/count)

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

def results_from_dict(results, total):
    pct = sorted(results.keys())
    aligned = [results[p][0] for p in pct]
    correct = [results[p][1] for p in pct]
    overall = [results[p][2] for p in pct]
    incorrect = [aligned[p] * (100-correct[p]) / 100 for p in range(len(pct))]
    mem = [results[p][3] for p in pct]
    num_vars = [total*p/100000. for p in pct]
    opt = findOptPoint(correct, incorrect)

    return pct, aligned, correct, overall, incorrect, mem, num_vars, opt


#########################

total_all = 3415974
total_ceu = 545317

if PLOT_POP_COV:
    popcov = read_tsv('../results/chr' + chrom + '_all_popcov_l100.tsv')
    pct_pc, aligned_pc, correct_pc, accuracy_pc, incorrect_pc, mem_pc, count_pc, opt_pc = results_from_dict(popcov, total_all)

    popcov_ceu = read_tsv('../results/ceu/chr' + chrom + '_ceu_popcov_l100.tsv')
    pct_pc_ceu, aligned_pc_ceu, correct_pc_ceu, accuracy_pc_ceu, incorrect_pc_ceu, mem_pc_ceu, count_pc_ceu, opt_pc_ceu = results_from_dict(popcov_ceu, total_ceu)

if PLOT_AMB:
    #amb = read_tsv('../results/chr' + chrom + '_all_amb_l100.tsv')
    amb = read_tsv('../results/chr9_all_amb100_max15.tsv')
    pct_amb, aligned_amb, correct_amb, accuracy_amb, incorrect_amb, mem_amb, count_amb, opt_amb = results_from_dict(amb, total_all)

    amb_ceu = read_tsv('../results/ceu/chr' + chrom + '_ceu_amb100_l100.tsv')
    pct_amb_ceu, aligned_amb_ceu, correct_amb_ceu, accuracy_amb_ceu, incorrect_amb_ceu, mem_amb_ceu, count_amb_ceu, opt_amb_ceu = results_from_dict(amb_ceu, total_ceu)



#########################

width = 3

plt.figure(figsize=(10,10))

'''
if PLOT_POP_COV:
    plt.plot(count_pc, accuracy_pc, color='blue', label='All, Pop Cov', linewidth=width)
    plt.plot(count_pc[opt_pc], accuracy_pc[opt_pc], color='blue', marker='D', ms=10)
    plt.plot(count_pc_ceu, accuracy_pc_ceu, color='blue', linestyle='--', label='CEU, Pop Cov', linewidth=width)
    plt.plot(count_pc_ceu[opt_pc_ceu], accuracy_pc_ceu[opt_pc_ceu], color='blue', marker='D', ms=10)
if PLOT_AMB:
    plt.plot(count_amb, accuracy_amb, color='red', label='All, Hybrid', linewidth=width)
    plt.plot(count_amb[opt_amb], accuracy_amb[opt_amb], color='red', marker='D', ms=10)
    plt.plot(count_amb_ceu, accuracy_amb_ceu, color='red', linestyle='--', label='CEU, Hybrid', linewidth=width)
    plt.plot(count_amb_ceu[opt_amb_ceu], accuracy_amb_ceu[opt_amb_ceu], color='red', marker='D', ms=10)
if PLOT_POP_COV_COMBINED:
    plt.plot(count_pcb, accuracy_pcb, color='blue', linestyle='--', label='All, Pop Cov + Blowup', linewidth=width)
    plt.plot(count_pcb[opt_pcb], accuracy_pcb[opt_pcb], color='blue', marker='D', ms=10)
    plt.plot(count_pcb_ceu, accuracy_pcb_ceu, color='red', linestyle='--', label='CEU, Pop Cov + Blowup', linewidth=width)
    plt.plot(count_pcb_ceu[opt_pcb_ceu], accuracy_pcb_ceu[opt_pcb_ceu], color='red', marker='D', ms=10)
if PLOT_AMB_COMBINED:
    plt.plot(count_amb_combined, accuracy_amb_combined, color='red', linestyle='--', label='All, Hybrid + Blowup', linewidth=width)
    plt.plot(count_amb_combined[opt_amb_combined], accuracy_amb_combined[opt_amb_combined], color='red', marker='D', ms=10)
    plt.plot(count_amb_combined_ceu, accuracy_amb_combined_ceu, color='red', linestyle='--', label='CEU, Hybrid + Blowup', linewidth=width)
    plt.plot(count_amb_combined_ceu[opt_amb_combined_ceu], accuracy_amb_combined_ceu[opt_amb_combined_ceu], color='red', marker='D', ms=10)
plt.xlim([0,600])
plt.xlabel('Thousands of SNPs')
plt.ylabel('% Correct Overall')
plt.legend(loc=4)
plt.savefig('all_vs_ceu_accuracy.png', bbox_inches='tight')
plt.clf()
exit()
'''

f, axs = plt.subplots(2, 2, figsize=(20,20))
if PLOT_POP_COV:
    axs[0,0].plot(count_pc, aligned_pc, color='blue', label='All, Pop Cov', linewidth=width)
    axs[0,0].plot(count_pc[opt_pc], aligned_pc[opt_pc], color='blue', marker='D', ms=10)
    axs[0,0].plot(count_pc_ceu, aligned_pc_ceu, color='blue', linestyle='--', label='CEU, Pop Cov', linewidth=width)
    axs[0,0].plot(count_pc_ceu[opt_pc_ceu], aligned_pc_ceu[opt_pc_ceu], color='blue', marker='D', ms=10)
if PLOT_AMB:
    axs[0,0].plot(count_amb, aligned_amb, color='red', label='All, Hybrid', linewidth=width)
    axs[0,0].plot(count_amb[opt_amb], aligned_amb[opt_amb], color='red', marker='D', ms=10)
    axs[0,0].plot(count_amb_ceu, aligned_amb_ceu, color='red', linestyle='--', label='CEU, Hybrid', linewidth=width)
    axs[0,0].plot(count_amb_ceu[opt_amb_ceu], aligned_amb_ceu[opt_amb_ceu], color='red', marker='D', ms=10)
if PLOT_POP_COV_COMBINED:
    axs[0,0].plot(count_pcb, aligned_pcb, color='blue', linestyle='--', label='All, Pop Cov + Blowup', linewidth=width)
    axs[0,0].plot(count_pcb[opt_pcb], aligned_pcb[opt_pcb], color='blue', marker='D', ms=10)
    axs[0,0].plot(count_pcb_ceu, aligned_pcb_ceu, color='red', linestyle='--', label='CEU, Pop Cov + Blowup', linewidth=width)
    axs[0,0].plot(count_pcb_ceu[opt_pcb_ceu], aligned_pcb_ceu[opt_pcb_ceu], color='red', marker='D', ms=10)
if PLOT_AMB_COMBINED:
    axs[0,0].plot(count_amb_combined, aligned_amb_combined, color='red', linestyle='--', label='All, Hybrid + Blowup', linewidth=width)
    axs[0,0].plot(count_amb_combined[opt_amb_combined], aligned_amb_combined[opt_amb_combined], color='red', marker='D', ms=10)
    axs[0,0].plot(count_amb_combined_ceu, aligned_amb_combined_ceu, color='red', linestyle='--', label='CEU, Hybrid + Blowup', linewidth=width)
    axs[0,0].plot(count_amb_combined_ceu[opt_amb_combined_ceu], aligned_amb_combined_ceu[opt_amb_combined_ceu], color='red', marker='D', ms=10)
axs[0,0].set_xlim([0,600])
axs[0,0].set_xlabel('Thousands of SNPs')
axs[0,0].set_ylabel('% Reads Aligned')

if PLOT_POP_COV:
    axs[0,1].plot(count_pc, correct_pc, color='blue', label='All, Pop Cov', linewidth=width)
    axs[0,1].plot(count_pc[opt_pc], correct_pc[opt_pc], color='blue', marker='D', ms=10)
    axs[0,1].plot(count_pc_ceu, correct_pc_ceu, color='blue', linestyle='--', label='CEU, Pop Cov', linewidth=width)
    axs[0,1].plot(count_pc_ceu[opt_pc_ceu], correct_pc_ceu[opt_pc_ceu], color='blue', marker='D', ms=10)
if PLOT_AMB:
    axs[0,1].plot(count_amb, correct_amb, color='red', label='All, Hybrid', linewidth=width)
    axs[0,1].plot(count_amb[opt_amb], correct_amb[opt_amb], color='red', marker='D', ms=10)
    axs[0,1].plot(count_amb_ceu, correct_amb_ceu, color='red', linestyle='--', label='CEU, Hybrid', linewidth=width)
    axs[0,1].plot(count_amb_ceu[opt_amb_ceu], correct_amb_ceu[opt_amb_ceu], color='red', marker='D', ms=10)
if PLOT_POP_COV_COMBINED:
    axs[0,1].plot(count_pcb, correct_pcb, color='blue', linestyle='--', label='All, Pop Cov + Blowup', linewidth=width)
    axs[0,1].plot(count_pcb[opt_pcb], correct_pcb[opt_pcb], color='blue', marker='D', ms=10)
    axs[0,1].plot(count_pcb_ceu, correct_pcb_ceu, color='red', linestyle='--', label='CEU, Pop Cov + Blowup', linewidth=width)
    axs[0,1].plot(count_pcb_ceu[opt_pcb_ceu], correct_pcb_ceu[opt_pcb_ceu], color='red', marker='D', ms=10)
if PLOT_AMB_COMBINED:
    axs[0,1].plot(count_amb_combined, correct_amb_combined, color='red', linestyle='--', label='All, Hybrid + Blowup', linewidth=width)
    axs[0,1].plot(count_amb_combined[opt_amb_combined], correct_amb_combined[opt_amb_combined], color='red', marker='D', ms=10)
    axs[0,1].plot(count_amb_combined_ceu, correct_amb_combined_ceu, color='red', linestyle='--', label='CEU, Hybrid + Blowup', linewidth=width)
    axs[0,1].plot(count_amb_combined_ceu[opt_amb_combined_ceu], correct_amb_combined_ceu[opt_amb_combined_ceu], color='red', marker='D', ms=10)
axs[0,1].set_xlim([0,600])
axs[0,1].set_xlabel('Thousands of SNPs')
axs[0,1].set_ylabel('% Correct of Aligned')

axs[0,1].get_yaxis().get_major_formatter().set_useOffset(False)


if PLOT_POP_COV:
    axs[1,0].plot(count_pc, accuracy_pc, color='blue', label='All, Pop Cov', linewidth=width)
    axs[1,0].plot(count_pc[opt_pc], accuracy_pc[opt_pc], color='blue', marker='D', ms=10)
    axs[1,0].plot(count_pc_ceu, accuracy_pc_ceu, color='blue', linestyle='--', label='CEU, Pop Cov', linewidth=width)
    axs[1,0].plot(count_pc_ceu[opt_pc_ceu], accuracy_pc_ceu[opt_pc_ceu], color='blue', marker='D', ms=10)
if PLOT_AMB:
    axs[1,0].plot(count_amb, accuracy_amb, color='red', label='All, Hybrid', linewidth=width)
    axs[1,0].plot(count_amb[opt_amb], accuracy_amb[opt_amb], color='red', marker='D', ms=10)
    axs[1,0].plot(count_amb_ceu, accuracy_amb_ceu, color='red', linestyle='--', label='CEU, Hybrid', linewidth=width)
    axs[1,0].plot(count_amb_ceu[opt_amb_ceu], accuracy_amb_ceu[opt_amb_ceu], color='red', marker='D', ms=10)
if PLOT_POP_COV_COMBINED:
    axs[1,0].plot(count_pcb, accuracy_pcb, color='blue', linestyle='--', label='All, Pop Cov + Blowup', linewidth=width)
    axs[1,0].plot(count_pcb[opt_pcb], accuracy_pcb[opt_pcb], color='blue', marker='D', ms=10)
    axs[1,0].plot(count_pcb_ceu, accuracy_pcb_ceu, color='red', linestyle='--', label='CEU, Pop Cov + Blowup', linewidth=width)
    axs[1,0].plot(count_pcb_ceu[opt_pcb_ceu], accuracy_pcb_ceu[opt_pcb_ceu], color='red', marker='D', ms=10)
if PLOT_AMB_COMBINED:
    axs[1,0].plot(count_amb_combined, accuracy_amb_combined, color='red', linestyle='--', label='All, Hybrid + Blowup', linewidth=width)
    axs[1,0].plot(count_amb_combined[opt_amb_combined], accuracy_amb_combined[opt_amb_combined], color='red', marker='D', ms=10)
    axs[1,0].plot(count_amb_combined_ceu, accuracy_amb_combined_ceu, color='red', linestyle='--', label='CEU, Hybrid + Blowup', linewidth=width)
    axs[1,0].plot(count_amb_combined_ceu[opt_amb_combined_ceu], accuracy_amb_combined_ceu[opt_amb_combined_ceu], color='red', marker='D', ms=10)
axs[1,0].set_xlim([0,600])
axs[1,0].set_xlabel('Thousands of SNPs')
axs[1,0].set_ylabel('% Correct Overall')

if PLOT_POP_COV:
    axs[1,1].plot(incorrect_pc, accuracy_pc, color='blue', label='All, Pop Cov', linewidth=width)
    axs[1,1].plot(incorrect_pc[opt_pc], accuracy_pc[opt_pc], color='blue', marker='D', ms=10)
    axs[1,1].plot(incorrect_pc_ceu, accuracy_pc_ceu, color='blue', linestyle='--', label='CEU, Pop Cov', linewidth=width)
    axs[1,1].plot(incorrect_pc_ceu[opt_pc_ceu], accuracy_pc_ceu[opt_pc_ceu], color='blue', marker='D', ms=10)
if PLOT_AMB:
    axs[1,1].plot(incorrect_amb, accuracy_amb, color='red', label='All, Hybrid', linewidth=width)
    axs[1,1].plot(incorrect_amb[opt_amb], accuracy_amb[opt_amb], color='red', marker='D', ms=10)
    axs[1,1].plot(incorrect_amb_ceu, accuracy_amb_ceu, color='red', linestyle='--', label='CEU, Hybrid', linewidth=width)
    axs[1,1].plot(incorrect_amb_ceu[opt_amb_ceu], accuracy_amb_ceu[opt_amb_ceu], color='red', marker='D', ms=10)
if PLOT_POP_COV_COMBINED:
    axs[1,1].plot(incorrect_pcb, accuracy_pcb, color='blue', linestyle='--', label='All, Pop Cov + Blowup', linewidth=width)
    axs[1,1].plot(incorrect_pcb[opt_pcb], accuracy_pcb[opt_pcb], color='blue', marker='D', ms=10)
    axs[1,1].plot(incorrect_pcb_ceu, accuracy_pcb_ceu, color='red', linestyle='--', label='All, Pop Cov + Blowup', linewidth=width)
    axs[1,1].plot(incorrect_pcb_ceu[opt_pcb_ceu], accuracy_pcb_ceu[opt_pcb_ceu], color='red', marker='D', ms=10)
if PLOT_AMB_COMBINED:
    axs[1,1].plot(incorrect_amb_combined, accuracy_amb_combined, color='red', linestyle='--', label='All, Hybrid + Blowup', linewidth=width)
    axs[1,1].plot(incorrect_amb_combined[opt_amb_combined], accuracy_amb_combined[opt_amb_combined], color='red', marker='D', ms=10)
    axs[1,1].plot(incorrect_amb_combined_ceu, accuracy_amb_combined_ceu, color='red', linestyle='--', label='All, Hybrid + Blowup', linewidth=width)
    axs[1,1].plot(incorrect_amb_combined_ceu[opt_amb_combined_ceu], accuracy_amb_combined_ceu[opt_amb_combined_ceu], color='red', marker='D', ms=10)

# Add arrowheads
xlim = [5.36, 5.48]
ylim = [91.1, 91.7]
if PLOT_POP_COV:
    dy = (accuracy_pc[-1] - accuracy_pc[-2]) / (ylim[1]-ylim[0])
    dx = (incorrect_pc[-1] - incorrect_pc[-2]) / (xlim[1]-xlim[0])
    axs[1,1].plot(incorrect_pc[-1], accuracy_pc[-1], color='blue', marker=(3, 1, -90+math.degrees(math.atan2(dy,dx))), ms=18)
    axs[1,1].plot(incorrect_pc[0], accuracy_pc[0], color='blue', marker='o', ms=12)
if PLOT_AMB:
    dy = (accuracy_amb[-1] - accuracy_amb[-2]) / (ylim[1]-ylim[0])
    dx = (incorrect_amb[-1] - incorrect_amb[-2]) / (xlim[1]-xlim[0])
    axs[1,1].plot(incorrect_amb[-1], accuracy_amb[-1], color='red', marker=(3, 1, -90+math.degrees(math.atan2(dy,dx))), ms=18)
    axs[1,1].plot(incorrect_amb[0], accuracy_amb[0], color='red', marker='o', ms=12)

#plt.legend(bbox_to_anchor=(-1,-0.1), loc='upper left')
plt.legend(bbox_to_anchor=(1,2), loc='upper left')
axs[1,1].set_xlabel('% Incorrect')
axs[1,1].set_ylabel('% Correct')
plt.savefig('all_vs_ceu.png', bbox_inches='tight')
plt.clf()


