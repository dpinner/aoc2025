import sys
from collections import defaultdict

if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename, "r") as f:
        grid = f.read().splitlines()

    tot_1, tot_2 = 0, 1
    locs = defaultdict(int)
    locs[grid[0].find("S") if grid else -1] = 1
    for row in grid:
        new_locs = defaultdict(int)
        for loc in locs.keys():
            if loc >= 0 and loc < len(row) and row[loc] == "^":
                tot_1 += 1
                tot_2 += locs[loc]
                new_locs[loc - 1] += locs[loc]
                new_locs[loc + 1] += locs[loc]
            else:
                new_locs[loc] += locs[loc]

        locs = new_locs

    print(tot_1, tot_2)
