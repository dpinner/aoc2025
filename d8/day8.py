import sys
import itertools

class UnionFind:
    def __init__(self, n: int):
        self.parents = [i for i in range(n)]
        self.sizes = [1]*n
        self.subgraphs = n

    def find(self, i: int):
        while i != self.parents[i]:
            tmp = i
            i = self.parents[i]
            self.parents[tmp] = self.parents[i]

        return i

        

    def union(self, i: int, j: int):
        pi = self.find(i)
        pj = self.find(j)
        if pi == pj:
            return
        
        self.subgraphs -= 1
        if self.sizes[pi] < self.sizes[pj]:
            self.parents[pi] = pj
            self.sizes[pj] += self.sizes[pi]
        else:
            self.parents[pj] = pi
            self.sizes[pi] += self.sizes[pj]


if __name__ == "__main__":
    filename = sys.argv[1]
    locs = []
    with open(filename,'r') as f:
        lines = f.read().splitlines()
        locs = [tuple(map(int, line.split(','))) for line in lines]

    pairs = sorted(
        itertools.combinations(range(len(locs)), 2), 
        key=lambda p: 
            (locs[p[0]][0] - locs[p[1]][0])**2 + 
            (locs[p[0]][1] - locs[p[1]][1])**2 + 
            (locs[p[0]][2] - locs[p[1]][2])**2
    )

    uf = UnionFind(len(locs))
    x1,x2 = None,None
    for i in range(1000):
        pair = pairs[i]
        uf.union(*pair)
        if uf.subgraphs == 1 and x1 is None and x2 is None:
            x1 = locs[pair[0]][0]
            x2 = locs[pair[1]][0]

    sizes = sorted(uf.sizes, key=lambda s:-s)
    print(sizes[0]*sizes[1]*sizes[2])

    while uf.subgraphs > 1:
        pair = pairs[i]
        uf.union(*pair)
        i += 1

    x1 = x1 or locs[pair[0]][0]
    x2 = x2 or locs[pair[1]][0]
    
    print(x1*x2)
