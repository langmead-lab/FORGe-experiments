#! /usr/bin/env python2.7

# Map reads simulated from a personalized genome to their coordinates in the reference genome

import sys


def indel_file_parser(fn):
    with open(fn, 'r') as fh:
        for ln in fh:
            row = ln.rstrip().split()
            chrom = row[0]
            pos = int(row[1])     # position with respect to reference
            change = int(row[2])  # +ve for insertion in donor, -ve for deletion
            yield chrom, pos, change


def accumulator(rec_iter):
    curr_offset = 0
    for rec in rec_iter:
        chrom, pos, change = rec
        curr_offset += change
        yield pos + curr_offset, -curr_offset


def densify(accum):
    # For every base in the non-reference genome, what do I have to add to it
    # to get its offset w/r/t the reference
    mapping = list(accum)
    map_arr = [0] * (mapping[-1][0]+1)
    offset = 0
    for m in range(len(mapping)-1):
        offset += mapping[m][1]
        for i in range(mapping[m][0], mapping[m+1][0]):
            map_arr[i] = mapping[m][1]
    map_arr[mapping[-1][0]] = mapping[-1][1]
    return map_arr


def go():
    # Indels inserted into ref genome to get personalized genome
    indels = sys.argv[1]
    reads_in = sys.argv[2]

    mapping = list(accumulator(indel_file_parser(indels)))
    map_arr = list(densify(mapping))
    num_indels = len(mapping)
    def map(id):
        if id > mapping[-1][0]:
            return id + map_arr[-1]
        else:
            return id + map_arr[id]

    # Modify Mason records to have reference coordinates

    with open(reads_in, 'r') as f_in:
        #with open(reads_out, 'w') as f_out:
        for line in f_in:
            if line[0] == '@':
                tags = line.rstrip().split(' ')
                found_begin = False
                found_end = False
                for i in range(len(tags)):
                    if tags[i][:11] == 'orig_begin=':
                        #print('Mapping %d -> %d' % (int(tags[i][11:]), map(int(tags[i][11:]))))
                        tags[i] = 'orig_begin=' + str(map(int(tags[i][11:])))
                        found_begin = True
                        if found_end:
                            break
                    elif tags[i][:9] == 'orig_end=':
                        tags[i] = 'orig_end=' + str(map(int(tags[i][9:])))
                        found_end = True
                        if found_begin:
                            break
                #f_out.write(' '.join(tags) + '\n')
                print(' '.join(tags))
            else:
                #f_out.write(line)
                print(line.rstrip())
            #exit()


if __name__ == '__main__':
    go()


def test_indel_file_parser():
    with open('tmp.txt', 'w') as fh:
        fh.write("""chr1 10 1
chr1 20 -1""")
    recs = list(indel_file_parser('tmp.txt'))
    assert 2 == len(recs)
    assert 'chr1' == recs[0][0] == recs[1][0]
    assert 10 == recs[0][1]
    assert 20 == recs[1][1]
    assert 1 == recs[0][2]
    assert -1 == recs[1][2]


def test_accumulator():
    # Ref: 01234567890-12345678901234
    #                1          2
    #      ||||||||||| ||||||||| ||||
    # Alt: 012345678901234567890-1234
    #                1         2
    with open('tmp.txt', 'w') as fh:
        fh.write("""chr1 10 1
chr1 20 -1""")
    mapping = list(accumulator(indel_file_parser('tmp.txt')))
    assert 2 == len(mapping)
    assert 11 == mapping[0][0]
    assert -1 == mapping[0][1]
    assert 20 == mapping[1][0]
    assert 0 == mapping[1][1]


def test_densify():
    # Ref: 01234567890-12345678901234
    #                1          2
    #      ||||||||||| ||||||||| ||||
    # Alt: 012345678901234567890-1234
    #                1         2
    with open('tmp.txt', 'w') as fh:
        fh.write("""chr1 10 1
chr1 20 -1""")
    map_array = list(densify(accumulator(indel_file_parser('tmp.txt'))))
    assert 0 == map_array[0]
    assert 0 == map_array[1]
    assert 0 == map_array[2]
    assert 0 == map_array[10]
    #assert -1 == map_array[11]  # could be either 0 or -1
    assert -1 == map_array[12]
    assert -1 == map_array[13]
    assert -1 == map_array[14]
    assert -1 == map_array[15]
    assert -1 == map_array[16]
    assert -1 == map_array[17]
    assert -1 == map_array[18]
    assert -1 == map_array[19]
    #assert 0 == map_array[20]
