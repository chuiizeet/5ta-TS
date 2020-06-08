# 2.5 Shannon Fano 

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


def run(S):
    if isprefixcode(S):
        print("{} is a prefix code.".format(S))
    else:
        print("{} is not a prefix code.".format(S))

def split(probability, sorted_symbols):
    split_point = 1
    min_diff = float('inf')
    for i in range(1, len(sorted_symbols)-1):
        left = sum(probability[k] for k in sorted_symbols[:i])
        right = sum(probability[k] for k in sorted_symbols[i:])
        diff = abs(left-right)
        if diff < min_diff:
            split_point = i
            min_diff = diff
    return split_point


def assign_digit(code, symbols, digit):
    for symbol in symbols:
        code.setdefault(symbol, "")
        code[symbol] += digit
    return code


def shannon_fano_(probability, sorted_symbols, code={}):
    if len(sorted_symbols) == 1:
        return code

    split_point = split(probability, sorted_symbols)
    L = sorted_symbols[split_point:]
    R = sorted_symbols[:split_point]

    assign_digit(code, L, "1")
    code = shannon_fano_(probability, L, code)

    assign_digit(code, R, "0")
    code = shannon_fano_(probability, R, code)

    return code


def shannon_fano(probability):
    return shannon_fano_(probability, sort_symbols(probability))


def test_shannon_fano():
    occurrences = {"A": 15, "B": 7, "C": 6, "D": 6, "E": 5}
    probability = {}
    for symbol in occurrences.keys():
        probability[symbol] = occurrences[symbol] / sum(occurrences.values())

    code = shannon_fano(probability)

    expected1 = {"A": "00", "B": "01", "C": "10", "D": "110", "E": "111"}
    expected2 = {"A": "00", "B": "01", "C": "110", "D": "10", "E": "111"}
    assert(code == expected1 or code == expected2)
    assert(isprefixcode(code))


if __name__ == '__main__':
    test_shannon_fano()