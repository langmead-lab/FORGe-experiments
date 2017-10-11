#! /usr/bin/env python2.7

import sys
import bisect

'''
Usage: ./add_read_info.py snps.1ksnp del_variants.vcf confident_regions.bed repeat_regins.bed reads.fastq output.fastq
1ksnp file should be sorted by chromsome and position
'''

index_skip = 10000

def read_bed(bed, chrom):
    intervals = []
    with open(bed, 'r') as f:
        for line in f:
            row = line.rstrip().split('\t')
            if row[0] == 'chr'+chrom:
                intervals.append((int(row[1]), int(row[2])))
    return intervals

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
                    all_vars[last_chrom] = sorted(S)
                S = []
            elif pos == last_pos:
                S[-1] = (S[-1][0], S[-1][1]+freq, S[-1][2] or deleterious)
            else:
                S.append((pos, freq, deleterious))
            last_chrom = chrom
            last_pos = pos

    if last_chrom:
        all_vars[last_chrom] = sorted(S)

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

def add_read_info(in_reads, out_reads, all_vars, conf, repeats):
    numc = len(conf)
    numr = len(repeats)
    with open(in_reads, 'r') as f:
        with open(out_reads, 'w') as f_out:
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

                debug = False
                #if row[0] == '@sim_l100_hapA.fastq.000001421':
                #    debug=True

                if not chrom or start == -1 or end == -1:
                    print('Error! Couldn\'t parse line: ' + line.rstrip())
                    f_out.write(line.rstrip() + ' nsnps=0 del=0 freqs=\n')
                    continue

                freqs = []
                v = all_vars[chrom]
                num_s = len(v)
                s_start = bisect.bisect_left(v, (start,0,0))
                s_end = s_start
                while s_end < num_s:
                    if v[s_end][0] >= end:
                        break
                    s_end += 1

                if debug:
                    print(start)
                    print('%d - %d / %d' % (s_start, s_end, num_s))
                    print(v[s_start-1])
                    print(v[s_start:s_end+1])

                count_snps = s_end - s_start
                count_del = sum([s[2] for s in v[s_start:s_end]])
                freqs = [str(s[1]) for s in v[s_start:s_end]]

                conf_v = 0
                conf_i = bisect.bisect_left(conf, (start,start))-1
                while conf_i < numc and conf[conf_i][0] <= start:
                    if conf[conf_i][1] >= end:
                        conf_v = 2
                        break
                    elif conf[conf_i][1] > start:
                        conf_v = 1
                        break
                    conf_i += 1
                if not conf_v and conf[conf_i][0] < end:
                    conf_v = 1

                rep_v = 0
                rep_i = bisect.bisect_left(repeats, (start,start))-1
                while rep_i < numr and repeats[rep_i][0] <= start:
                    if repeats[rep_i][1] >= end:
                        rep_v = 2
                        break
                    elif repeats[rep_i][1] > start:
                        rep_v = 1
                        break
                    rep_i += 1
                if not rep_v and repeats[rep_i][0] < end:
                    rep_v = 1

                f_out.write(line.rstrip() + ' nsnps=' + str(count_snps) + ' del=' + str(count_del) + ' freqs=' + ','.join(freqs) + ' conf=' + str(conf_v) + ' rep='+ str(rep_v) + '\n')

if __name__ == '__main__':
    snps_file = sys.argv[1]
    del_var_file = sys.argv[2]
    conf_regions = sys.argv[3]
    repeat_regions = sys.argv[4]
    in_reads = sys.argv[5]
    out_reads = sys.argv[6]

    del_vars = read_del_vars(del_var_file)
    all_snps = read_snps(snps_file, del_vars)
    conf = read_bed(conf_regions, '9')
    repeats = read_bed(repeat_regions, '9')

    add_read_info(in_reads, out_reads, all_snps, conf, repeats)
