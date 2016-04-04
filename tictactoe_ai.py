#!/usr/bin/python

from Tkinter import *
from time import sleep


# The tic-tac-toe grid will have the following numbering convertion
# 0 | 1 | 2
# ---------
# 3 | 4 | 5
# ---------
# 6 | 7 | 8


class TicTacToe:
    topLeft = 0
    topMid = 1
    topRight = 2
    midLeft = 3
    mid = 4
    midRight = 5
    botLeft = 6
    botMid = 7
    botRight = 8

    buttons = []

    def __init__(self):
        self.board = [" "] * 9
        # List comprehension is needed so that each StringVar will not point to the same object
        self.moves = [StringVar() for x in xrange(9)]
        self.xWins = 0
        self.oWins = 0
        self.currPlayer = "X"
        self.moveNumber = 0

        for m in self.moves:
            m.set(" ")

    def makeMove(self, move):
        aiOn.config(state='disabled')
        if self.currPlayer == "X":
            self.board[move] = "X"
            self.updateBoard(move)
            infoText.set("It is O's turn")
            self.currPlayer = "O"
        else:
            self.board[move] = "O"
            self.updateBoard(move)
            infoText.set("It is X's turn")
            self.currPlayer = "X"



    def reset(self):
        self.currPlayer = "X"
        self.moveNumber = 0

    def updateBoard(self, move):
        for i in xrange(9):
            self.moves[i].set(self.board[i])


# -------------------------------------
#             Game Setup
# -------------------------------------

root = Tk()
root.title("Ian's Tic-Tac-Toe Game")

game = TicTacToe()


# -------------------------------------
#              GUI Setup
# -------------------------------------

# Welcome Label
welcomeText = StringVar()
welcomeText.set("Welcome to Ian's Tic-Tac-Toe Game!")
welcome = Label(root, textvariable=welcomeText)
welcome.grid(row=0, column=0, columnspan=3)

# Label used to display the current scores
countText = StringVar()
countText.set("X: " + str(game.xWins) + "\tO: " + str(game.oWins))
count = Label(root, textvariable=countText)
count.grid(row=1, column=0, columnspan=3)

# Label used to give the user information
infoText = StringVar()
infoText.set("It is X's turn")
info = Label(root, textvariable=infoText)
info.grid(row=2, column=0, columnspan=3)

# Create buttons
for square in xrange(9):
    tempButton = Button(root, textvariable=game.moves[square], command=lambda s=square: game.makeMove(s))
    # Divide by 3 to get row number, modulus by 3 to get column number
    tempButton.grid(row=(square / 3) + 3, column=(square % 3), sticky=NSEW)
    game.buttons.append(tempButton)

# Button for resetting the game
restartButtonText = StringVar()
restartButtonText.set("Restart")
restartButton = Button(root, textvariable=restartButtonText, command=game.reset)
restartButton.grid(row=1, column=0)

# Checkbox for turning the AI on/off
aiOnVar = IntVar()
aiOn = Checkbutton(root, text="Turn on AI", variable=aiOnVar)
aiOn.grid(row=1, column=2)

# Set the size of the rows and columns
root.columnconfigure(0, minsize=100)
root.columnconfigure(1, minsize=100)
root.columnconfigure(2, minsize=100)
root.rowconfigure(3, minsize=100)
root.rowconfigure(4, minsize=100)
root.rowconfigure(5, minsize=100)

# Start the GUI loop
root.mainloop()

