import math
import os
import pickle

class precompute:

    def __init__(self):
        f = open("beep/case.txt", "r")
        real = []
        for x in f:
            var = x.split(' ', 1)[0]
            if var.isalnum():
                if len(var) == 5:
                    real.append(var)
                
        self.guessList = real
        self.words = real
        self.wordIndex = self.precomputeIndex()
        self.responses = self.precomputeReponse()
        self.distribution = self.precomputeDistribution()


    def precomputeIndex(self):
        #words uses a number to bind to a word
        #indexs uses a word to bind the same number
        return {"words": {x: i for i, x in enumerate(self.words)},
                "indexs":  {i: x for i, x in enumerate(self.words)}

                }
    
    def precomputeReponse(self):
        #Text file path
        outputPath = "precomputeResponses.txt"
        #make a list of reponses
        responses = {i: {} for i in range(len(self.guessList))}
        #if file exist, open the file and read the line
        if os.path.exists(outputPath):


                with open(outputPath) as f:
                    for line in f.readlines():

                        guessIndex, targetIndex, perm = line.strip().split("\t")
                        responses[int(guessIndex)][int(targetIndex)] = perm
        elif os.path.exists("data.pickle"):
                with open('data.pickle', 'rb') as f:
                    responses = pickle.load(f)
        else:
            li = self.guessList
            with open(outputPath, "w") as f:
                for i, guess in enumerate(li):
                    for j, target in enumerate(self.words):

                        responses[i][j] = self.pattern(guess, target)
                        f.write("\t".join([str(i), str(j), responses[i][j]]) + "\n")


                with open('precomputeResponses.pickle', 'wb') as f:
                    pickle.dumpS(responses, f)

        return responses

    def precomputeDistribution(self):
        outputPath = "precomputeDistribution.txt"
        if os.path.exists(outputPath):
            distribution = {i: {} for i in self.responses}
            with open(outputPath) as f:
                for line in f.readlines():
                    i, response, count = line.strip().split("\t")
                    distribution[int(i)][response] = int(count)
        else:

            distribution = {}
            for i in self.responses:
                distribution[i] = {}
                for w in self.words:
                    j = self.wordIndex["words"][w]
                    response = self.responses[i][j]
                    if response not in distribution[i]:
                        distribution[i][response] = 0
                    distribution[i][response] += 1

            with open(outputPath, "w") as f:
                for i in self.responses:
                    for response in distribution[i]:
                        f.write("\t".join([str(i), response, str(distribution[i][response])]) + "\n")
                print("{} saved.".format(f.name))

        return distribution



    def pattern(self, guess, target):
        #turn guess word and target word into pattern for wordle, where 0 mean grey, 1 mean yellow and 2 mean green
        targetDict = {}
        for x in target:
            if x not in targetDict:
                targetDict[x] = 0
            targetDict[x] += 1

        response = ['0'] * len(guess)

        for i, (g, t) in enumerate(zip(guess, target)):
            if g == t:
                response[i] = "2"
                targetDict[g] -= 1

        for i, (g, t) in enumerate(zip(guess, target)):
            if g != t:
                if g in targetDict and targetDict[g] > 0:
                    response[i] = "1"
                    targetDict[g] -= 1

        return "".join(response)

    def computeScore(self, word):

        wordIndex = self.wordIndex["words"][word]
        total = sum(self.distribution[wordIndex].values())
        score = 0.0
        for x in self.distribution[wordIndex].values():
            px = x * 1.0 / total
            score += -px * math.log(px)

        return score
if __name__ == '__main__':
    max = precompute()
    print(max.wordIndex)
    print(max.computeScore("CHECK"))




