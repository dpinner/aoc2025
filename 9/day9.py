import sys
import itertools

if __name__ == "__main__":
    filename = sys.argv[1]
    locs = []
    with open(filename, "r") as f:
        lines = f.read().splitlines()
        locs = [tuple(map(int, line.split(","))) for line in lines]

    pairs = sorted(
        itertools.combinations(range(len(locs)), 2),
        key=lambda p: (abs(locs[p[0]][0] - locs[p[1]][0]) + 1)
        * (abs(locs[p[0]][1] - locs[p[1]][1]) + 1),
    )

    corners = pairs[-1]
    print(
        (abs(locs[corners[0]][0] - locs[corners[1]][0]) + 1)
        * (abs(locs[corners[0]][1] - locs[corners[1]][1]) + 1)
    )
