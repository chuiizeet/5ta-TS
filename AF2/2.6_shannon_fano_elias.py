from math import log2, ceil

def sort_symbols(probability):
    symbols = probability.keys()
    return sorted(symbols, key=lambda k: probability[k], reverse=True)

def dangling_suffixes(code1, code2):
    def suffixes(code, word):
        N = len(word)
        s = set()
        for c in code:
            if c == word:
                continue
            if c.startswith(word):
                s.add(c[N:])
        return s

    ss = set()
    for c1 in code1:
        ss |= suffixes(code2, c1)
    for c2 in code2:
        ss |= suffixes(code1, c2)
    return ss


def isprefixcode(code):
    S0 = set(code)
    S = dangling_suffixes(S0, S0)
    D = dangling_suffixes(S0, S)

    while S != (S | D):
        S = S | D
        D = dangling_suffixes(S0, S)
    return len(S & S0) == 0


def shannon_fano_elias(probability, sort_symbols=False):
    symbols = list(probability.keys())

    # sort symbols for execution stability
    if sort_symbols:
        symbols.sort()

    def F(i):
        a = sum(probability[k] for k in symbols[:i])
        b = probability[symbols[i]] / 2
        return a + b

    def L(symbol):
        p = probability[symbol]
        return ceil(-log2(p)) + 1

    def Z(x, n):
        x = round(x, 7)  # avoid rounding error
        assert(0 <= x <= 1)
        if x == 1:
            return '0' * n

        z = ''
        for i in range(1, n+1):
            if x >= pow(2, -i):
                x -= pow(2, -i)
                z += '1'
            else:
                z += '0'
        return z

    return {symbol: Z(F(i), L(symbol)) for i, symbol in enumerate(symbols)}


def test_shannon_fano_elias():
    probability = {"A": 1/3, "B": 1/4, "C": 1/6, "D": 1/4}
    code = shannon_fano_elias(probability, sort_symbols=True)
    expected = {"A": "001", "B": "011", "C": "1010", "D": "111"}
    assert(code == expected)
    assert(isprefixcode(code))


if __name__ == '__main__':
    test_shannon_fano_elias()