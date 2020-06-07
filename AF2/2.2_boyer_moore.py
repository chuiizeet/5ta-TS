import random
import string

NO_OF_CHARS = 256

def randomTxt(stringLength=32):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def randomPath(stringLength=4):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

  
def badCharRule(string, size): 

    badChar = [-1]*NO_OF_CHARS 
  
    for i in range(size): 
        badChar[ord(string[i])] = i 
  
    return badChar 
  
def search(txt, pat): 

    m = len(pat) 
    n = len(txt) 
  

    badChar = badCharRule(pat, m)  
  
    s = 0
    while(s <= n-m): 
        j = m-1
  

        while j>=0 and pat[j] == txt[s+j]: 
            j -= 1

        if j<0: 
            print("Pattern occur at shift = {}".format(s)) 
  
            s += (m-badChar[ord(txt[s+m])] if s+m<n else 1) 
        else: 
            s += max(1, j-badChar[ord(txt[s+j])]) 
  
  
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
		search(txt, pat)

	if o == 2:
		print("Ingrese el diccionario de entrada: \n")
		txt = input()
		print("Ingrese el patron que desea buscar: \n")
		pat = input()
		search(txt, pat)


if __name__ == "__main__":
	menu()

  