import itertools

A = ['#', '&', '!', '?', '+']
B = ['#', '&&', '!!', '???', '++++']
L = 8

_BResults = []

def getAllBResults():
	global _BResults, L
	for i in range(0,L):
		_BResults += itertools.product(B, repeat=i+1)

def getAllAResults(n):
	return list(itertools.product(A, repeat=n))

def process():
	global L, _BResults
	getAllBResults()

	for i in range(0,L):
		print('L:',i+1,'\n')

		# A
		aData = getAllAResults(i+1)
		# print('A:',aData,'\n')

		# nA
		print('nA:',len(aData),'\n')

		#B
		bData = []
		for j in _BResults:
			l = sum(len(w) for w in j)
			if l == i+1:
				bData.append(j)
		# print('B:',bData,'\n')

		# nB
		print('nB:',len(bData),'\n')

		print('----------------------------------------\n\n')
		

process()