import itertools, operator
from Input_Module.input import console
import numpy


def combinaciones(p: [str], L: int):
    # p = ['#', '$$', '%%', '@@@', '!!!!']

    c = []

    lst = []

    # L = 8

    sl = len(p[0])
    for e in p:
        if len(e) < sl:
            sl = len(e)

    N = L / sl

    for n in range(1, int(N + 1)):
        for cuts in itertools.combinations_with_replacement(range(n + 1), len(p) - 1):
            lst.append(list(map(operator.sub, cuts + (n,), (0,) + cuts)))

    for e in lst:
        l = 0
        for i in range(len(e)):
            l += e[i] * len(str(p[i]))
        if 0 < l < L + 1:
            x = []
            for i in range(len(e)):
                if e[i] > 0:
                    for j in range(e[i]):
                        x.append(p[i])
            c.append([x, l])

    groups = []
    for e in range(L):
        groups.append([])

    for e in c:
        e.append(set(itertools.permutations(e[0])))
        for x in e[2]:
            s = ''
            for y in x:
                s += y
            if 0 < len(s) < L + 1:
                if s not in groups[len(s) - 1]:
                    groups[len(s) - 1].append(s)

    n = []

    for g in groups:
        # print(len(g[0]))
        # print(len(g))
        n.append(len(g))

    return n


while True:
    print("Ingrese el diccionario de entrada")
    in_dict = []
    while True:
        x = console(3, 'Ingrese el valor de entrada: ')
        if x == '':
            break
        if x not in in_dict:
            in_dict.append(x)
        else:
            print('El valor \'' + x + '\' ya se registró anteriormente. Por favor ingrese un valor distinto.')
    if len(in_dict) > 0:
        break

while True:
    print("Ingrese el diccionario de salida")
    out_dict = []
    while True:
        x = console(3, 'Ingrese el valor de salida: ')
        if x == '':
            break
        if x not in out_dict:
            out_dict.append(x)
        else:
            print('El valor \'' + x + '\' ya se registró anteriormente. Por favor ingrese un valor distinto.')
    if len(out_dict) > 0:
        break

while True:
    l = console(1, "Ingrese la longitud del mensaje: ")
    if l != '' and l > 0:
        break

x = []
for i in range(l):
    x.append(i + 1)

y_in = combinaciones(in_dict, l)
y_out = combinaciones(out_dict, l)

print()
print(x, '\n' + str(y_in), '\n' + str(y_out))
print()

a = numpy.polyfit(x, y_in, 3, rcond=None, full=False)
b = numpy.polyfit(x, y_out, 3, rcond=None, full=False)

print(a, ':', b)
