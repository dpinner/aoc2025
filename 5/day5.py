import sys
from sortedcontainers import SortedList

def insert_ival(ivals: SortedList, ival: tuple[int,int]):
    idx = ivals.bisect_left(ival)

    if idx == len(ivals):
        ivals.add(ival)
        return
    
    to_remove = []
    merged_ival = ival
    if idx > 0 and ivals[idx-1][1] >= ival[0]:
        to_remove.append(idx-1)
        merged_ival = (ivals[idx-1][0], max(ivals[idx-1][1],ival[1]))

    while idx < len(ivals) and ivals[idx][0] <= merged_ival[1]:
        merged_ival = (merged_ival[0], max(ivals[idx][1], merged_ival[1]))
        to_remove.append(idx)
        idx += 1

    for i in to_remove[::-1]:
        del ivals[i]

    ivals.add(merged_ival)


def is_contained(ivals: SortedList, val: int) -> bool:
    idx = ivals.bisect_left((val,-1))

    return (idx < len(ivals) and ivals[idx][0] == val) or (idx > 0 and ivals[idx-1][1] >= val)



if __name__ == "__main__":
    filename = sys.argv[1]
    ivals = SortedList(key = lambda ival: ival[0])
    ids = []
    hit_newline = False
    with open(filename,'r') as f:
        for line in f:
            if line.rstrip() == '':
                hit_newline = True
                continue
            if not hit_newline:
                insert_ival(ivals, tuple(map(int, line.rstrip().split('-'))))
            else:
                ids.append(int(line.rstrip()))

    tot1 = sum(int(is_contained(ivals, id)) for id in ids)
    tot2 = sum(x[1]-x[0]+1 for x in ivals)

    
    print(tot1, tot2)