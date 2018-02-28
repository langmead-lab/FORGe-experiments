#! /usr/bin/env python2.7

import sys

perfect = 0
unique_mapped = 0
unique_score = 0

curr_name = None
rem_hits = 0
curr_best = 0
curr_sec = 0
with open(sys.argv[1], 'r') as f:
  for line in f:
    if line[0] == '@':
      continue

    row = line.rstrip().split('\t')
    score = 0
    for r in row[11:]
      if r[:5] == 'AS:i:':
        score = int(r[5:]):
        break

    if curr_name and rem_hits > 0:
      if not row[0] == curr_name:
        print("Error! Reads not in order? Couldn't find " + curr_name)
      for r in row[11:]:
          if score > curr_best:
            curr_sec = curr_best
            curr_best = score
          elif score > curr_sec:
            curr_sec = score

      rem_hits -= 1
      if rem_hits == 0 and curr_best > curr_sec:
        unique_score += 1
    else:
      for r in row[11:]:
        if r[:5] == 'NH:i:':
          hits = int(r[5:])
          if hits == 1:
            unique_mapped += 1
            unique_score += 1
            if score == 0:
              perfect += 1
          else:
            curr_name = row[0]
            rem_hits = hits - 1
            curr_best = score
            curr_sec = 0
