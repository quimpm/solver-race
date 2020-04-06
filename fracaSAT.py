#!/usr/bin/env python3
import sys
import random
import numpy


class FracaSAT(object):

    def __init__(self, formula, num_vars, not_found, num_clauses, clauses):
        self.clauses = clauses
        self.num_clauses = num_clauses
        self.not_found = not_found
        self.num_vars = num_vars
        self.formula = formula


def get_rnd_interpretation(fracaSAT):
    cost_clauses = [0 for _ in range(fracaSAT.num_clauses)]
    inter = [random.choice([-1, 1]) * (x + 1) for x in range(fracaSAT.num_vars)]
    for lit in fracaSAT.not_found:
        inter[abs(lit) - 1] = -lit
    for lit in inter:
        for c in fracaSAT.formula[lit]:
            cost_clauses[c] += 1
    return inter, cost_clauses


def satisfies(cost_clauses):
    return all(map(lambda x: x > 0, cost_clauses))


def find_unsat_clause(cost_clauses):
    return random.choice(list(filter(lambda x: x[1] == 0, enumerate(cost_clauses))))[0]

def find_all_unsat_clauses(cost_clauses, vars, clauses):
    return [ [var, list(map(lambda x : x[0], filter(lambda x: x[1] == 0 and (var in clauses[x[0]]), enumerate(cost_clauses))))] for var in vars ]

def walk_sat(max_tries, max_flips, fracasat):
    for i in range(max_tries):
        inter, cost_clauses = get_rnd_interpretation(fracasat)
        print(inter)
        print(cost_clauses)
        for j in range(max_flips):
            if satisfies(cost_clauses):
                return inter
            clause_unsat = find_unsat_clause(cost_clauses)
            vars = fracasat.clauses[clause_unsat]
            unsat_var_clauses = find_all_unsat_clauses(cost_clauses, vars, fracasat.clauses)
            broken = min(unsat_var_clauses, key = lambda x : len(x[1]))
            

def get_formula(file_name) -> FracaSAT:
    with open(file_name) as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if line[0] == 'p':
                num_vars, num_clauses = map(int, line.split()[2:])
                index_line = i
                break
        formula = [[] for _ in range(num_vars + num_vars + 1)]
        for i, clause in enumerate(lines[index_line + 1:]):
            for lit in clause.split()[:-1]:
                formula[int(lit)].append(i)
        clauses = [list(map(int, c.split()[:-1])) for c in lines[index_line + 1:]]
        not_found = []
        for i, lit in enumerate(formula[1:num_vars + 1]):
            if not lit:
                not_found.append(i + 1)
        for i, lit in enumerate(formula[num_vars + 1:]):
            if not lit:
                not_found.append(-i - 1)
        return FracaSAT(formula, num_vars, not_found, num_clauses, clauses)


def main():
    if len(sys.argv) != 2:
        sys.exit()
    else:
        fracaSAT = get_formula(sys.argv[1])
    debug = True
    if debug:
        print('FORMULA:', fracaSAT.formula)
        print('NUM_VARS:', fracaSAT.num_vars)
        print('NOT_FOUND:', fracaSAT.not_found)
        print('NUM_CLAUSES:', fracaSAT.num_clauses)
        print('CLAUSES:', fracaSAT.clauses)
        interpretation, cost_clauses = get_rnd_interpretation(fracaSAT)
        print('RNDM INTERPRETATION:', interpretation)
        print('COST OF EACH CLAUSES:', cost_clauses)
        print('DOES IT SATISFY?', satisfies(cost_clauses))
    walk_sat(1, 1, fracaSAT)


if __name__ == '__main__':
    main()
