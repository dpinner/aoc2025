import sys
import numpy as np
from scipy.optimize import LinearConstraint, milp

def presses(n: int, buttons: set[int], cache: dict[int,int]) -> int:
    if n == 0:
        return 0
    
    if n in cache:
        return cache[n]
    
    min_presses = len(buttons)+1
    for b in buttons:
        min_presses = min(min_presses, 1 + presses(n ^ b, buttons - {b}, cache))

    cache[n] = min_presses

    return cache[n]

def joltage(target: list[int], buttons: list[list[int]]) -> float:
    
    A = np.array(buttons).T

    res = milp(c=np.ones(len(buttons)), constraints=LinearConstraint(A, target, target), integrality=np.ones(len(buttons)))

    return sum(res.x)
    


if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = f.read().splitlines()

    tot1 = 0
    tot2 = 0
    for line in lines:
        x = line.split()
        n = int(''.join('0' if c == '.' else '1' for c in x[0][1:-1]),2)
        d = len(x[0][1:-1])
        int_buttons = set()
        bit_buttons = []
        for button in x[1:-1]:
            bit_array = ['0']*d
            indices = button[1:-1].split(',')
            for idx in indices:
                bit_array[int(idx)] = '1'

            int_buttons.add(int(''.join(bit_array), 2))
            bit_buttons.append([int(i) for i in bit_array])

        target = [int(t) for t in x[-1][1:-1].split(',')]

        tot1 += presses(n,int_buttons,{})
        tot2 += joltage(target, bit_buttons)

    print(tot1, tot2)