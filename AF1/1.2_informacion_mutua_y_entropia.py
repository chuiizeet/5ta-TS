import numpy as np
from random import random

# Test del ejercicio del dado
# A = np.array([1/36,1/18,1/12,1/9,5/36,1/6,5/36,1/9,1/12,1/18,1/36])
A = np.array([])

def entropia_informacion():
    pA = A / A.sum()
    ent = -np.sum(pA*np.log2(pA))
    print("Entropia: {}".format(ent))

    total_values = len(A)

    info = -np.log10(1/total_values)
    print("Informacion mutua: {}".format(info))

def menu():

    global A

    print("\n----{}----\n".format(__file__))
    print("Que desea hacer: ")
    print("1)Valores random")
    print("2)Valores de entrada")

    option = input()
    # assert option
    assert option.isnumeric(), 'Opcion no valida'

    o = int(option)
    if o != 1 and o != 2:
        print('Opcion no valida'); return
    
    if o == 1: # Valores aleatorios
        A = np.random.uniform(-0,1,18)
        entropia_informacion()
    if o == 2:
        print("Ingrese las frecuencias separadas por coma: \n")
        f = input()
        narray = []
        for x in f.split(','):
            data = float(x)
            narray.append(data)
        
        A = np.array(narray)
        entropia_informacion()


if __name__ == "__main__":
    menu()