"""
Author: Arthur Sweetman

Creation date: October 21, 2023
"""

import numpy as np
import pandas as pd
from tkinter import *
from tkinter import ttk
from enum import Enum


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


def main():
    board = Board(Players.O, Players.X)
    # openGame()
    board.play(3, Players.X)
    board.play(3, Players.X)
    board.play(4, Players.X)
    board.play(5, Players.X)
    board.play(6, Players.O)
    board.play(1, Players.O)
    board.play(1, Players.X)
    board.play(1, Players.O)
    board.play(8, Players.O)
    board.play(0, Players.X)
    board.play(7, Players.O)
    board.reset()
    board.show()



if __name__ == "__main__":
    main()