#! /usr/bin/env python2.7

# Executes a given command and prints the peak memory usage after completion

import resource
import subprocess
import threading
import sys

max_mem = 0
def finish():
    print('Maximum memory: %0.1f MB' % (max_mem / 1000.0))
    #exit()

def run():
    proc = subprocess.Popen(sys.argv[1:])

    proc.wait()
    finish()

    return

thread = threading.Thread(target=run)
thread.start()

while thread.isAlive():
    mem = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    if mem > max_mem:
        max_mem = mem
    #sleep()

