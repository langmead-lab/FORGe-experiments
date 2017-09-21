#! /usr/bin/env python2.7

import sys

'''
Usage: ./add_read_info.py snps.1ksnp del_variants.vcf reads.fastq output.fastq
1ksnp file should be sorted by chromsome and position
'''

index_skip = 10000

def read_snps(snp_file, del_vars):
    all_vars = dict()
    last_chrom = None
    last_pos = -1
    with open(snp_file, 'r') as f:
        for line in f:
            row = line.rstrip().split('\t')
            chrom = row[0]
            pos = int(row[1])+1
            orig = row[2]
            freq = float(row[4])
            tag = row[7]

            # Cross-reference with list of deleterious variants
            deleterious = 0
            for d in del_vars[chrom]:
                #if d[0] == pos and orig in d[1]:
                if d == tag:
                    deleterious = 1
                    break

            if not chrom == last_chrom:
                if last_chrom:
                    all_vars[last_chrom] = S
                S = []
            elif pos == last_pos:
                S[-1] = (S[-1][0], S[-1][1]+freq, S[-1][2] or deleterious)
            else:
                S.append((pos, freq, deleterious))
            last_chrom = chrom
            last_pos = pos

    if last_chrom:
        all_vars[last_chrom] = S

    print(all_vars.keys())

    return all_vars

def read_del_vars(filename):
    del_vars = dict()
    with open(filename, 'r') as f:
        for line in f:
            if line[0] == '#':
                continue

            row = line.rstrip().split('\t')
            chrom = row[0]
            #pos = int(row[1])
            #origs = row[3].split(',')
            #alts =  row[4].split(',')
            tag = row[2]

            if chrom in del_vars:
                #del_vars[chrom].append((pos, origs, alts))
                del_vars[chrom].append(tag)
            else:
                #del_vars[chrom] = [(pos, origs, alts)]
                del_vars[chrom] = [tag]

    return del_vars

def index_snps(all_vars):
    index = dict()

    for chrom, v in all_vars.items():
        curr_index = [0] * (int(v[-1][0] / index_skip)+1)
        curr_i = 0
        for i in range(len(v)):
            while v[i][0] >= (curr_i * index_skip):
                curr_index[curr_i] = i
                curr_i += 1
        index[chrom] = curr_index
    return index

def add_read_info(in_reads, out_reads, all_vars, index):
    with open(in_reads, 'r') as f:
        with open(out_reads, 'w') as f_out:
            counts = []
            line_id = 0
            for line in f:
                if not line_id % 4 == 0:
                    f_out.write(line)
                    line_id += 1
                    continue
                line_id += 1

                row = line.rstrip().split(' ')
                chrom = None
                start = -1
                end = -1
                for r in row:
                    if r[:7] == 'contig=':
                        chrom = r[7:]
                    if r[:11] == 'orig_begin=':
                        start = int(r[11:])
                    elif r[:9] == 'orig_end=':
                        end = int(r[9:])
                    elif r[:5] == 'snps=':
                        snps = int(r[5:])

                if not chrom or start == -1 or end == -1:
                    f_out.write(line.rstrip() + ' nsnps=0 del=0 freqs=\n')
                    continue

                freqs = []
                curr_index = index[chrom]
                v = all_vars[chrom]
                p = int(start / index_skip)
                if p >= len(curr_index):
                    f_out.write(line.rstrip() + ' nsnps=0 del=0 freqs=\n')
                    continue
                s_start = curr_index[p]
                num_s = len(v)
                while s_start < num_s:
                    if v[s_start][0] >= start:
                        break
                    s_start += 1
                s_end = s_start
                while s_end < num_s:
                    if v[s_end][0] >= end:
                        break
                    s_end += 1

                count_snps = s_end - s_start
                count_del = sum([s[2] for s in v[s_start:s_end]])
                freqs = [str(s[1]) for s in v[s_start:s_end]]

                f_out.write(line.rstrip() + ' nsnps=' + str(count_snps) + ' del=' + str(count_del) + ' freqs=' + ','.join(freqs) + '\n')

if __name__ == '__main__':
    snps_file = sys.argv[1]
    del_var_file = sys.argv[2]
    in_reads = sys.argv[3]
    out_reads = sys.argv[4]

    del_vars = read_del_vars(del_var_file)
    all_snps = read_snps(snps_file, del_vars)
    index = index_snps(all_snps)

    add_read_info(in_reads, out_reads, all_snps, index)
