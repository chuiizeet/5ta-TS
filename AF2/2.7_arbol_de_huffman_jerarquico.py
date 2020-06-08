#2.7 Arbol de huffman jerarquico

from functools import total_ordering

@total_ordering
class Dot:
    def __init__(self, name, value):
        self.__name = name
        self.__value = value
        self.__code = ''

    def get_name(self):
        return self.__name

    def get_code(self):
        return self.__code

    def set_code(self, code):
        self.__code += str(code)

    def get_value(self):
        return self.__value

    def __eq__(self, other):
        if other is self.__class__:
            return True if self.get_value() == other.get_value() else False
        else:
            return True if self.get_value() == other else False

    def __le__(self, other):
        if other is self.__class__:
            return True if self.get_value() <= other.get_value() else False
        else:
            return True if self.get_value() <= other else False

    def __str__(self):
        return "{0} : {1} > {2}".format(self.get_name(), str(self.get_value()), str(self.get_code()[::-1]))

    def __iter__(self):
        return self


class Cont(Dot):
    def __init__(self, dot1, dot2):
        self.__dot1, self.__dot2 = dot1, dot2
        self.__value = self.__dot1.get_value() + self.__dot2.get_value()
        self.__verify()

    def get_value(self):
        return self.__value

    def __verify(self):
        if self.__dot1 < self.__dot2:
            self.__dot1.set_code(0)
            self.__dot2.set_code(1)
        elif self.__dot1 >= self.__dot2:
            self.__dot1.set_code(1)
            self.__dot2.set_code(0)

    def set_code(self, code):
        self.__dot1.set_code(code)
        self.__dot2.set_code(code)

    def __str__(self):
        return "{0}\n{1}".format(self.__dot1, self.__dot2)


def main():
    # Letras y frecuencoas
    l = list(map(lambda x: Dot(x[0], x[1]),
                 zip(('A', "B", 'C', 'D', 'E', 'F', 'G', 'H'), (0.5, 0.15, 0.12, 0.10, 0.04, 0.04, 0.03, 0.02))))

    while len(l) > 1:
        a = min(l)
        l.remove(a)
        b = min(l)
        l.remove(b)
        l.append(Cont(a, b))
    for c in l: print(c)
    return


if __name__ == "__main__": main()