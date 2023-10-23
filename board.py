"""
@author: Arthur Sweetman

Tic-tac-toe board class
"""

import numpy as np
import pandas as pd

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
            return False
        elif self.__thisPlayer != player:
            print("It is not your turn. Please let the other player play their turn.")
            return False
        elif np.sum(self.tiles[tile]) > 0:
            print("Space is already occupied. Cannot play there.")
            return False
        else:
            self.tiles[tile, player] = 1
            self.__switchPlayersTurn()
            self.__allBoards.append(self.tiles.copy())  # important to append a copy of the current game board, so it does not get updated in the future
            self.analyze(player)
            return True

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