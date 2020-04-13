from typing import List

from solver.data.literal import Literal


class Clause:

    def __init__(self, lits: List[Literal]):
        self.__lits = lits

    def __str__(self):
        ' '.join(map(str, self.__lits))

    def satisfyes(self, interpretation: List[int]) -> bool:

        pass
