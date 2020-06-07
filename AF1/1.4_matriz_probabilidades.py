import numpy as np
from random import randint

def probabilidades(transitions):
	n = 3 
	M = [[0]*n for _ in range(n)]

	for (i,j) in zip(transitions,transitions[2:]):
		M[i-1][j-1] += 1

	for row in M:
		s = sum(row)
		if s > 0:
			row[:] = [f/s for f in row]
	return M
def menu():

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
		sample = []
		for i in range(0,randint(5,6)):
			sample.append(randint(0,3))
		print(np.array(probabilidades(sample)))
	if o == 2:
		print("Ingrese las probabilidades separadas por coma: \n")
		f = input()
		narray = []
		for x in f.split(','):
			data = int(x)
			narray.append(data)
		
		print(np.array(probabilidades(narray)))


if __name__ == "__main__":
	menu()