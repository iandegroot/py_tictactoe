#!/usr/bin/python

from Tkinter import *
import copy

# The tic-tac-toe grid will have the following numbering convention
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
        self.moves = [StringVar() for _ in xrange(9)]
        self.xWins = 0
        self.oWins = 0
        self.currPlayer = "X"
        self.moveNumber = 0

        for m in self.moves:
            m.set(" ")

    def makeMove(self, move):
        aiOn.config(state='disabled')
        self.moveNumber += 1
        if self.currPlayer == "X":
            self.board[move] = "X"
            infoText.set("It is O's turn")
            self.currPlayer = "O"
            # If the AI is turned on then tell the AI to take its turn
            if aiOnVar.get() and self.moveNumber < 9:
                self.aiMMInit()
        else:
            self.board[move] = "O"
            infoText.set("It is X's turn")
            self.currPlayer = "X"

        self.buttons[move].config(state="disabled")

        # Check for a win
        if self.gameWon(self.board, "X"):
            self.whoWon("X")
        elif self.gameWon(self.board, "O"):
            self.whoWon("O")
        # Check for a Cat's game
        elif self.moveNumber == 9:
            if self.boardFull(self.board):
                infoText.set("Cat's game!")
                for b in self.buttons:
                    b.config(disabledforeground="red")

        self.updateBoard()

    # Check who won the game, and change the GUI state accordingly
    def whoWon(self, winningPlayer):
        if winningPlayer == "X":
            infoText.set("X wins!!!")
            self.xWins += 1
        else:
            infoText.set("O wins!!!")
            self.oWins += 1

        countText.set("X: " + str(self.xWins) + "\tO: " + str(self.oWins))

        for b in self.buttons:
            b.config(state="disabled")

    # Reset the game to its base state
    def reset(self):
        aiOn.config(state='normal')
        self.currPlayer = "X"
        self.moveNumber = 0

        infoText.set("It is X's turn")

        self.board = [" " for _ in self.board]
        self.updateBoard()

        for b in self.buttons:
            b.config(state="normal")
            b.config(disabledforeground="black")

    # Update the GUI to reflect the moves in the board attribute
    def updateBoard(self):
        for i in xrange(9):
            self.moves[i].set(self.board[i])

    def gameWon(self, gameboard, player):
        won = False

        # Horizontal
        won |= self.threeInARow(gameboard, player, TicTacToe.topLeft, TicTacToe.topMid, TicTacToe.topRight)
        won |= self.threeInARow(gameboard, player, TicTacToe.midLeft, TicTacToe.mid, TicTacToe.midRight)
        won |= self.threeInARow(gameboard, player, TicTacToe.botLeft, TicTacToe.botMid, TicTacToe.botRight)

        # Vertical
        won |= self.threeInARow(gameboard, player, TicTacToe.topLeft, TicTacToe.midLeft, TicTacToe.botLeft)
        won |= self.threeInARow(gameboard, player, TicTacToe.topMid, TicTacToe.mid, TicTacToe.botMid)
        won |= self.threeInARow(gameboard, player, TicTacToe.topRight, TicTacToe.midRight, TicTacToe.botRight)

        # Diagonal
        won |= self.threeInARow(gameboard, player, TicTacToe.topLeft, TicTacToe.mid, TicTacToe.botRight)
        won |= self.threeInARow(gameboard, player, TicTacToe.topRight, TicTacToe.mid, TicTacToe.botLeft)

        return won

    def threeInARow(self, gameboard, player, pos1, pos2, pos3):
        # TODO - Save winning positions to change the colors on a win
        if gameboard[pos1] == gameboard[pos2] == gameboard[pos3] and gameboard[pos1] == player:
            return True
        else:
            return False

    # Get the opposite player
    def getEnemy(self, currPlayer):
        if currPlayer == "X":
            return "O"
        else:
            return "X"

    # Returns true if the board is full
    def boardFull(self, board):
        for s in board:
            if s == " ":
                return False

        return True

    def aiMMInit(self):
        player = 'O'
        a = -1000
        b = 1000

        boardCopy = copy.deepcopy(self.board)

        bestOutcome = -100

        bestMove = None

        for i in xrange(9):
            if boardCopy[i] == " ":
                boardCopy[i] = player
                val = self.minimax(self.getEnemy(player), boardCopy, a, b)
                boardCopy[i] = " "
                if player == "O":
                    if val > bestOutcome:
                        bestOutcome = val
                        bestMove = i
                else:
                    if val < bestOutcome:
                        bestOutcome = val
                        bestMove = i

        self.makeMove(bestMove)

    def minimax(self, player, board, alpha, beta):
        boardCopy = copy.deepcopy(board)

        # Check for a win
        if self.gameWon(boardCopy, "O"):
            return 1
        elif self.gameWon(boardCopy, "X"):
            return -1
        elif self.boardFull(boardCopy):
            return 0

        best = -100 if player == "O" else 100

        for i in xrange(9):
            if boardCopy[i] == " ":
                boardCopy[i] = player
                val = self.minimax(self.getEnemy(player), boardCopy, alpha, beta)
                boardCopy[i] = " "
                if player == "O":
                    best = max(best, val)
                    alpha = min(alpha, best)
                else:
                    best = min(best, val)
                    beta = max(beta, best)

                if beta <= alpha:
                    return best

        return best


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

