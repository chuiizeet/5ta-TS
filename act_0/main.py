import itertools
import numpy as np

_a = np.array([0,1,2,3])
_2 = np.array([4,5,6,7])
_3 = np.array([8,9,10,11])
_4 = np.array([12,13,14,15])
_5 = np.array([16,17,18,19])
_6 = np.array([20,21,22,23])
_7 = np.array([24,25,26,27])
_8 = np.array([28,29,30,31])
_9 = np.array([32,33,34,35])
_10 = np.array([36,37,38,39])
_j = np.array([40,41,42,43])
_q = np.array([44,45,46,47])
_k = np.array([48,49,50,51])

x = list(itertools.combinations(range(52), 5))
pears = [_a, _2, _3, _4, _5, _6, _7, _8, _9, _10, _j, _q, _k]
manos = []

for i in x:
	pares = 0
	for e,p in enumerate(pears):
		if np.setdiff1d(i,p).size == 3:
			pares += 1
			if pares == 2:
				manos.append(i)

print(manos)
print(len(manos))