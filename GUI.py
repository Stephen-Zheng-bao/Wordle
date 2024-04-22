import tkinter as tk
from tkinter import ttk

class GUI:
    def __init__(self, maxGuessCount, maxWordLength,
                 addCharacterFunction, removeCharacterFunction,checkGuessFunction, getCharacterColoursFunction, getGuessListFunction,
                 isGameOverFunction, getEntropyDataFunction,getInformationDataFunction,getLetterColoursFuction):
        self.root = tk.Tk()
        self.root.title('Wordle')
        self.root.resizable(0, 0)

        self.maxGuessCount = maxGuessCount
        self.maxWordLength = maxWordLength

        self.addCharacterFunction = addCharacterFunction
        self.removeCharacterFunction = removeCharacterFunction
        self.checkGuessFunction = checkGuessFunction
        self.getCharacterColoursFunction = getCharacterColoursFunction
        self.getLetterColorsFuction = getLetterColoursFuction
        self.getGuessList = getGuessListFunction
        self.isGameOverFunction = isGameOverFunction
        self.getEntropyDataFunction = getEntropyDataFunction

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(7, weight=1)
        self.root.rowconfigure(7, weight=1)

        self.characterColours = getCharacterColoursFunction()
        self.keyboardColors = getLetterColoursFuction()
        self.guessList = getGuessListFunction()
        self.entropyData = getEntropyDataFunction()
        self.informationData = getInformationDataFunction

        self.createLayout()

    def left_frame(self):
        ttk.Label(self.root, text="Infomation Left").grid(row=0, column=0, padx=5, pady=5)
        if self.entropyData is not None:
            for i, pair in enumerate(self.informationData):
                left,expect,actual = pair
                # Insert the text into respective Text widgets
                txt = "Infomation Left: "+str(round(left,2))+"\n"+"Expected Information: "+str(round(expect,2))+"\n"+"Actual Infomation"+str(round(actual,2))
                ttk.Label(self.root, text=txt).grid(row=i+1, column=0, padx=5, pady=5, sticky="nsew")
    def right_frame(self):
        ttk.Label(self.root, text="Suggestion").grid(row=0, column=7, padx=5, pady=5)

        if self.entropyData is not None:
            for i, pair in enumerate(self.entropyData):
                word, score = pair
                # Insert the text into respective Text widgets
                txt = "Word: "+word+"\n"+"Score: "+str(score)+"\n"
                ttk.Label(self.root, text=txt).grid(row=i+1, column=7, padx=5, pady=5, sticky="nsew")


    def middle_frame(self):
        s = ttk.Style()
        s.configure("yellow.TFrame",background = "yellow")
        s.configure("green.TFrame", background="green")
        s.configure("grey.TFrame", background="grey")
        background = None

        ttk.Frame(self.root, borderwidth=5, relief="ridge", width=200, height=100, style=None).grid(row=0, column=1, columnspan=5,padx=5, pady=5)
        ttk.Label(self.root, text="Wordle").grid(row=0, column=1,columnspan = 5, padx=5, pady=5)


        for r in range(0, self.maxGuessCount):
            for c in range(0, self.maxWordLength):
                if self.characterColours[r]:
                    background = self.characterColours[r][c].lower() + ".TFrame"
                else:
                    background = None

                ttk.Frame(self.root, borderwidth=1, relief="ridge", width=30, height=30,style=background).grid(row=r+1, column=c+1, padx=5, pady=5)
                ttk.Label(self.root, text=self.guessList[r][c]).grid(row=r+1, column=c+1, padx=5, pady=5)
                self.root.grid_columnconfigure(c, weight=1, minsize=75)
    def keyboard_frame(self):
        s = ttk.Style()
        s.configure("yellow.TFrame", background="yellow")
        s.configure("green.TFrame", background="green")
        s.configure("grey.TFrame", background="grey")
        x=0
        ttk.Separator(self.root, orient='horizontal').grid(column=12, row=0, rowspan=10, sticky='ew')

        for c in self.keyboardColors:
            if c[1] is None:
                background = None
            else:
                #print(c[1])
                background = c[1].lower() + ".TFrame"
            x+=1


            ttk.Frame(self.root, borderwidth=1, relief="ridge", width=30, height=30, style=background).grid(row=13+(x//10), column=0+(x%10), padx=5, pady=5)
            ttk.Label(self.root, text=c[0].upper()).grid(row=13+(x//10), column=0+(x%10))



    def refresh(self):
        self.guessList = self.getGuessList()
        self.characterColours = self.getCharacterColoursFunction()
        self.entropyData = self.getEntropyDataFunction()
        self.keyboardColors = self.getLetterColorsFuction()

        for widgets in self.root.winfo_children():
            widgets.destroy()

        self.left_frame()
        self.middle_frame()
        self.right_frame()
        self.keyboard_frame()

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
        self.keyboard_frame()

        self.root.bind("<Key>", lambda event: self.onKeyPress(event))
        self.onKeyPress()
        self.winner()
        self.root.mainloop()


    def winner(self):
        if self.isGameOverFunction == True:

            self.root.destroy()
            self.root = tk.Tk()
            self.createLayout()






