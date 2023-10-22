"""
Author: Arthur Sweetman

Creation date: October 21, 2023
"""

import numpy as np
import pandas as pd
from tkinter import *
from tkinter import ttk


class Board():
    def __init__(self):
        self.tiles = np.repeat(None, 9)

    def play(self, tile, player):
        self.tiles[tile] = player

    def show(self):
        print(self.tiles)


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
    board = Board()
    openGame()


if __name__ == "__main__":
    main()