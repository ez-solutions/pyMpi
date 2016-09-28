#!/bin/python

import imp
import sys
import time
import timeit


def loop(num_steps):
    sum = 0.0
    step = 1.0 / num_steps
    for i in xrange(num_steps):
        x = (i+0.5)*step
        sum += 4.0/(1.0+x*x)
    return sum


def Pi(num_steps):
    start = time.time()
    
    sum = loop(num_steps)
    
    pi = sum / num_steps
    end = time.time()
    print "\n\nPi with %d steps is %f in %f secs\n\n" % (num_steps, pi, end-start)


if __name__ == '__main__':
    Pi(2000000)