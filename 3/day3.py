import sys
import heapq

def joltage(bank: str, n: int) -> int:
    vals = []
    idx = -1
    while n > 0:
        cur = 0
        for i in range(idx+1, len(bank)-n+1):
            if cur == 9:
                break
            j = int(bank[i])
            if j > cur:
                cur = j
                idx = i

        vals.append(cur)
        n -= 1

    tot = 0
    n = len(vals)
    for i in range(n):
        tot += (10 ** (n-1-i)) * vals[i]
    return tot

if __name__ == "__main__":
    filename = sys.argv[1]
    tot1, tot2 = 0, 0
    with open(filename,'r') as f:
        for l in f.read().splitlines():
            tot1 += joltage(l, 2)
            tot2 += joltage(l, 12)
            

    print(tot1)
    print(tot2)