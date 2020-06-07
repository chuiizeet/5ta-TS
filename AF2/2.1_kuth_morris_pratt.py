import random
import string

def randomTxt(stringLength=32):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def randomPath(stringLength=4):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def KMPSearch(pat, txt): 
	M = len(pat) 
	N = len(txt) 
  
	lps = [0]*M 
	j = 0 
  
	LPSArray(pat, M, lps) 
  
	i = 0 
	while i < N: 
		if pat[j] == txt[i]: 
			i += 1
			j += 1
  
		if j == M: 
			print ("Found pat at index " + str(i-j)) 
			j = lps[j-1] 
  
		elif i < N and pat[j] != txt[i]: 

			if j != 0: 
				j = lps[j-1] 
			else: 
				i += 1
  
def LPSArray(pat, M, lps): 
	len = 0 
  
	lps[0] 
	i = 1

	while i < M: 
		if pat[i]== pat[len]: 
			len += 1
			lps[i] = len
			i += 1
		else: 

			if len != 0: 
				len = lps[len-1] 
  
			else: 
				lps[i] = 0
				i += 1
  

  
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
	
	if o == 1:
		txt = randomPath()
		pat = randomPath()
		KMPSearch(pat, txt)

	if o == 2:
		print("Ingrese el diccionario de entrada: \n")
		txt = input()
		print("Ingrese el patron que desea buscar: \n")
		pat = input()
		KMPSearch(pat, txt) 


if __name__ == "__main__":
	menu()
