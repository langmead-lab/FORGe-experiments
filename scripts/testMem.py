#! /usr/bin/env python2.7

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
    '''
    max_mem = 0
    while proc.poll() is None:
        mem = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
        print(mem)
        if mem > max_mem:
            max_mem = mem

    print(max_mem)
    '''

thread = threading.Thread(target=run)
thread.start()

while thread.isAlive():
    mem = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    if mem > max_mem:
        max_mem = mem
    #sleep()

