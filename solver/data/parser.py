from .literal import Literal
from .clause import Clause
from .formula import Formula


class Parser:

    def __init__(self, file_name):
        self.file_name = file_name

    def get_formula(self):
        with open(self.file_name) as file:
            index_line, num_vars = 0, 0
            lines = file.readlines()
            print(lines)
            for i, line in enumerate(lines):
                if line[0] == 'p':
                    num_vars = line.split()[2]
                    index_line = i
                    break
            print(num_vars)
            formula = Formula(int(num_vars))
            for i, line in enumerate(lines[index_line+1:]):
                formula.add_clause(list(map(lambda x: Literal.from_string(x), line.split()))[:-1], i)
            return formula
