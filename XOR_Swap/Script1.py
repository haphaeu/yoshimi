from xor_swap import BatchTests
#BatchTests(numTimes, ArraySize)
BatchTests(100,1000)
#results of the tests indicate that allocating with tmp is
#almost twice faster than with XOR...