#! /usr/bin/env python

'''
Plot chromosome-specific accuracy results
'''

import matplotlib.pyplot as plt

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

            mem = 0
            if 'BuildMem' in header:
                mem = float(val(row, 'BuildMem', header)) / 1000 # Convert to GB

            if pct in results:
                prev = results[pct]
                results[pct] = (prev[0]+aligned, prev[1]+correct, prev[2]+overall, prev[3]+mem, prev[4]+1)
            else:
                results[pct] = (aligned, correct, overall, mem, 1)

    for pct, res in results.items():
        count = res[4]
        results[pct] = (res[0]/count, res[1]/count, res[2]/count, res[3]/count)

    return results

def read_mem(filename):
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
            num = int(val(row, 'Num', header))
            build_mem = float(val(row, 'BuildMem', header)) / 1000 # Convert to GB
            align_mem = float(val(row, 'AlignMem', header))

            results[pct] = build_mem
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

def results_from_dict(results, mem):
    pct = sorted([int(p) for p in results.keys()])
    aligned = [results[str(p)][0] for p in pct]
    correct = [results[str(p)][1] for p in pct]
    overall = [results[str(p)][2] for p in pct]
    incorrect = [aligned[p] * (100-correct[p]) / 100 for p in range(len(pct))]
    
    mem = [mem[str(p)] for p in pct]
    opt = findOptPoint(correct, incorrect)

    return pct, aligned, correct, overall, incorrect, mem, opt


#########################
hisat_auto = read_tsv('../results/chr' + chrom + '_all_hisat_auto.tsv')
aligned_auto, correct_auto, accuracy_auto, mem_auto = hisat_auto['Auto'][0], hisat_auto['Auto'][1], hisat_auto['Auto'][2], hisat_auto['Auto'][3]
incorrect_auto = aligned_auto * (100 - correct_auto) / 100

if PLOT_POP_COV:
    popcov = read_tsv('../results/chr' + chrom + '_all_popcov.tsv')
    popcov_mem = read_mem('../results/chr' + chrom + '_all_popcov_mem.tsv')
    pct_pc, aligned_pc, correct_pc, accuracy_pc, incorrect_pc, mem_pc, opt_pc = results_from_dict(popcov, popcov_mem)

if PLOT_POP_COV_COMBINED:
    popcov_blowup = read_tsv('../results/chr' + chrom + '_all_popcov_blowup.tsv')
    popcov_blowup_mem = read_mem('../results/chr' + chrom + '_all_popcov_blowup_mem.tsv')
    pct_pcb, aligned_pcb, correct_pcb, accuracy_pcb, incorrect_pcb, mem_pcb, opt_pcb = results_from_dict(popcov_blowup, popcov_blowup_mem)

if PLOT_AMB:
    amb = read_tsv('../results/chr' + chrom + '_all_amb.tsv')
    amb_mem = read_mem('../results/chr' + chrom + '_all_amb_mem.tsv')
    pct_amb, aligned_amb, correct_amb, accuracy_amb, incorrect_amb, mem_amb, opt_amb = results_from_dict(amb, amb_mem)

if PLOT_AMB_COMBINED:
    amb_blowup = read_tsv('../results/chr' + chrom + '_all_amb_blowup.tsv')
    amb_blowup_mem = read_mem('../results/chr' + chrom + '_all_amb_blowup_mem.tsv')
    pct_amb_combined, aligned_amb_combined, correct_amb_combined, accuracy_amb_combined, incorrect_amb_combined, mem_amb_combined, opt_amb_combined = results_from_dict(amb_blowup, amb_blowup_mem)

#########################

width = 3

plt.figure(figsize=(10,10))
if PLOT_POP_COV:
    plt.plot(pct_pc, mem_pc, color='blue', label='Pop Cov', linewidth=width)
if PLOT_AMB:
    plt.plot(pct_amb, mem_amb, color='red', label='Hybrid', linewidth=width)
if PLOT_POP_COV_COMBINED:
    plt.plot(pct_pcb, mem_pcb, color='blue', linestyle='--', label='Pop Cov + Blowup', linewidth=width)
if PLOT_AMB_COMBINED:
    plt.plot(pct_amb_combined, mem_amb_combined, color='red', linestyle='--', label='Hybrid + Blowup', linewidth=width)
plt.plot([0,100], [mem_auto, mem_auto], color='black', label='HISAT2 Auto-Prune', linewidth=2)

plt.legend(bbox_to_anchor=(1,1), loc='upper left')
plt.xlabel('% SNPs')
plt.ylabel('Alignment Mem (GB)')
plt.savefig('chr' + chrom + '_hisat_vs_mem.png', bbox_inches='tight')
plt.clf()
exit()

f, axs = plt.subplots(2, 2, figsize=(20,20))
if PLOT_POP_COV:
    axs[0,0].plot(mem_pc, aligned_pc, color='blue', label='Pop Cov', linewidth=2)
    axs[0,0].plot(mem_pc[opt_pc], aligned_pc[opt_pc], color='blue', marker='D', ms=10)
if PLOT_AMB:
    axs[0,0].plot(mem_amb, aligned_amb, color='red', label='Hybrid', linewidth=2)
    axs[0,0].plot(mem_amb[opt_amb], aligned_amb[opt_amb], color='red', marker='D', ms=10)
if PLOT_POP_COV_COMBINED:
    axs[0,0].plot(mem_pcb, aligned_pcb, color='blue', linestyle='--', label='Combined (Pop Cov + Blowup)', linewidth=2)
    axs[0,0].plot(mem_pcb[opt_pcb], aligned_pcb[opt_pcb], color='blue', marker='D', ms=10)
if PLOT_AMB_COMBINED:
    axs[0,0].plot(mem_amb_combined, aligned_amb_combined, color='red', linestyle='--', label='Combined (Hybrid + Blowup)', linewidth=2)
    axs[0,0].plot(mem_amb_combined[opt_amb_combined], aligned_amb_combined[opt_amb_combined], color='red', marker='D', ms=10)
axs[0,0].plot(mem_auto, aligned_auto, color='black', marker='D', ms=10)
axs[0,0].set_xlabel('Alignment Mem (GB)')
axs[0,0].set_ylabel('% Reads Aligned')

if PLOT_POP_COV:
    axs[0,1].plot(mem_pc, correct_pc, color='blue', label='Pop Cov', linewidth=2)
    axs[0,1].plot(mem_pc[opt_pc], correct_pc[opt_pc], color='blue', marker='D', ms=10)
if PLOT_AMB:
    axs[0,1].plot(mem_amb, correct_amb, color='red', label='Hybrid', linewidth=2)
    axs[0,1].plot(mem_amb[opt_amb], correct_amb[opt_amb], color='red', marker='D', ms=10)
if PLOT_POP_COV_COMBINED:
    axs[0,1].plot(mem_pcb, correct_pcb, color='blue', linestyle='--', label='Combined (Pop Cov + Blowup)', linewidth=2)
    axs[0,1].plot(mem_pcb[opt_pcb], correct_pcb[opt_pcb], color='blue', marker='D', ms=10)
if PLOT_AMB_COMBINED:
    axs[0,1].plot(mem_amb_combined, correct_amb_combined, color='red', linestyle='--', label='Combined (Hybrid + Blowup)', linewidth=2)
    axs[0,1].plot(mem_amb_combined[opt_amb_combined], correct_amb_combined[opt_amb_combined], color='red', marker='D', ms=10)
axs[0,1].plot(mem_auto, correct_auto, color='black', marker='D', ms=10)
axs[0,1].set_xlabel('Alignment Mem (GB)')
axs[0,1].set_ylabel('% Correct of Aligned')

if PLOT_POP_COV:
    axs[1,0].plot(mem_pc, accuracy_pc, color='blue', label='Pop Cov', linewidth=2)
    axs[1,0].plot(mem_pc[opt_pc], accuracy_pc[opt_pc], color='blue', marker='D', ms=10)
if PLOT_AMB:
    axs[1,0].plot(mem_amb, accuracy_amb, color='red', label='Hybrid', linewidth=2)
    axs[1,0].plot(mem_amb[opt_amb], accuracy_amb[opt_amb], color='red', marker='D', ms=10)
if PLOT_POP_COV_COMBINED:
    axs[1,0].plot(mem_pcb, accuracy_pcb, color='blue', linestyle='--', label='Combined (Pop Cov + Blowup)', linewidth=2)
    axs[1,0].plot(mem_pcb[opt_pcb], accuracy_pcb[opt_pcb], color='blue', marker='D', ms=10)
if PLOT_AMB_COMBINED:
    axs[1,0].plot(mem_amb_combined, accuracy_amb_combined, color='red', linestyle='--', label='Combined (Hybrid + Blowup)', linewidth=2)
    axs[1,0].plot(mem_amb_combined[opt_amb_combined], accuracy_amb_combined[opt_amb_combined], color='red', marker='D', ms=10)
axs[1,0].plot(mem_auto, accuracy_auto, color='black', marker='D', ms=10)
axs[1,0].set_xlabel('Alignment Mem (GB)')
axs[1,0].set_ylabel('% Correct Overall')

if PLOT_POP_COV:
    axs[1,1].plot(pct_pc, mem_pc, color='blue', label='Pop Cov', linewidth=2)
if PLOT_AMB:
    axs[1,1].plot(pct_amb, mem_amb, color='red', label='Hybrid', linewidth=2)
if PLOT_POP_COV_COMBINED:
    axs[1,1].plot(pct_pcb, mem_pcb, color='blue', linestyle='--', label='Pop Cov + Blowup', linewidth=2)
if PLOT_AMB_COMBINED:
    axs[1,1].plot(pct_amb_combined, mem_amb_combined, color='red', linestyle='--', label='Hybrid + Blowup (0.5)', linewidth=2)
axs[1,1].plot([0,100], [mem_auto, mem_auto], color='black', label='HISAT2 Auto Prune', linewidth=1.5)

plt.legend(bbox_to_anchor=(-1,-0.1), loc='upper left')
axs[1,1].set_xlabel('% SNPs')
axs[1,1].set_ylabel('Alignment Mem (GB)')
plt.savefig('chr' + chrom + '_hisat_vs_mem.png', bbox_inches='tight')
plt.clf()
