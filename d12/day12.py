import sys
import re


if __name__ == "__main__":
    filename = sys.argv[1]
    re2 = r'^\d+x\d+:'
    re1 = r'^\d+:'
    idx = -1

    regions = []
    presents = []

    cur_w, cur_h, cur_a = 0,0,0


    with open(filename, "r") as f:
        for line in f.read().splitlines():
            h1 = re.match(re1, line)
            h2 = re.match(re2, line)

            if h2:
                if cur_a > 0:
                    presents.append((cur_w,cur_h,cur_a))
                    cur_w,cur_h,cur_a = 0,0,0
                counts = list(map(int,line.split(":")[1].split()))
                w,h = h2[0][:-1].split("x")

                regions.append((int(w),int(h),counts))

            elif h1:
                if cur_a > 0:
                    presents.append((cur_w,cur_h,cur_a))
                cur_w,cur_h,cur_a = 0,0,0

            else:
                cur_w = max(cur_w,len(line))
                cur_h += int(len(line) > 0)
                cur_a += sum(int(c == '#') for c in line)

    
    fit,no_fit,pack = 0,0,0

    max_w = max(p[0] for p in presents)
    max_h = max(p[1] for p in presents)

    for (w,h,counts) in regions:
        packed_area, tot = 0,0
        for i,c in enumerate(counts):
            packed_area += presents[i][2] * c
            tot += c

        if (w // max_w) * (h // max_h) >= tot:
            fit += 1
        elif packed_area > w * h:
            no_fit += 1
        else:
            pack += 1

    print(fit, no_fit, pack)

