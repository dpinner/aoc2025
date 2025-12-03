import sys

def invalids(sstart: str, sstop: str) -> int:
    start = int(sstart)
    stop = int(sstop)

    tot = 0
    tot_2 = 0

    lstart = len(sstart)
    lstop = len(sstop)

    lmax = max(lstart,lstop) + 1

    seen = set()

    for d in range(2, lmax):
        dstart = lstart // d

        seed = sstart[:dstart] if len(sstart) % d == 0 else '1' + '0'*dstart

        n = int(seed * d)

        while n < start:
            seed = str(int(seed) + 1)
            n = int(seed * d)

        while n <= stop:
            if n not in seen:
                tot += n
                tot_2 += n if d == 2 else 0
            seen.add(n)
            seed = str(int(seed) + 1)
            n = int(seed * d)


    return tot_2, tot

if __name__ == "__main__":
    filename = sys.argv[1]
    tot, tot_2 = 0,0
    with open(filename,'r') as f:
        ranges = f.readline().strip().split(",")
        for r in ranges:
            start,stop = r.split("-")
            t_2,t = invalids(start, stop)
            tot_2 += t_2
            tot += t

    print(tot_2)
    print(tot)