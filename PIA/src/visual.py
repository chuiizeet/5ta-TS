import sys
import json
import collections
import math


class ZipfLaw:

    def __init__(self, path=("dictionary.txt", "./data/wordcount.json")):
        # def __init__(self, path=("d2016.bin", "r")):
        self.N = 0
        self.p = {}
        self.A = 0

        try:
            self.path = sys.argv[1]
        except IndexError:
            self.path = path[0]

        try:
            self.jsonPath = sys.argv[2]
        except IndexError:
            self.jsonPath = path[1]

        self.essay = open(self.path, 'r')

        with open(self.path, 'r') as file:
            self.A = 682869

        self.wordCount = {}
        self.wordSplit()
        self.jsonifyDict()
        self.draw()

        self.essay.close()

    def wordSplit(self):
        wordList = self.essay.read().split()

        self.N = len(wordList)
        for word in wordList:
            if word.isalpha():
                if word in self.wordCount:
                    self.wordCount[word.lower()] += 1
                else:
                    self.wordCount[word.lower()] = 1

    def jsonifyDict(self):

        self.sortedWordCount = collections.OrderedDict(reversed(sorted(self.wordCount.items(), key=lambda t: t[1])))

        with open(self.jsonPath, 'w') as jsonData:
            json.dump(self.sortedWordCount, jsonData, ensure_ascii=False)

    def draw(self, WordsLimit=150):
        x = []
        y = []
        general = []

        for i in range(len(self.sortedWordCount)):
            milista = []
            x_val = list(self.sortedWordCount.items())[i][0]
            y_val = list(self.sortedWordCount.items())[i][1]
            x.append(x_val)
            y.append(y_val)
            milista.append(x_val)
            milista.append(y_val)
            general.append(milista)

        # Volumen del diccionario
        D = len(x)
        sumPi = 0

        for i in general:
            self.p.update({i[0]: (i[1] / self.N) / (general.index(i) + 1)})

        for key in self.p.keys():
            sumPi += self.p[key] * (-math.log(self.p[key], 10))

        sumFreq = 0
        for i in range(1, D):
            sumFreq += general[i][1] * (1 / i)

        print("Cantidad total de palabras en el diccionario:")
        print(self.N)
        print("Volumen del diccionario del Lenguaje Natural")
        print(D)
        print("Frecuencias:")
        print(general)
        print("Probabilidad de cada palabra (Pi):")
        print(self.p)
        print("Bajo la codificacion de Shanon B1 (Longitud del texto comprimido) es igual a:")
        B1 = self.N * sumPi
        print(round(B1, 4))
        tmp = B1
        print("Bajo la codificacion uniforme B1 (Longitud del texto comprimido) es igual a:")
        B2 = self.N * math.log(D, 10)
        print(round(B2, 4))

        print("Sumatoria Bakulina(7) frecuencias:")
        print(round(sumFreq, 4))

        B1_n1 = []
        for key in self.p.keys():
            sum = 0
            sum2 = 0
            sumD = 0
            for i in range(1, D):
                sumD += 1 / i
                sum += ((self.p[key] / i) * (math.log(i, 10) - math.log(self.p[key] + 1)))
                sum2 += ((math.log(i) / i) + (math.log(2) - math.log(self.p[key]) * sumD))
            if tmp < (self.N * sum):
                tmp = ((self.N * self.p[key]) / math.log(2)) * sum2
                if tmp < (self.N / math.log(2) * math.log(D + 1)) * (
                        (math.pow(math.log(D + 1), 2)) + -0.105 + (
                        math.log(2) + math.log(math.log(D + 1)) + 0.577) * (
                                math.log(D + 1) + 0.577)) and ((self.N / math.log(2) * math.log(D + 1)) *
                                                               ((math.pow(math.log(D + 1), 2) / 2)
                                                                + (-0.105) +
                                                                (math.log(2) + math.log(2) * math.log(D + 1) + (
                                                                        0.577 / math.log(D + 1))) * (
                                                                        math.log(D + 1) + 0.577))):
                    tmp = ((self.N / (math.log(2) * math.log(D + 1))) * (
                            (math.pow(math.log(D + 1), 2)) / 2) + 0.577 * (1 + math.log(2)) + (-0.105) + (
                                   math.log(2) * math.log(D + 1)) * (math.log(D + 1) + math.log(2)) + 0.577 * (
                                   math.log(2) * math.log(D + 1)) + (math.pow(0.577, 2) / math.log(D + 1)))

            B1_n1.append(tmp)
            tmp = B1
        print(B1_n1)


if __name__ == '__main__':
    ZipfLaw()
