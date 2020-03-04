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

    @staticmethod
    def from_string(req: str):
        return Literal(abs(int(req)), int(req) > 0)
