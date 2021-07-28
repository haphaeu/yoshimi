'''
Tower of Hanoi

author: Rafael Rossi
date: 28.07.2021
'''

# Global variables
#
#  N: 
#      number of disks
#  I: 
#      iteraction counter
#  SRC, DST, TMP:
#      lists representing the source, temp and destination towers.
N, I = 0, 0
SRC, DST, TMP = [], [], []


def hanoi(n, src, dst, tmp):
    '''Recursive Hanoi algorithm. 
    
    src, dst, tmp are lists, for example, in the start of a n == 3 problem,
    the source tower will be src == [3, 2, 1].
    '''
    global I
    if n > 0:
        hanoi(n-1, src, tmp, dst)
        # move n from src to dst
        dst.append(src.pop())
        I += 1
        show()
        hanoi(n-1, tmp, dst, src)

def show():
    '''Show each iteraction of the algorithm.'''
    def fix(tmp):
        return repr(tmp).rjust(r)
    r = 3 * N + 5    
    print(f'{I:3d} \t {fix(SRC)} \t {fix(TMP)} \t {fix(DST)}')
    
    
def go(n):
    '''Sets the globals and runs the Hanoi algorithm for `n` disks.'''

    print(f'Solving the Tower of Hanoi with {n} disks ({2**n-1} iterations).')

    global N, I, SRC, DST, TMP, DELAY
    # Resets globals upon each
    N = n
    I = 0
    DST, TMP = [], []
    SRC = [N-i for i in range(N)]
    
    show()
    hanoi(N, SRC, DST, TMP)    

if __name__ == '__main__':
    go(3)
