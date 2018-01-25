#! /usr/bin/env python2.7

import sys

genome_in = sys.argv[1]
snps_file = sys.argv[2]
genome_out = sys.argv[3]

def read_genome(filename, target_chrom=None):
    G = dict()
    header = dict()
    seq = None
    skip = False

    with open(filename, 'r') as f:
        for line in f:
            # Skip header line
            if line[0] == '>':
                if not skip and seq:
                    G[chrom] = seq
                chrom = line.rstrip().split(' ')[0][1:]
                seq = ''
                if target_chrom and not chrom == target_chrom:
                    skip = True
                else:
                    header[chrom] = line
                    skip = False
                continue

            if not skip:
                seq += line.rstrip()
    if not skip and seq:
        G[chrom] = seq

    return header, G

def update_snps(header, G, snps, outfile):
    last_name, last_chrom, last_pos, alleles, probs = None, None, None, None, None
    major = dict()
    for chrom,seq in G.items():
        major[chrom] = list(seq[:])

    changed = 0
    total = 0

    with open(snps, 'r') as f:
        for line in f:
            row = line.rstrip().split('\t')
            chrom = row[0]
            pos = int(row[1])
            ref = row[2]
            alt = row[3]
            p_alt = float(row[4])
            name = row[7]

            if name == last_name:
                alleles.append(alt)
                probs.append(p_alt)
                probs[0] -= p_alt
            else:
                if last_name:
                    total += 1
                    max_i = 0
                    for i in range(1, len(probs)):
                        if probs[i] > probs[max_i]:
                            max_i = i
                    if max_i > 0:
                        changed += 1
                    major[last_chrom][last_pos-1] = alleles[max_i]

                last_name, last_chrom, last_pos = name, chrom, pos
                alleles = [ref, alt]
                probs = [1-p_alt, p_alt]

    print('%d / %d alleles changed to major' % (changed, total))

    with open(outfile, 'w') as f:
        for chrom, seq in major.items():
            f.write(header[chrom])
            for i in range(0, len(seq), 60):
                f.write(''.join(seq[i:i+60]) + '\n')

header, genome = read_genome(genome_in, target_chrom='9')
update_snps(header, genome, snps_file, genome_out)

