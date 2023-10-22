"""
Author: Arthur Sweetman

Creation date: October 21, 2023
"""

import numpy as np
import pandas as pd
from tkinter import *
from tkinter import ttk
from keras.layers import Dense, Input
from keras import Model


class Board():

    def __init__(self, firstPlayer, secondPlayer):
        self.tiles = np.zeros((9,2), dtype=bool)
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
        elif np.sum(self.tiles[tile]) > 0:
            print("Space is already occupied. Cannot play there.")
        else:
            self.tiles[tile, player] = 1
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
        thisPlayersBoard = self.tiles[:,player]
        for combo in self.__winningCombos:
            test = np.isin(np.where(combo), np.where(thisPlayersBoard))
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

    def getPlayersTurn(self):
        return self.__thisPlayer

    def getWinner(self):
        return self.__winner

    def getWinningCombos(self):
        return self.__winningCombos


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
    input = Input(shape=(9,2))
    layer1 = Dense(50, activation="relu")(input)
    out = Dense(9, activation="softmax")(layer1)
    model = Model(input, out)
    return model


def compileModel():
    model = createModel()
    model.compile()
    # model.fit()
    return model


def playTiffnnyGame(model):
    tiffnny = 0
    rando = 1
    board = Board(tiffnny, rando)
    while board.getStatus() == "Unresolved":
        if board.getPlayersTurn() == tiffnny:
            modelInput = board.tiles.copy()
            pred = model.predict(board.tiles)
            nextMove = np.where(np.max(pred))
            board.play(nextMove, tiffnny)
        elif board.getPlayersTurn() == rando:
            openSpaces = np.where(board.tiles is None)
            randomChoice = np.random.randint(0, len(openSpaces))
            board.play(openSpaces[randomChoice], rando)
        else:
            print("...something's wrong...")
            break
    print(board.getAllBoards())


def main():
    # tiffnnyModel = compileModel()
    # playTiffnnyGame(tiffnnyModel)
    board = Board(0, 1)
    board.play(0,0)
    board.play(4, 1)
    board.play(1, 0)
    board.play(5, 1)
    board.play(2, 0)
    print(board.getAllBoards())
    # board.play(4, Players.O)
    # board.play(8, Players.X)
    # print(board.getAllBoards())


if __name__ == "__main__":
    main()