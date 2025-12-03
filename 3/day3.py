import sys

def joltage(bank: str, n: int) -> int:
    vals = []
    for i,b in enumerate(bank):
        while vals and vals[-1] < int(b) and len(vals) + len(bank) - i > n:
            vals.pop()

        if len(vals) < n:
            vals.append(int(b))

    tot = 0
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