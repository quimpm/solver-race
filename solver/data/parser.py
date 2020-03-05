from .literal import Literal
from .clause import Clause
from .formula import Formula

class Parser:

    def __init__(self, file_name):
        self.file_name = file_name

    def get_formula(self):
        formula = Formula()
        file = open(self.file_name)
        for line in file:
            formula.add_clause(list(map(lambda x: Literal.from_string(x), line.split())))
        return formula