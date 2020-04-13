from solver.data.formula import Formula


class SAT(object):

    def __init__(self, formula):
        self.formula: Formula = formula
        self.num_lits: int = formula.get_num_lits()

    def get_random_interpretation(self):
        raise NotImplementedError
