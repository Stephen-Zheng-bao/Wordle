import random
import wordfreq
import math
from GUI import GUI
from entropy import calculateMatches
from precompute import precompute


import numpy as np

import timeit

class Main:
    def __init__(self, maxGuessCount, maxWordLength,auto=False):

        self.maxWordLength = maxWordLength
        self.precompute = precompute()
        data = self.generateRandomWord()
        self.guess = "_" * maxWordLength

        self.won = False
        self.auto = auto
        self.maxGuessCount = maxGuessCount
        self.answer = data[0]
        self.dictionary = data[1]
        self.possibleWordlist = data[2]
        self.guessCount = 0
        self.guessWordCount = 0
        self.characterColours=[]
        x = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m']

        self.letterColors = [[y,None] for y in x]

        self.guessList = []
        self.top10Score = []
        self.information = []

        for i in range(0, maxGuessCount):
            self.characterColours.append([])
            self.guessList.append("_" * maxWordLength)

            for j in range(0, maxWordLength):
                self.characterColours[i].append("")



    def generateRandomWord(self):
        ###This will generate a random word and return it
        f = open("beep/case.txt", "r")
        dictionary = {}
        real = []
        for x in f:
            # Remove all text after the first word
            var = x.split(' ', 1)[0]
            # if there is only non-punctuation, put it on the word list using a hash
            if var.isalnum():
                if len(var) == self.maxWordLength:
                    real.append(var)
                dictionary.update({hash(var): var})
        ###Currently the word is set to snake but it does work
        word = random.choice(real).upper()
        word = "SCOLD"
        #print(word)
        return word, dictionary,real
    def reset(self):
        if self.won or self.guessWordCount == self.maxGuessCount:
            self.maxWordLength = self.maxWordLength
            self.precompute = self.precompute
            data = self.generateRandomWord()
            self.guess = "_" * self.maxWordLength

            self.won = False
            self.answer = data[0]
            self.dictionary = data[1]
            self.possibleWordlist = data[2]
            self.autoCount = 0
            self.guessCount = 0
            self.guessWordCount = 0
            self.characterColours = []
            self.guessList = []
            self.top10Score = []
            self.information = []

            for i in range(0, self.maxGuessCount):
                self.characterColours.append([])
                self.guessList.append("_" * self.maxWordLength)

                for j in range(0, self.maxWordLength):
                    self.characterColours[i].append("")

    def validGuess(self):
        #check the hashmap is the word is valid and it contain in the diction (hashmap for O(1) instead of O(n)
        return True if self.dictionary.get(hash(self.guess.upper())) and not self.won else False

    def checkGuess(self):
        #This will check if hash is the same as the answer hash using a hash table, if so, you win

        self.won = True if self.guess.upper()==self.answer else False
        #reset everything and increase the word count if word is valid
        if self.won:
            #print("win")
            self.reset()
        if self.validGuess():
            self.updateCharacterColours()

            self.getNextWord()

            self.addWordToList()


            self.guessWordCount += 1
            self.guessCount = 0


    def removeCharacter(self):
        #if the current word count(length) is greater than 0, subtract the last letter from it
        if self.guessCount > 0:
            self.guess = self.guess.split("_")
            self.guess = self.guess[0][:-1]

            self.guessCount -= 1
            self.guess +=("_"*(int(self.maxWordLength)-int(self.guessCount)))

        self.updateWordList()

    def addCharacter(self, character):
        #add a character to the current word
        if self.guessCount != self.maxWordLength:
            listGuess = list(self.guess)
            listGuess[self.guessCount] = character
            self.guess = ''.join(listGuess)
            self.guessCount += 1

            self.updateWordList()
        #AutoDone feature
        """if self.guessCount == self.maxWordLength:
            self.checkGuess()"""
    def addWord(self,word):
        self.guess = word
        self.guessCount = len(word)
        if (self.guessCount == self.maxGuessCount) or self.won:
            self.reset()
        if self.validGuess():
            self.updateWordList()
            self.guessCount += 1

    def updateWordList(self):
        #based on how many trys, set the guess list to the current word.
        self.won = True if self.guess.upper() == self.answer else False
        # reset everything and increase the word count if word is valid
        if self.isGameOver():
            self.reset()
        else:
            self.guessList[self.guessWordCount] = self.guess

    def getNextWord(self):

        
        word = self.guess.upper()

        matches = []
        for possibleWord in self.possibleWordlist:

            if possibleWord == word:
                continue

            matchBool = True
            #the point of using this word list so double letter can be coved
            lettersUsed = []
            for i, p in enumerate(self.characterColours[self.guessWordCount]):

                if p == "yellow":

                    lettersUsed.append(word[i])
                    #if its is yellow word but no containing the word or match it, dont add the word
                    if word[i] not in possibleWord or word[i] == possibleWord[i]:
                        matchBool = False
                        break
                elif p == "green":
                    lettersUsed.append(word[i])
                    #if the postion isnt correct, break the loop
                    if word[i] != possibleWord[i]:
                        matchBool = False
                        break
            for i, p in enumerate(self.characterColours[self.guessWordCount]):
                if word[i] in lettersUsed:
                    continue
                if p == "grey":

                    if word[i] in possibleWord:
                        matchBool = False
                        break
            #After all the check, if the matchBool isnt broken, the possible word must be possible
            if matchBool:
                #print("ADDED")
                matches.append(possibleWord)


        newList = {}
        for x in matches:
            newList[x]=wordfreq.word_frequency(x,"en")

        self.updateInfomation(matches)
        self.calculateScore(matches)

        self.possibleWordlist = matches

    def sigmoid(self,x):
        return 1 / (1 + np.exp(-x))
    def calculateScore(self,matches):
        newList = {}
        freqList = {}
        for x in matches:
            freqList[x] = wordfreq.word_frequency(x, "en")
        # This will scale the freq
        #OLD scale
        """
        total = sum(freqList.values())
        if total == 0:
            scaled_values = {key:value for key,value in freqList.items()}
        else:
            scaled_values = {key: value / total for key, value in freqList.items()}"""

        #New Scale
        scaled_values = {key: self.sigmoid(value) for key, value in freqList.items()}


        for x in matches:
            newList[x] = self.precompute.computeScore(x) * scaled_values[x]
            #newList[x] =wordfreq.word_frequency(x, "en")
            #newList[x] = self.precompute.computeScore(x)
            #newList[x] = self.precompute.computeScore(x) + scaled_values[x]

        #sort the list and remove freq
        #change the code
        words = np.array(list(scaled_values.keys()))
        freq = np.array([newList[w] for w in words])
        argSort = freq.argsort()[::-1]
        sortedWords = words[argSort]

        #print(newList)

        #print("sorted", sortedWords)
        #print("top 10:", sortedWords[:10])

        #cal the top 10 score based on the sortedwords list
        self.top10Score = [[word, newList[word]] for word in sortedWords if word in newList]

        #print("top 10 with freq",self.top10Score)

    def getEntropyData(self):
        return self.top10Score[:10]

    def updateInfomation(self,matches):
        #print("Infomation left")
        #print(self.getInfomation(1/float(len(self.possibleWordlist))))

        #print("Expected Intomation")
        #print(self.precompute.computeScore(self.guess.upper()))
        expect = self.precompute.computeScore(self.guess.upper())
        #print("Actual Infomation:")
        #print("Info: ", self.getInfomation(float(len(matches)) / float(len(self.possibleWordlist))))
        left = self.getInfomation(1/float(len(self.possibleWordlist)))
        actual = self.getInfomation(float(len(matches)) / float(len(self.possibleWordlist)))
        expect = self.precompute.computeScore(self.guess.upper())
        self.information.append([left,expect,actual])
    def getInfomation(self,prob):

        if prob == 0:
            return 0.0
        return -math.log2(prob)

    def updateCharacterColours(self):
        #this return a colour based on the letter matching
        for i in range(0, self.maxGuessCount):
            for j in range(0, self.maxWordLength):
                character = self.guessList[i][j].upper()

                if character == "_":
                    self.characterColours[i][j] = "none"
                    continue

                index = self.answer.find(character)

                if index == -1:
                    self.characterColours[i][j] = "grey"
                elif index == j:
                    self.characterColours[i][j] = "green"
                else:
                    self.characterColours[i][j] = "yellow"
        inc = 0
        for x in self.letterColors:

            for i in range(0, self.maxGuessCount):
                for j in range(0, self.maxWordLength):
                    character = self.guessList[i][j].upper()
                    if x[0].upper() == character:
                        index = self.answer.find(character)
                        if index == -1:
                            #grey
                            if x[1] != "green" and x[1] != "yellow":
                                self.letterColors[inc] = [x[0],"grey"]
                        elif index == j:
                            self.letterColors[inc] = [x[0],"green"]
                        else:
                            if x[1] != "green":
                                self.letterColors[inc] = [x[0], "yellow"]
            inc +=1

        #print(self.characterColours)
        #print(self.letterColors)

    def addWordToList(self):
        #update the list and reset the guess to blank
        self.updateWordList()
        self.guess = "_" * self.maxWordLength

    def getInformationData(self):
        return self.information

    def getCharacterColours(self):
        return self.characterColours

    def getLetterColours(self):
        return self.letterColors

    def getGuessList(self):
        return self.guessList

    def getDictionary(self):
        return self.dictionary

    def isGameOver(self):
        return self.won or self.guessWordCount == self.maxGuessCount

    def getWord(self):
        return self.answer


if __name__ == '__main__':

    main = Main(maxGuessCount = 6, maxWordLength = 5)
    gui = GUI(maxGuessCount = 6, maxWordLength = 5,
              addCharacterFunction = main.addCharacter, removeCharacterFunction = main.removeCharacter, checkGuessFunction = main.checkGuess,
              getCharacterColoursFunction = main.getCharacterColours, getGuessListFunction = main.getGuessList,
              isGameOverFunction = main.isGameOver, getEntropyDataFunction = main.getEntropyData, getInformationDataFunction = main.getInformationData(),getLetterColoursFuction=main.getLetterColours)