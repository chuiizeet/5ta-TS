import sys

import src.visual as sv

try:
    sv.ZipfLaw(path=("dictionary1.txt", "./data/wordcount.json"))
    print(
        "------------------------------------------------------------------------------------------------------------")
    sv.ZipfLaw(path=("oil_bourse.txt", "./data/wordcount.json"))

    print("REFERENCES")
    print("http://www.mathnet.ru/links/c6d04548ffd7ea92149c511a1190b1f5/da511.pdf")
    print("http://www.mathnet.ru/php/archive.phtml?wshow=paper&jrnid=da&paperid=511&option_lang=eng")
    print("http://www.mathnet.ru/links/4b1d0d48883ed22d8716aed768a81949/da_511_refs_eng.pdf")
    print("(Application of the Zipf law to text compression) "
          "https://link.springer.com/article/10.1134/S1990478908040042")
except Exception as error:
    print(error)
finally:
    sys.exit()
