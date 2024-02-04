import pathlib
import random
import re
import string
import tkinter
import wordfreq
import math
from GUI import GUI
from entropy import calculateMatches
from itertools import permutations
class Main:
    def __init__(self, maxGuessCount, maxWordLength):
        self.maxWordLength = maxWordLength
        data = self.generateRandomWord()
        self.guess = "_" * maxWordLength
        self.answer = data[0]
        self.won = False
        self.maxGuessCount = maxGuessCount
        self.dictionary = data[1]
        self.possibleWordlist = data[2]
        self.guessCount = 0
        self.guessWordCount = 0
        self.characterColours = []
        self.guessList = []

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
        word = "snake".upper()
        return word, dictionary,real
    def validGuess(self):
        #check the hashmap is the word is valid and it contain in the diction (hashmap for O(1) instead of O(n)
        return True if self.dictionary.get(hash(self.guess.upper())) and not self.won else False

    def checkGuess(self):
        #This will check if hash is the same as the answer hash using a hash table, if so, you win
        self.won = True if self.guess==self.answer else False
        #reset everything and increase the word count if word is valid
        if self.validGuess():
            self.updateCharacterColours()

            self.getNextWord()
            print("Done")
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

    def updateWordList(self):
        #based on how many trys, set the guess list to the current word.
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
                print("ADDED")
                matches.append(possibleWord)
        print("Info: ",self.getInfomation(float(len(matches)) / float(len(self.possibleWordlist))))


        newList = []
        for x in matches:
            newList.append([self.getInfomation(wordfreq.word_frequency(x,"en")),x])
        newList.sort()
        newList.reverse()
        print(newList)
        self.getEntropyData()
        self.possibleWordlist = matches
    def getEntropyData(self):
        perm = permutations(["green","yellow","grey"],5)
        print([x for x in perm])
        return [x for x in perm]

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

    def addWordToList(self):
        #update the list and reset the guess to blank
        self.updateWordList()
        self.guess = "_" * self.maxWordLength

    def getCharacterColours(self):
        return self.characterColours

    def getGuessList(self):
        return self.guessList

    def isGameOver(self):
        return self.won or self.guessWordCount == self.maxGuessCount


if __name__ == '__main__':
    main = Main(maxGuessCount = 6, maxWordLength = 5)
    gui = GUI(maxGuessCount = 6, maxWordLength = 5,
              addCharacterFunction = main.addCharacter, removeCharacterFunction = main.removeCharacter, checkGuessFunction = main.checkGuess,
              getCharacterColoursFunction = main.getCharacterColours, getGuessListFunction = main.getGuessList,
              isGameOverFunction = main.isGameOver, getEntropyDataFunction = main.getEntropyData)