#coding=utf8
"""
Created on Nov 9, 2011

@author: CVi
"""
from pieces import *
import syslog
syslog.openlog("Python")

class board(object):
    def __init__(self):
        self.empty = piece
        self.grid = []
        for i in range(8):
            self.grid.append(list([self.empty(self, None)] * 8))
        self.player = 0
        self.dirty = []
        self.cloned = None
        self.cloned2 = None

        self.grid[0] = [
            rook(self, 0), knight(self, 0), bishop(self, 0), queen(self, 0),
            king(self, 0), bishop(self, 0), knight(self, 0), rook(self, 0)]
        self.grid[1] = list([pawn(self, 0)]) * 8
        self.grid[6] = list([pawn(self, 1)]) * 8
        self.grid[7] = [
            rook(self, 1), knight(self, 1), bishop(self, 1), king(self, 1),
            queen(self, 1), bishop(self, 1), knight(self, 1), rook(self, 1)]

    def move(self, start, stop):
        """
        Moves a piece from start to stop
        Complete!
        @param start: tuple with 2 numbers from 0 to 7 (board coordiantes)
        @param stop: tuple with 2 numbers from 0 to 7 (board coordiantes)
        """
        #Check if move is legal
        if self.grid[start[0]][start[1]].player == self.player and self.grid[start[0]][start[1]].LegalMove(start, stop):
            self.clone()
            #preform move
            self.grid[start[0]][start[1]], self.grid[stop[0]][stop[1]] = self.empty(self, None), self.grid[start[0]][start[1]]
            self.grid[stop[0]][stop[1]].postMove(stop)
            #Dirty squares
            self.dirty.append(start)
            self.dirty.append(stop)
            self.player = 1 if self.player == 0 else 0
            return True
        else:
            return False

    def getPieces(self, player):
        ps = []
        for x in range(8):
            for y in range(8):
                if self.grid[y][x].player == player:
                    ps.append((y, x, self.grid[y][x]))
        return ps

    def findKing(self, player):
        for x in range(8):
            for y in range(8):
                if self.grid[y][x].player == player and str(self.grid[y][x]).lower() == "k":
                    return (y, x)

    def check(self, player):
        pieces = self.getPieces(1 if player == 0 else 0)
        king = self.findKing(player)
        for piece in pieces:
            if piece[2].LegalMove((piece[0], piece[1]), king):
                return True
        return False

    def mate(self):
        pieces = self.getPieces(self.player)
        possibleMoves = []
        for piece in pieces:
            possibleMoves += map(
                                 lambda to:((piece[1], piece[2]), to),
                                 piece[0].possibleMoves((piece[1], piece[2]))
                                 )
        for move in possibleMoves:
            self.move(move[0], move[1])
            if not self.check(1 if self.player == 0 else 0):
                self.abort()
                return False
            self.abort()
        self.abort()


    def abort(self):
        if self.cloned:
            self.grid, self.cloned, self.player = self.cloned, None, 1 if self.player == 0 else 0

    def clone(self):
        self.cloned = []
        for row in self.grid:
            self.cloned.append(list(row))
