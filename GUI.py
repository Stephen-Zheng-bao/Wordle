import tkinter as tk
from tkinter import ttk

class GUI:
    def __init__(self, maxGuessCount, maxWordLength,
                 addCharacterFunction, removeCharacterFunction,checkGuessFunction, getCharacterColoursFunction, getGuessListFunction,
                 isGameOverFunction, getEntropyDataFunction):
        self.root = tk.Tk()
        self.root.title('Wordle')
        self.root.resizable(0, 0)

        self.maxGuessCount = maxGuessCount
        self.maxWordLength = maxWordLength

        self.addCharacterFunction = addCharacterFunction
        self.removeCharacterFunction = removeCharacterFunction
        self.checkGuessFunction = checkGuessFunction
        self.getCharacterColoursFunction = getCharacterColoursFunction
        self.getGuessList = getGuessListFunction
        self.isGameOverFunction = isGameOverFunction
        self.getEntropyDataFunction = getEntropyDataFunction

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(7, weight=1)
        self.root.rowconfigure(7, weight=1)

        self.characterColours = getCharacterColoursFunction()
        self.guessList = getGuessListFunction()
        self.entropyData = getEntropyDataFunction()

        self.createLayout()

    def left_frame(self):
        ttk.Label(self.root, text="Left").grid(row=0, column=0, padx=5, pady=5)

    def right_frame(self):
        ttk.Label(self.root, text="Right").grid(row=0, column=7, padx=5, pady=5)

    def middle_frame(self):
        s = ttk.Style()
        s.configure("yellow.TFrame",background = "yellow")
        s.configure("green.TFrame", background="green")
        s.configure("grey.TFrame", background="grey")
        background = None

        ttk.Frame(self.root, borderwidth=5, relief="ridge", width=200, height=100, style=None).grid(row=0, column=1, columnspan=5,padx=5, pady=5)
        ttk.Label(self.root, text="Middle").grid(row=0, column=1,columnspan = 5, padx=5, pady=5)

        print(self.guessList)
        for r in range(0, self.maxGuessCount):
            for c in range(0, self.maxWordLength):
                if self.characterColours[r]:
                    background = self.characterColours[r][c].lower() + ".TFrame"
                else:
                    background = None

                ttk.Frame(self.root, borderwidth=1, relief="ridge", width=30, height=30,style=background).grid(row=r+1, column=c+1, padx=5, pady=5)
                ttk.Label(self.root, text=self.guessList[r][c]).grid(row=r+1, column=c+1, padx=5, pady=5)
                self.root.grid_columnconfigure(c, weight=1, minsize=75)

    def refresh(self):
        self.guessList = self.getGuessList()
        self.characterColours = self.getCharacterColoursFunction()
        self.entropyData = self.getEntropyDataFunction()

        for widgets in self.root.winfo_children():
            widgets.destroy()

        self.left_frame()
        self.middle_frame()
        self.right_frame()

    def onKeyPress(self, e=None):
        if self.isGameOverFunction():
            return

        if e:
            if e.keysym == "BackSpace":
                self.removeCharacterFunction()
            elif e.keysym == "Return":
                self.checkGuessFunction()
            elif 65 <= e.keycode <= 90:
                self.addCharacterFunction(e.keysym)


            self.refresh()

    def createLayout(self):
        self.left_frame()
        self.middle_frame()
        self.right_frame()

        self.root.bind("<Key>", lambda event: self.onKeyPress(event))
        self.onKeyPress()

        self.root.mainloop()





