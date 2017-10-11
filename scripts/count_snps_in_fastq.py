import sys
import bisect

def read_snps(snp_file):
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

            if not chrom == last_chrom:
                if last_chrom:
                    all_vars[last_chrom] = sorted(S)
                S = []
            elif pos == last_pos:
                S[-1] = (S[-1][0], S[-1][1]+freq)
            else:
                S.append((pos, freq))
            last_chrom = chrom
            last_pos = pos

    if last_chrom:
        all_vars[last_chrom] = sorted(S)

    print(all_vars.keys())

    return all_vars['9']

S = read_snps(sys.argv[1])
num_s = len(S)

index_skip = 10000
index = [0] * (int(S[-1][0] / index_skip)+1)
curr_i = 0
for i in range(num_s):
    while S[i][0] >= (curr_i * index_skip):
        index[curr_i] = i
        curr_i += 1

index_len = len(index)
with open(sys.argv[2], 'r') as f:
    with open(sys.argv[3], 'w') as f_out:
        counts = []
        for line in f:
            if not line[0] == '@':
                f_out.write(line)
                continue

            row = line.rstrip().split(' ')
            start = -1
            end = -1
            for r in row:
                if r[:11] == 'orig_begin=':
                    start = int(r[11:])
                elif r[:9] == 'orig_end=':
                    end = int(r[9:])
                elif r[:5] == 'snps=':
                    snps = int(r[5:])

            debug = False
            #if row[0] == '@sim_l100_hapA.fastq.000001421':
            #    debug = True

            if start == -1 or end == -1:
                f_out.write(line)
                continue

        
            if int(start / index_skip) >= index_len:
                f_out.write(line)
                continue

            freqs = []
            s_start = index[int(start / index_skip)]
            while s_start < num_s:
                if S[s_start][0] >= start:
                    break
                s_start += 1
            s_end = s_start
            while s_end < num_s:
                if S[s_end][0] >= end:
                    break
                s_end += 1

            if debug:
                print(start)
                print('%d - %d / %d' % (s_start, s_end, num_s))
                print(S[s_start-1])
                print(S[s_start:s_end+1])

            count_snps = s_end - s_start
            freqs = [s[1] for s in S[s_start:s_end]]

            f_out.write(line.rstrip() + ' nsnps=' + str(count_snps) + ' freqs=' + ','.join([str(fr) for fr in freqs]) + ' del=0\n')

