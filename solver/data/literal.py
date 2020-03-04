class Literal:

    def __init__(self, num_variable: int, value: bool):
        self.__num_variable = num_variable
        self.__value = value

    def get_id(self):
        return self.__num_variable

    def get_value(self):
        return self.__value

    def __str__(self):
        return f'{self.__num_variable}'

    def __le__(self, other):
        return self.__num_variable <= other.get_value()

    def __ge__(self, other):
        return self.__num_variable >= other.get_value()

    def __eq__(self, other):
        return self.__num_variable == other.get_value()

    def __lt__(self, other):
        return not self.__ge__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def from_string(req: str):
        return Literal(abs(int(req)), int(req) > 0)
