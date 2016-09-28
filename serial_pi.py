#!/bin/python

import imp
import sys
import time
import timeit
# from numba import jit

try:
    imp.find_module('mpi4py')
    # imp.find_module('line_profiler')
    found = True
    from mpi4py import MPI
except ImportError:
    sys.exit("mpi4py Module not found.")
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def loop(num_steps):
    sum = 0.0
    step = 1.0 / num_steps
    for i in xrange(num_steps):
        x = (i+0.5)*step
        sum += 4.0/(1.0+x*x)
    return sum

def opt_loop(num_steps, begin, end):
    step = 1.0/num_steps
    sum = 0
    for i in xrange(begin, end):
        x = (i+0.5)*step
        sum += 4.0/(1.0+x*x)
    return sum

def Pi(num_steps):
    t0 = MPI.Wtime()
    start = time.time()
    
    sum = loop(num_steps)
    

    pi = sum / num_steps
    t1 = MPI.Wtime()-t0
    print "\n\nPi with %d steps is %f in %f secs\n\n" % (num_steps, pi, t1)

def opt_Pi(num_steps):
    t0 = MPI.Wtime()
    # num_steps = int(num_steps.replace(',', ''))
    # start = time.time()
    num_steps2 = num_steps / size
    start = rank * num_steps2
    end = start + num_steps2
    local_sum = opt_loop(num_steps, start, end)

    sum = comm.reduce(local_sum, op=MPI.SUM, root=0)
    t1 = MPI.Wtime()-t0
    if rank == 0:
        pi = sum / num_steps
        print "\n\nPi with %d steps is %f in %f secs\n\n" % (num_steps, pi, t1)




def hello_mpi():
    
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    print "hello world from process %d/%d" %(rank,size)


def hello_p2p():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    if rank == 0:
        for i in xrange(1, size):
            sendMsg = "Hello, Rank %d" % i
            comm.send(sendMsg, dest=i)
    else:
        recvMsg = comm.recv(source=0)
        print recvMsg

def hello_bcast():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    if rank == 0:
        comm.bcast("Hello from Rank 0", root = 0)
    else:
        msg=comm.bcast('', root=0)
        print "Rank %d received: %s" % (rank, msg)

def sum_p2p():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    # set value to all thread based on their rank
    val = (rank+1)*10
    print "Rank %d has value %d " % (rank, val)
    # calculate total on master node
    if rank == 0:
        sum = val
        for i in xrange(1, size):
            sum += comm.recv(source=i)
        print "Rank 0 worked out the total %d " % sum
    else:
        comm.send(val, dest=0)

def mpi_reduce():
    """
    equivalent to sum_p2p
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    # set value to all thread based on their rank
    val = (rank+1)*10
    print "Rank %d has value %d " % (rank, val)
    sum = comm.reduce(val, op=MPI.SUM, root=0)
    if rank == 0:
        print "Rank 0 worked out the total %d" % sum

# if rank == 0:
#     print 'Parallel time:'
#     tp = timeit.Timer("opt_Pi(10000)","from __main__ import opt_Pi")
#     print tp.timeit(number=10)

#     print 'Serial time:'
#     ts = timeit.Timer("Pi(10000)","from __main__ import Pi")
#     print ts.timeit(number=10)
    # hello_mpi()
    # hello_p2p()
    # hello_bcast()
    # sum_p2p()
    # mpi_reduce()

if __name__ == '__main__':
    Pi(10000)
    # opt_Pi(10000)
