#coding=utf8
"""
Created on Nov 9, 2011

@author: CVi
"""
from pieces import *
import syslog
syslog.openlog("Python")

class board(object):
    """
    Board object, containing all the rules needed for a chess game
    """
    M_OK = 1000
    """Move completed"""
    M_ILLEGAL = 1001
    """Illegal Move"""
    M_CHECK = 1002
    """Illegal Move: self-check"""
    S_OK = 2000
    """Users king is safe"""
    S_CHECK = 2001
    """User has been checked"""
    S_CHECKMATE = 2002
    """User has Been checkmated"""
    def __init__(self):
        """
        Initializes the board and places the pieces
        """
        self.empty = piece(self, None)
        """An instance of empty square object """
        self.grid = []
        """The grid for the board List of Lists (y, x)"""
        for i in range(8): #@UnusedVariable dummy Variable
            self.grid.append(list([self.empty] * 8))
        self.player = 0
        """"Current player (1 or 0) initialized to 0"""
        self.dirty = []
        """Dirty squares; 
        To produce efficient User Interfaces the module provides
        a list of squares that has changes made to them (y,x)"""
        self.cloned = None
        """Undo data, used to save previous game state when performing a move
        so it can be loaded if an undo is needed"""

        #Place the chess pieces
        #Pieces are autonomous objects and define their own rules for movement.
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
        @param start: coordinate (y,x)
        @param stop: coordinate (y,x)
        @return: True if move completed, otherwise false
        """
        #Check if move is legal
        if self.grid[start[0]][start[1]].player == self.player and self.grid[start[0]][start[1]].LegalMove(start, stop):
            self.clone()
            #preform move
            self.grid[start[0]][start[1]], self.grid[stop[0]][stop[1]] = self.empty, self.grid[start[0]][start[1]]
            self.grid[stop[0]][stop[1]].postMove(stop)
            #Dirty squares
            self.dirty.append(start)
            self.dirty.append(stop)
            self.player = 1 if self.player == 0 else 0
            return True
        else:
            return False

    def moveCheck(self, start, stop):
        """
        Wrapper to move piece from start to stop if move is legal
        and do not result in checking yourself.
        Returns a status code.
        @param start: (y,x)
        @param stop: (y,x)
        @return: M_OK|M_ILLEGAL|M_CHECK
        """
        #Try to move, return errorcode if unsuccessful
        if not self.move(start, stop): return self.M_ILLEGAL
        #Did that put the player in check, undo ad return errorcode. 
        if self.check(1 if self.player == 0 else 0):
            self.abort()
            return self.M_CHECK
        #Otherwise return sucesscode
        return self.M_OK


    def getPieces(self, player):
        """
        Gets all the pieces of the given player.
        @param player: 0|1
        @return (y,x,piece)
        """
        ps = []
        for x in range(8):
            for y in range(8):
                if self.grid[y][x].player == player:
                    ps.append((y, x, self.grid[y][x]))
        return ps

    def findKing(self, player):
        """
        Returns the position of the given players king
        @param player: 0|1
        @return: (y,x)
        """
        for x in range(8):
            for y in range(8):
                if self.grid[y][x].player == player and isinstance(self.grid[y][x], king):
                    return (y, x)

    def check(self, player):
        """
        Checks if the given player is checked.
        @param player: 0|1
        @return bool
        """
        pieces = self.getPieces(1 if player == 0 else 0)
        king = self.findKing(player)
        for piece in pieces:
            if piece[2].LegalMove((piece[0], piece[1]), king):
                return True
        return False

    def mate(self):
        """
        Checks if the current player (in check) is in a checkmate.
        @return: bool
        """
        pieces = self.getPieces(self.player)
        possibleMoves = []
        for piece in pieces:
            possibleMoves += map(
                                 lambda to:((piece[0], piece[1]), to),
                                 piece[2].possibleMoves((piece[0], piece[1]))
                                 )
        for move in possibleMoves:
            self.move(move[0], move[1])
            if not self.check(1 if self.player == 0 else 0):
                self.abort()
                return False
            self.abort()
        self.abort()
        return True

    def checkmate(self):
        """
        Checks if the current player is in check and if so is it a checkmate.
        @return: S_OK|S_CHECK|S_CHECKMATE
        """
        if self.check(self.player):
            if self.checkmate():
                return self.S_CHECKMATE
            else:
                return self.S_CHECK
        else:
            return self.S_OK

    def abort(self):
        """
        Aborts the last move, used internally by "one move" simulation.
        returns nothing
        """
        if self.cloned:
            self.grid, self.cloned, self.player = self.cloned, None, 1 if self.player == 0 else 0

    def clone(self):
        """
        Clones the current state of the board, needed to be able to abort()
        returns nothing
        """
        self.cloned = []
        for row in self.grid:
            self.cloned.append(list(row))
