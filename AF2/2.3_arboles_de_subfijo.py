from suffix_trees import STree
import random
import string

def randomTxt(stringLength=72):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def randomPath(stringLength=1):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def arbol(txt, findTxt):

    st = STree.STree(txt)
    first = st.find(findTxt)
    print("El primer patron se encuentra en la posicion: {}".format(first))
    all = st.find_all(findTxt)
    print("Todas las posiciones: {}".format(all))

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
		txt = randomTxt()
		find = randomPath()
		arbol(txt, find)

	if o == 2:
		print("Ingrese el diccionario de entrada: \n")
		txt = input()
		print("Ingrese el patron que desea buscar: \n")
		find = input()
		arbol(txt, find)


if __name__ == "__main__":
	menu()
