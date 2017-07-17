# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 13:08:47 2017

@author: raf
"""

import asyncio
from numpy.random import randint


async def slow_operation(n):
    x = randint(3, 7)
    print('Slow operation {} started. Waiting {}s'.format(n, x))
    await asyncio.sleep(x)
    print("Slow operation {} complete".format(n))


async def main():
    print('Start main')
    await asyncio.wait([
        slow_operation(1),
        slow_operation(2),
        slow_operation(3),
    ])
    print('main done')

print('Start script')
loop = asyncio.get_event_loop()
print('RUnning loop')
loop.run_until_complete(main())
print('End of script')


ints = (1,2,3,4)
sqs = (i*i for i in ints)
for i, s in zip(ints, sqs):
    print(i, s)