#!/usr/bin/env python3
import sys
import random
from functools import reduce

#num_restart, num_flips, num_gsat_choice, num_walk_choice, num_gsat_local, generated_inter = 0, 0, 0, 0, 0, []

class FracaSAT(object):

    def __init__(self, formula, num_vars, not_found, num_clauses, clauses):
        self.clauses = clauses
        self.num_first_clauses = num_clauses
        self.num_clauses = num_clauses
        self.not_found = not_found
        self.num_vars = num_vars
        self.formula = formula


def get_rnd_interpretation(fracaSAT):
    inter = [random.choice([-1, 1]) * (x + 1) for x in range(fracaSAT.num_vars)]
    for lit in fracaSAT.not_found:
        inter[abs(lit) - 1] = -lit
    return inter


def calculate_clauses_cost(fracaSAT, inter):
    cost_clauses = [0 for _ in range(fracaSAT.num_clauses)]
    for i, c in enumerate(fracaSAT.clauses):
        for lit in c:
            cost_clauses[i] += 1 if lit == inter[abs(lit) - 1] else 0
            if cost_clauses[i] >= 2:
                break
    return cost_clauses


def satisfies(cost_clauses):
    return all(map(lambda x: x > 0, cost_clauses))


def find_unsat_clause(cost_clauses):
    return random.choice(list(filter(lambda x: x[1] == 0, enumerate(cost_clauses))))[0]


def find_all_unsat_clauses(vars, fracasat, current_clauses_cost):
    unsat_clauses = []
    for var in vars:
        i = 0
        var_clauses = fracasat.formula[-var]
        for clause in var_clauses:
            if current_clauses_cost[clause] == 1:
                i += 1
        unsat_clauses.append([var, i])
    return unsat_clauses


def find_actual_cost(cost_clauses):
    return len(list(filter(lambda x: x == 0, cost_clauses)))


def find_best_flipped_vars(inter, cost_clauses, fracasat):
    best_vars = []
    for var in inter:
        cost = calculate_flipped_cost(var, fracasat.formula, cost_clauses)
        if cost > 0:
            best_vars.append(var)
    return best_vars


def calculate_flipped_cost(var, formula, cost_clauses):
    change_var = get_critical_clauses(formula[-var], cost_clauses, 0)
    actual_var_cost = get_critical_clauses(formula[var], cost_clauses)
    return len(change_var) - len(actual_var_cost)


def get_critical_clauses(clauses, cost_clauses, cost=1):
    return list(filter(lambda x: cost_clauses[x] == cost, clauses))


def solver_structure(fracasat, algorithm, prob):
    while True:
        inter = get_rnd_interpretation(fracasat)
        for j in range(fracasat.num_clauses * 10):
            cost_clauses = calculate_clauses_cost(fracasat, inter)
            if satisfies(cost_clauses):
                return inter
            algorithm(inter, cost_clauses, fracasat, prob)


def add_all_unsat_clause(fracasat, cost_clause):
    unsat_lits = reduce(lambda x, y: set(x).union(y),
                        map(lambda c: fracasat.clauses[c], filter(lambda x: x == 0, cost_clause)))
    fracasat.clauses.append(list(unsat_lits))
    for lit in unsat_lits:
        fracasat.formula[lit].append(fracasat.num_clauses - 1)
    fracasat.num_clauses += 1


def add_twice_unsat_clause(fracasat, cost_clause):
    unsat_cl = find_unsat_clause(cost_clause)
    fracasat.clauses.append(fracasat.clauses[unsat_cl])
    for lit in fracasat.clauses[unsat_cl]:
        fracasat.formula[lit].append(fracasat.num_clauses - 1)
    fracasat.num_clauses += 1


def add_new_clause_inter(fracasat, inter):
    fracasat.num_clauses += 1
    new_clause = list(map(lambda x: -x, inter))
    fracasat.clauses.append(new_clause)
    for lit in new_clause:
        fracasat.formula[lit].append(fracasat.num_clauses - 1)


def gsat(inter, cost_clauses, fracasat, prob):
    vars = find_best_flipped_vars(inter, cost_clauses, fracasat)
    if not vars:
        #heuristic_stats_gsat(cost_clauses, fracasat, inter, prob)
        substitute = random.choice(fracasat.clauses[find_unsat_clause(cost_clauses)])
    else:
        substitute = random.choice(vars)
    inter[abs(substitute) - 1] = -substitute


def heuristic_stats_gsat(cost_clauses, fracasat, inter, prob):
    global num_gsat_local, generated_inter
    num_gsat_local += 1
    if inter not in generated_inter:
        generated_inter.append(inter)
    if random.random() > prob and fracasat.num_first_clauses * 1.2 > fracasat.num_clauses:
        add_all_unsat_clause(fracasat, cost_clauses)


def walk_sat(inter, cost_clauses, fracasat, prob):
    clause_unsat = find_unsat_clause(cost_clauses)
    vars = fracasat.clauses[clause_unsat]
    unsat_var_clauses = find_all_unsat_clauses(vars, fracasat, cost_clauses)
    broken_var, num_broken_clauses = min(unsat_var_clauses, key=lambda x: x[1])
    if num_broken_clauses > 0 and random.random() < prob:
        substitute = -random.choice(vars)
    else:
        substitute = broken_var
    inter[abs(substitute) - 1] = substitute


def random_walk_gsat(inter, cost_clauses, fracasat, prob):
    #global num_walk_choice, num_gsat_choice
    current_prob = random.random()
    if current_prob <= prob:
        #num_walk_choice += 1
        unsat_lit = random.choice(fracasat.clauses[find_unsat_clause(cost_clauses)])
        inter[abs(unsat_lit) - 1] = -inter[abs(unsat_lit) - 1]
    else:
        #num_gsat_choice += 1
        gsat(inter, cost_clauses, fracasat, 0.8)


def get_formula(file_name):
    with open(file_name) as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if line[0] == 'p':
                num_vars, num_clauses = map(int, line.split()[2:])
                index_line = i
                break
        formula = [[] for _ in range(num_vars + num_vars + 1)]
        for i, clause in enumerate(lines[index_line + 1:]):
            if not clause[0].__eq__('c'):
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
    global max_flips
    #global num_restart, num_flips, num_gsat_choice, num_walk_choice, num_gsat_local, generated_inter
    if len(sys.argv) < 2:
        sys.exit()
    else:
        fracaSAT = get_formula(sys.argv[1])
    # inter = solver_structure(500, fracaSAT, gsat, 0)
    # inter = solver_structure(500, fracaSAT, walk_sat, 0.5)
    inter = solver_structure(fracaSAT, random_walk_gsat, 0.5)
    if inter != None:
        print('s SATISFIABLE')
        print('v', ' '.join(map(str, inter)), 0)
        """print('==========')
        print(f'\tNUM RESTART: {num_restart}')
        print(f'\tNUM FLIPS: {num_flips}')
        print(f'\tNUM GSAT CHOICE: {num_gsat_choice}')
        print(f'\tNUM WALK CHOICE: {num_walk_choice}')
        print(f'\tNUM LOCAL GSAT FLIP: {num_gsat_local}')
        print(f'\tNUM_LOCAL_MIN {len(generated_inter)}')
        print(f'\tNUM TOTAL CLAUSES {fracaSAT.num_clauses}')
        print('==========')"""
    else:
        print('UNSATISFIABLE')


if __name__ == '__main__':
    main()
