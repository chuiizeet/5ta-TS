import sys

import src.visual as sv

try:
    sv.ZipfLaw()
except Exception as error:
    print(error)
finally:
    sys.exit()
