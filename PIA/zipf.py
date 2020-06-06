import sys

import src.visual as sv

try:
    sv.ZipfLaw()
except Exception as error:
    print("'dictionary.txt' el archivo a leer no debe estar vacío, asegurese de agregar palabras al diccionario")
    print("o")
    print(error)
finally:
    sys.exit()
