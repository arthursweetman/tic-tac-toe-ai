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
from board import Board


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