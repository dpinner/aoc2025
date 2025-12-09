import sys
from math import prod

def solve(lines: list[str], op: list[str]) -> int:
    if not lines:
        return 0
    j = -1
    nums = []
    tot = 0
    for idx in range(len(lines[0])-1,-1,-1):
        cur = ''
        for line in lines:
            cur += line[idx] if line[idx] != ' ' else ''

        if cur == '':
            tot += sum(nums) if op[j] == '+' else prod(nums)
            nums = []
            j -= 1
        else:
            nums.append(int(cur))

    if nums:
        tot += sum(nums) if op[j] == '+' else prod(nums)
    return tot


if __name__ == "__main__":
    filename = sys.argv[1]
    lines = []
    operators = []
    with open(filename,'r') as f:
        lines = f.readlines()
        operators = lines[-1].rstrip().split()
        lines = [l.rstrip('\n\r') for l in lines[:-1]]

    # split on whitespace, transpose and map to integers
    operands = [list(map(int,row)) for row in zip(*(line.split() for line in lines))]
    tot1 = sum(sum(operands[i]) if op == '+' else prod(operands[i]) for i,op in enumerate(operators))

    tot2 = solve(lines, operators)
    print(tot1, tot2)