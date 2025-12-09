import sys
from collections import deque

def clear(grid: list[list[str]], thresh: int) -> tuple[int,int]:
    ns = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    counts = {}
    q = deque([])
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == '.':
                continue
            cnt = 0
            for (dr,dc) in ns:
                if row + dr < 0 or row + dr >= len(grid):
                    continue
                if col + dc < 0 or col + dc >= len(grid[0]):
                    continue
                cnt += int(grid[row+dr][col+dc] == '@')

            counts[(row,col)] = cnt
            if cnt < thresh:
                q.append((row,col))
            counts[(row,col)] = cnt
    
    init = len(q)
    final = 0

    while q:
        (r,c) = q.popleft()
        if (r,c) not in counts:
            continue
        final += 1
        del counts[(r,c)]
        for (dr,dc) in ns:
            if (r+dr,c+dc) not in counts:
                continue

            counts[(r+dr,c+dc)] -= 1
            if counts[(r+dr,c+dc)] < thresh:
                q.append((r+dr,c+dc))
    
    return init, final

if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename,'r') as f:
        grid = f.read().splitlines()
    

    print(clear(grid, 4))