#!/usr/bin/env python3
import sys
import random

global formula
global num_vars
global not_finded


def get_rnd_interpretation():
    inter = [random.choice([-1, 1]) * (x + 1) for x in range(num_vars)]
    for lit in not_finded:
        inter[abs(lit) - 1] = -lit
    return inter


def get_formula(file_name):
    global formula
    global num_vars
    global not_finded
    with open(file_name) as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if line[0] == 'p':
                num_vars = int(line.split()[2])
                index_line = i
                break
        formula = [[] for _ in range(num_vars + num_vars + 1)]
        for i, clause in enumerate(lines[index_line + 1:]):
            for lit in clause.split()[:-1]:
                formula[int(lit)].append(i)
        not_finded = []
        for i, lit in enumerate(formula[1:num_vars + 1]):
            if not lit:
                not_finded.append(i + 1)
        for i, lit in enumerate(formula[num_vars + 1:]):
            if not lit:
                not_finded.append(-i - 1)


def main():
    if len(sys.argv) != 2:
        sys.exit()
    else:
        get_formula(sys.argv[1])
    print(formula)
    interpretation = get_rnd_interpretation()
    print(interpretation)


if __name__ == '__main__':
    main()
