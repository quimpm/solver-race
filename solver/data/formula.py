from typing import List

from solver.data.literal import Literal


class Formula:

    def __init__(self, num_vars):
        self.clauses = [[] for _ in range(num_vars*2 + 1)]

    def add_clause(self, clause: List[Literal], index_clause):
        for lit in clause:
            self.clauses[lit.get_var()].append(index_clause)
