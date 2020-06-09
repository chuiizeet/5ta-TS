import sys
import json
import collections
from collections import Counter
import math


class ZipfLaw:

    def __init__(self, path=("", "./data/wordcount.json")):
        self.TotalWords = 0
        self.Frequencies = {}
        self.fileSize = 0

        try:
            self.path = sys.argv[1]
        except IndexError:
            self.path = path[0]

        self.essay = open(self.path, 'r')
        data = self.essay.read()
        wordList = data.split()
        self.Frequencies = Counter(wordList)
        print("===========================================================================================")
        print("||                                   1. THE ZIPF LAW                                     ||")
        print("===========================================================================================")
        print("Palabras con frecuencias ordenadas de menor a mayor")
        print(self.Frequencies)
        self.fileSize = data.__sizeof__()
        self.TotalWords = len(wordList)
        self.DictionaryVolume = len(self.Frequencies.keys())
        self.draw()
        self.essay.close()

    def draw(self, WordsLimit=150):
        probabilities = {}
        self.Frequencies = {k: v for k, v in reversed(sorted(self.Frequencies.items(), key=lambda item: item[1]))}

        C = 0
        for i in range(1, self.DictionaryVolume):
            C += 1 / i
        C = 1 / C

        count = 1
        for key in self.Frequencies.keys():
            probabilities.update({key: C / count})
            count += 1

        sumPi = 0
        for key in probabilities.keys():
            sumPi += probabilities[key] * (-math.log10(probabilities[key]))

        print("Cantidad total de palabras en el texto:")
        print(self.TotalWords)
        print("Longitud inicial del texto")
        print(self.fileSize, "bytes")
        print("Volumen del diccionario del Lenguaje Natural (Cantidad total de palabras diferentes)")
        print(self.DictionaryVolume)
        print("Nueva Constante")
        print(C)
        print("Probabilidades")
        print(probabilities)
        print("===========================================================================================")
        print("||          2.-CODING WORDS, UNIFORMLY AND NONUNIFORMLY WITH RESPECT TO OUTPUT           ||")
        print("===========================================================================================")
        print("Bajo la codificacion de Shannon B1 (Longitud del texto comprimido) es igual a:")
        B1 = self.TotalWords * sumPi
        print(round(B1, 4), "bits")
        print("Bajo la codificacion uniforme B2 (Longitud del texto comprimido) es igual a:")
        B2 = self.TotalWords * math.log10(self.DictionaryVolume)
        print(round(B2, 4), "bits")
        B1final = 0
        # for key in self.Frequencies.keys():
        #     sum = 0
        #     sum2 = 0
        #     sumD = 0
        #     for i in range(1, self.DictionaryVolume):
        #         sumD += 1 / i
        #         sum += ((self.Frequencies[key] / i) * (math.log(i, 10) - math.log(self.Frequencies[key] + 1)))
        #         sum2 += ((math.log(i) / i) + (math.log(2) - math.log(self.Frequencies[key]) * sumD))
        #         if B1final < (self.TotalWords * sum):
        #             B1final = ((self.TotalWords * self.Frequencies[key]) / math.log(2)) * sum2
        #             if B1final < (self.TotalWords / math.log(2) * math.log(self.DictionaryVolume + 1)) * (
        #                     (math.pow(math.log(self.DictionaryVolume + 1), 2)) + -0.105 + (
        #                     math.log(2) + math.log(math.log(self.DictionaryVolume + 1)) + 0.577) * (
        #                             math.log(self.DictionaryVolume + 1) + 0.577)) and (
        #                     (self.TotalWords / math.log(2) * math.log(self.DictionaryVolume + 1)) *
        #                     ((math.pow(math.log(self.DictionaryVolume + 1), 2) / 2)
        #                      + (-0.105) +
        #                      (math.log(2) + math.log(2) * math.log(self.DictionaryVolume + 1) + (
        #                              0.577 / math.log(self.DictionaryVolume + 1))) * (
        #                              math.log(self.DictionaryVolume + 1) + 0.577))):
        #                 B1final = ((self.TotalWords / (math.log(2) * math.log(self.DictionaryVolume + 1))) * (
        #                         (math.pow(math.log(self.DictionaryVolume + 1), 2)) / 2) + 0.577 * (1 + math.log(2)) + (
        #                                -0.105) + (
        #                                    math.log(2) * math.log(self.DictionaryVolume + 1)) * (
        #                                    math.log(self.DictionaryVolume + 1) + math.log(2)) + 0.577 * (
        #                                    math.log(2) * math.log(self.DictionaryVolume + 1)) + (
        #                                    math.pow(0.577, 2) / math.log(self.DictionaryVolume + 1)))

        print("b1 final")
        print(B1final)

        n1 = B1 / self.fileSize
        n2 = B2 / self.fileSize
        bitsTotales = self.fileSize * 8
        print("Coeficientes de compresión")
        print("n1")
        print(n1, "bits")
        print("n2")
        print(n2, "bits")
        print("Validacion de desigualdades expresadas en el teorema "
              "n1/n2 = B1/B2 < ln(D + 1) 2ln D + c1 · (1 + ln 2) + c2 ln(D + 1) · "
              "ln D + ln ln(D + 1) ln D + ln ln(D + 1) · (ln 2 + c1) ln(D + 1) · ln D")
        print(B1 / B2)
        print(n1 / n2)
        print("n1 (%)")
        print((B1 / self.fileSize) * 100)
        print("n2 (%)")
        print((B2 / self.fileSize) * 100)

        print("===========================================================================================")
        print("||                           3. THE SINGLE-PASS COMPRESSION SCHEME                       ||")
        print("===========================================================================================")

        count = 1
        li = {}
        for key in self.Frequencies.keys():
            if key not in li.keys():
                a = 1 / math.log(self.DictionaryVolume)
                li.update({key: -math.log10((a / count))})
                count += 1

        Ksp = 0
        for key in li:
            Ksp += li[key]

        print(li)
        print(Ksp)
        print(((Ksp * 8) / self.fileSize) * 100)


if __name__ == '__main__':
    ZipfLaw()
