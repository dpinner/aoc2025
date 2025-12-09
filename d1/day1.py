import sys

if __name__ == "__main__":
    filename = sys.argv[1]
    cur = 50
    cnt1, cnt2 = 0, 0
    with open(filename,'r') as f:
        for l in f.read().splitlines():
            d = 1 if l[0] == 'R' else -1
            n = int(l[1:])
            cnt2 += n // 100
            n %= 100
            cnt2 += int(d == 1 and n > (100 - cur))
            cnt2 += int(d == -1 and n > cur > 0)
            cur += d * n
            cur %= 100
            cnt1 += int(cur == 0)
            

    print(cnt1)
    print(cnt1 + cnt2)