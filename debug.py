#coding=utf8
"""
Created on Nov 11, 2011

@author: CVi
"""
from board import board
#from pprint import pprint
gameBoard = board()
print gameBoard.move((1, 0), (3, 0))
print gameBoard.move((6, 1), (4, 1))
print gameBoard.move((3, 0), (4, 1))
print gameBoard.move((6, 2), (5, 2))
print gameBoard.grid[0][0].possibleMoves((0, 0))
print gameBoard.move((0, 0), (6, 0))
print gameBoard.grid[7][1].possibleMoves((7, 1))
print gameBoard.move((7, 1), (5, 0))
print gameBoard.move((1, 3), (3, 3))
print gameBoard.grid[7][2].possibleMoves((7, 2))
print gameBoard.move((7, 2), (6, 1))
print gameBoard.move((0, 3), (2, 3))
print gameBoard.move((0, 3), (2, 3))
#pprint (gameBoard.grid)
