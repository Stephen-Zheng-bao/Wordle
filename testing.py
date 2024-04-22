import timeit
import pickle
import random

from main import Main
from tqdm import tqdm


class Test:
    def __init__(self, maxGuessCount, maxWordLength,
                 GetAddWord,checkGuessFunction, getCharacterColoursFunction, getGuessListFunction,
                 isGameOverFunction, getEntropyDataFunction,getInformationDataFunction,getReset,getWord):

        self.maxGuessCount = maxGuessCount
        self.maxWordLength = maxWordLength

        self.addWordFunction = GetAddWord
        self.checkGuessFunction = checkGuessFunction
        self.getGuessList = getGuessListFunction
        self.isGameOverFunction = isGameOverFunction
        self.getEntropyDataFunction = getEntropyDataFunction
        self.getWordDataFunction = getWord

        self.characterColours = getCharacterColoursFunction()
        self.guessList = getGuessListFunction()
        self.entropyData = self.getEntropyDataFunction()
        self.informationData = getInformationDataFunction
        self.gameOver = self.isGameOverFunction()
        self.broken = 0
        self.wordCount = 0
        self.words = self.getWordDataFunction()

        f = open("beep/case.txt", "r")
        real = []
        for x in f:
            var = x.split(' ', 1)[0]
            if var.isalnum():
                if len(var) == 5:
                    real.append(var)
        self.wordList = real

    def start(self):

            Total = 0
            for x in tqdm(range(10000)):
                #for bais run this
                #word = x
                self.words = self.getWordDataFunction()
                word = random.choice(self.wordList)
                #print("End word "+self.words)
                #print("Starting word "+word)
                #print(x)
                self.addWordFunction(word)
                trycount = 1

                while not self.gameOver:
                    trycount += 1
                    self.checkGuessFunction()
                    self.entropyData = self.getEntropyDataFunction()
                    self.guessList = self.getGuessList()

                    try:
                        #random
                        word = random.choice(self.entropyData)[0]
                        #top 1
                        #                                                                                                                                                                                 word = self.entropyData[0][0]
                    except:
                        #print("Broken")
                        self.broken +=1
                        break
                    if word == self.words:
                        break

                    self.addWordFunction(word)


                    if trycount ==7:
                        break
                    self.gameOver = self.isGameOverFunction()

                Total+=trycount

                self.addWordFunction(self.words)
            print(Total)
            print(self.broken)

if __name__ == '__main__':
    main = Main(maxGuessCount = 6, maxWordLength = 5)
    test = Test(maxGuessCount=6, maxWordLength=5,
                GetAddWord=main.addWord,
                checkGuessFunction=main.checkGuess,
                getCharacterColoursFunction=main.getCharacterColours, getGuessListFunction=main.getGuessList,
                isGameOverFunction=main.isGameOver, getEntropyDataFunction=main.getEntropyData,
                getInformationDataFunction=main.getInformationData(),getReset=main.reset,getWord=main.getWord)
    test.start()