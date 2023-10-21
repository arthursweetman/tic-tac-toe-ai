"""
Author: Arthur Sweetman

Creation date: October 21, 2023
"""

import numpy as np
import pandas as pd


class Board():
    def __init__(self):
        self.tiles = np.repeat(None, 9)

    def play(self, tile, player):
        self.tiles[tile] = player

    def show(self):
        print(self.tiles)


def main():
    board = Board()
    board.show()
    board.play(0, "x")
    board.show()
    board.play(2, "o")
    board.show()


if __name__ == "__main__":
    main()