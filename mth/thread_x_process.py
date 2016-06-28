import math
#from Queue import Queue
import time
import threading
import multiprocessing

def factorize_naive(n):
    """ A naive factorization method. Take integer 'n', return list of
        factors.
    """
    if n < 2:
        return []
    factors = []
    p = 2

    while True:
        if n == 1:
            return factors

        r = n % p
        if r == 0:
            factors.append(p)
            n = n / p
        elif p * p >= n:
            factors.append(n)
            return factors
        elif p > 2:
            # Advance in steps of 2 over odd numbers
            p += 2
        else:
            # If p == 2, get to 3
            p += 1
    assert False, "unreachable"

def serial_factorizer(nums):
    return {n: factorize_naive(n) for n in nums}

def threaded_factorizer(nums, nthreads):
    def worker(nums, outdict):
        """ The worker function, invoked in a thread. 'nums' is a
            list of numbers to factor. The results are placed in
            outdict.
        """
        for n in nums:
            outdict[n] = factorize_naive(n)

    # Each thread will get 'chunksize' nums and its own output dict
    chunksize = int(math.ceil(len(nums) / float(nthreads)))
    threads = []
    outs = [{} for i in range(nthreads)]

    for i in range(nthreads):
        # Create each thread, passing it its chunk of numbers to factor
        # and output dict.
        t = threading.Thread(
                target=worker,
                args=(nums[chunksize * i:chunksize * (i + 1)],
                      outs[i]))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Merge all partial output dicts into a single dict and return it
    return {k: v for out_d in outs for k, v in out_d.iteritems()}

class worker2():
    def __init__(self, nums, out_q):
        self.nums=nums
        self.out_q=out_q
        outdict={}
        for n in nums:
            outdict[n]=factorize_naive(n)
        out_q.put(outdict)

def mp_factorizer(nums, nprocs):
    # Each process will get 'chunksize' nums and a queue to put his out
    # dict into
    out_q = multiprocessing.Queue()
    chunksize = int(math.ceil(len(nums) / float(nprocs)))
    procs = []

    for i in range(nprocs):
        p = multiprocessing.Process(
                target=worker2,
                args=(nums[chunksize * i:chunksize * (i + 1)],
                      out_q))
        procs.append(p)
        p.start()

    # Collect all results into a single result dict. We know how many dicts
    # with results to expect.
    resultdict = {}
    for i in range(nprocs):
        resultdict.update(out_q.get())

    # Wait for all worker processes to finish
    for p in procs:
        p.join()

    return resultdict


if __name__ == '__main__':
    print "allocating...",
    nums=range(500000)
    print "done."
    print "running serial...",
    t0=time.time()
    serial_factorizer(nums)
    t1=time.time()
    print "done. took %.3fs" % (t1-t0)
    print "running multi-thread...",
    t0=time.time()
    threaded_factorizer(nums, 8)
    t1=time.time()
    print "done. took %.3fs" % (t1-t0)
    print "running multi-processes",
    t0=time.time()
    mp_factorizer(nums, 8)
    t1=time.time()
    print "done. took %.3fs" % (t1-t0)
