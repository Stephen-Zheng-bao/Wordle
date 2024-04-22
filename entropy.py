import math

def calculateMatches(word, searchSpace, pattern):

  possibleMatches = searchSpace

  matches = []
  for possibleMatch in possibleMatches:
    if possibleMatch == word:
      continue
    matchBool = True
    lettersUsed = []
    for i, p in enumerate(pattern):

      if p==1: #Yellow. Letter in word, but not in position
        lettersUsed.append(word[i])
        if word[i] not in possibleMatch or word[i] == possibleMatch[i]:
          matchBool = False
          break
      elif p==2: #Green. Letter in current Position
        lettersUsed.append(word[i])
        if word[i] != possibleMatch[i]:
          matchBool = False
          break
    for i, p in enumerate(pattern):
      if word[i] in lettersUsed:
        continue
      if p == 0: #Grey. Letter not in Word.
        if word[i] in possibleMatch:
          matchBool = False
          break
    if matchBool:
      matches.append(possibleMatch)
      print("ADDED")

  return matches

"""f = open("beep/case.txt", "r")
dictionary = []
for x in f:
    # Remove all text after the first word
    var = x.split(' ', 1)[0]
    if len(var) ==5:
    # if there is only non-punctuation, put it on the word list using a hash
        if var.isalnum():
            dictionary.append(var)"""

def generatePatternPermutations():
  patterns = [[]]
  for i in range(5):
    newPatterns = []
    for pattern in patterns:
      newPatterns.append(pattern + [0])
      newPatterns.append(pattern + [1])
      newPatterns.append(pattern + [2])
    patterns = newPatterns
  print(patterns)
  return patterns
def calculateWordEntropy(word, searchSpace):
  entropy = 0
  patternPerms = generatePatternPermutations()
  for patternPerm in patternPerms:
    print(patternPerm)
    matchProbability = float(len(calculateMatches(word, searchSpace, patternPerm)))/float(len(searchSpace))
    entropy += (matchProbability * calculateInformation(matchProbability))
  print()
  return entropy

def calculateInformation(probablity):
  if not probablity:
    return 0.0
  return -math.log2(probablity)


class WordleGame:

  def __init__(self):
    with open("beep/case.txt", "r") as file:

      dictionary = []
      for x in file:
        # Remove all text after the first word
        var = x.split(' ', 1)[0]
        if len(var) == 5:
          # if there is only non-punctuation, put it on the word list using a hash
          if var.isalnum():
            if len(var) == 5:
              dictionary.append(var)

    self.searchSpace = dictionary
    self.informationRemaining = calculateInformation(1.0 / float(len(self.searchSpace)))

    self.suggestions = dictionary

    for i in range(6):
      if len(self.suggestions) > 1:  # More than 1 possible answer
        for x in self.suggestions:
          print(x)
        self.enterGuess(i + 1)
      elif len(self.suggestions) == 1:  # Only 1 answer
        print(
          f"Answer must be: {list(self.suggestions.keys())[0]}")
        break
      else:
        print('Something went wrong!')
        break

  def enterGuess(self, i):
    print(f'Info Remaining: {self.informationRemaining} bits')
    print(f'{i}:')
    wordGuess = input('Guess: ').upper()
    patternInput = input('Pattern: ')
    patternReturned = [int(i) for i in patternInput]
    print(patternReturned)
    # Do new calculations
    newSearchSpace = calculateMatches(wordGuess, self.searchSpace, patternReturned)
    print(f'Actual Info: {calculateInformation(float(len(newSearchSpace)) / float(len(self.searchSpace)))}')
    print("1",self.searchSpace)
    self.searchSpace = newSearchSpace
    print("*"*100)
    print("2",self.searchSpace)
    self.informationRemaining = calculateInformation(1.0 / float(len(self.searchSpace)))
    self.suggestions = {}
    for w in self.searchSpace:
      self.suggestions[w] = calculateWordEntropy(w, self.searchSpace)
    sortedSuggestions = [i for i in self.suggestions]


    def sortByEntropy(e):
      return self.suggestions[e]

    sortedSuggestions.sort(key=sortByEntropy, reverse=True)
    self.suggestions = {i: self.suggestions[i] for i in sortedSuggestions}

    print(self.suggestions)


if __name__ == '__main__':
  wordle = WordleGame()
