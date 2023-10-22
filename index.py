"""
Author: Arthur Sweetman

Creation date: October 21, 2023
"""

import numpy as np
import pandas as pd
from tkinter import *
from tkinter import ttk
from enum import Enum
from keras.layers import Dense, Input
from keras import Model


class Players(Enum):
    X = "x"
    O = "o"


class Board():

    def __init__(self, firstPlayer, secondPlayer):
        self.tiles = np.repeat(None, 9)
        self.__thisPlayer = firstPlayer
        self.__otherPlayer = secondPlayer
        self.__winningCombos = [[1, 1, 1, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 1, 1, 1],
                                [1, 0, 0, 1, 0, 0, 1, 0, 0],
                                [0, 1, 0, 0, 1, 0, 0, 1, 0],
                                [0, 0, 1, 0, 0, 1, 0, 0, 1],
                                [1, 0, 0, 0, 1, 0, 0, 0, 1],
                                [0, 0, 1, 0, 1, 0, 1, 0, 0]]
        self.__gameStatus = "Unresolved"
        self.__winner = "TBD"
        self.__allBoards = []

    def play(self, tile, player):
        if self.__gameStatus == "Resolved":
            print("Game is over.", self.__winner, "wins!\nPlease reset board to play again.")
        elif self.__thisPlayer != player:
            print("It is not your turn. Please let the other player play their turn.")
        elif self.tiles[tile] is not None:
            print("Space is already occupied. Cannot play there.")
        else:
            self.tiles[tile] = player
            self.__switchPlayersTurn()
            self.__allBoards.append(self.tiles.copy())  # important to append a copy of the current game board, so it does not get updated in the future
            self.analyze(player)

    def __switchPlayersTurn(self):
        temp = self.__thisPlayer
        self.__thisPlayer = self.__otherPlayer
        self.__otherPlayer = temp

    def show(self):
        print(self.tiles)

    def analyze(self, player):
        for combo in self.__winningCombos:
            test = np.isin(np.where(combo), np.where(self.tiles == player))
            result = test.prod()
            if result == 1:
                self.__gameStatus = "Resolved"
                self.__winner = player
                print("Game over.", player, "wins!")
                print("Final board:")
                print(self.show())
                break

    def reset(self):
        self.__init__(self.__thisPlayer, self.__otherPlayer)

    def getStatus(self):
        return self.__gameStatus


    def getAllBoards(self):
        return self.__allBoards


def openGame():
    window = Tk()
    for i in range(3):
        window.columnconfigure(i, weight=1, minsize=75)
        window.rowconfigure(i, weight=1, minsize=50)
        for j in range(3):
            frame = ttk.Frame(window, relief=RAISED, borderwidth=5)
            frame.grid(row=i, column=j)
            ttk.Button(frame, text=f"Row {i}\nColumn {j}").pack()

    window.mainloop()


def createModel():
    input = Input(9)
    layer1 = Dense(50, activation="relu")(input)
    out = Dense(9, activation="softmax")(layer1)
    model = Model(input, out)
    return model


def playGame(model, board = Board(Players.X, Players.O)):
    while board.getStatus() == "Unresolved":
        pred = model.predict(board.tiles)
        nextMove = np.where(np.max(pred))
        board.play(nextMove, Players.X)



def main():
    board = Board(Players.O, Players.X)
    # model = createModel()
    # model.summary()
    # model.fit()
    board.play(0, Players.O)
    board.play(4, Players.X)
    board.play(8, Players.O)
    print(board.getAllBoards())


if __name__ == "__main__":
    main()