#coding=utf8
"""
Created on Nov 10, 2011

@author: CVi
"""

class piece(object):
    def __init__(self, board, player):
        """
        @param board:
        @param palyer:
        """
        self.board = board
        self.player = player
        self.check = False

    def LegalMove(self, start, stop):
        return False

    def __str__(self):
        return " "

    def postMove(self, stop):
        pass

    def possibleMoves(self, pos):
        return []

class pawn(piece):
    def __str__(self):
        return "P" if self.player == 0 else "d"
    def LegalMove(self, start, stop):
        if start[1] == stop[1]:
            if stop[0] == start[0] + (1 if self.player == 0 else -1) and\
                self.board.grid[stop[0]][stop[1]].player == None:
                return True
            elif start[0] == (1 if self.player == 0 else 6) and\
                stop[0] == (3 if self.player == 0 else 4) and\
                self.board.grid[stop[0]][stop[1]].player == None and\
                self.board.grid[stop[0]][(start[0] + 1 if self.player == 0 else start[0] - 1)].player == None:
                return True
        elif start[1] == stop[1] + 1 or start[1] == stop[1] - 1:
            if stop[0] == start[0] + 1 - (2 * self.player) and\
                self.board.grid[stop[0]][stop[1]].player == (1 if self.player == 0 else 1):
                return True
        return False

        def postMove(self, stop):
            if stop[0] == (7 if self.player == 0 else 7):
                self.board.grid[stop[0]][stop[1]] = queen(self.board, self.player)

        def possibleMoves(self, pos):
            moves = []
            options = []
            if self.player == 0:
                options.append((pos[0] + 1, pos[1]))
                options.append((pos[0] + 1, pos[1] + 1))
                options.append((pos[0] + 1, pos[1] - 1))
                if pos[0] == 1:
                    options.append((pos[0] + 2, pos[1]))
            elif self.player == 1:
                options.append((pos[0] - 1, pos[1]))
                options.append((pos[0] - 1, pos[1] + 1))
                options.append((pos[0] - 1, pos[1] - 1))
                if pos[0] == 6:
                    options.append((pos[0] - 2, pos[1]))
            for move in options:
                if self.LegalMove(pos, move):
                    moves.append()
            return moves

class king(piece):
    def __str__(self):
        return "K" if self.player == 0 else "k"
    def LegalMove(self, start, stop):
        return (stop[0] == start[0] + 1 or stop[0] == start[0] - 1) and\
            (stop[1] == start[1] + 1 or stop[1] == start[1] - 1) and\
            self.board.grid[stop[0]][stop[1]].player != self.player

    def possibleMoves(self, pos):
        moves = []
        for x in [1, 0, -1]:
            for y in [1, 0, -1]:
                if pos[0] + y >= 0 and pos[0] + y <= 7 and\
                pos[1] + x >= 0 and pos[1] + x <= 7 and\
                self.LegalMove(pos, (pos[0] + y, pos[1] + x)):
                    moves.append((pos[0] + y, pos[1] + x))
        return moves

class queen(piece):
    def __str__(self):
        return "Q" if self.player == 0 else "q"
    def LegalMove(self, start, stop):
        if start[0] == stop[0]:
            if start[1] - stop[1] > 0:
                begin = stop[1]
                end = start[1]
            elif start[1] - stop[1] < 0:
                begin = start[1]
                end = stop[1]
            else:
                return False
            for i in range(begin + 1, end):
                if self.board.grid[stop[0]][i].player != None:
                    return False
            return self.board.grid[stop[0]][stop[1]].player != self.player

        elif start[1] == stop[1]:
            if start[0] - stop[0] > 0:
                begin = stop[0]
                end = start[0]
            elif start[0] - stop[0] < 0:
                begin = start[0]
                end = stop[0]
            else:
                return False
            for i in range(begin + 1, end):
                if self.board.grid[i][stop[1]].player != None:
                    return False
            return self.board.grid[stop[0]][stop[1]].player != self.player

        elif abs(start[0] - stop[0]) == abs(start[1] - stop[1]) and abs(start[1] - stop[1]) > 0:
            ym = (start[0] - stop[0]) / abs(start[0] - stop[0])
            xm = (start[1] - stop[1]) / abs(start[1] - stop[1])
            for i in range(1, abs(start[1] - stop[1])):
                if self.board.grid[start[0] + (ym * i)][start[1] + (xm * i)].player != None:
                    return False
            return self.board.grid[stop[0]][stop[1]].player != self.player
        else:
            return False
    def possibleMoves(self, pos):
        moves = []
        for x in [1, 0, -1]:
            for y in [1, 0, -1]:
                i = 1
                while pos[0] + (y * i) >= 0 and pos[0] + (y * i) <= 7 and\
                pos[1] + (x * i) >= 0 and pos[1] + (x * i) <= 7 and\
                self.LegalMove(pos, (pos[0] + (y * i), pos[1] + (x * i))):
                    moves.append[(pos[0] + (y * i), pos[1] + (x * i))]
                    i += 1
        return moves

class bishop(piece):
    def __str__(self):
        return "B" if self.player == 0 else "b"
    def LegalMove(self, start, stop):
        if abs(start[0] - stop[0]) == abs(start[1] - stop[1]) and abs(start[1] - stop[1]) > 0:
            ym = (start[0] - stop[0]) / abs(start[0] - stop[0])
            xm = (start[1] - stop[1]) / abs(start[1] - stop[1])
            for i in range(1, abs(start[1] - stop[1])):
                if self.board.grid[start[0] + (ym * i)][start[1] + (xm * i)].player != None:
                    return False
            return self.board.grid[stop[0]][stop[1]].player != self.player
        else:
            return False

    def possibleMoves(self, pos):
        moves = []
        for x in [1, -1]:
            for y in [1, -1]:
                i = 1
                while pos[0] + (y * i) >= 0 and pos[0] + (y * i) <= 7 and\
                pos[1] + (x * i) >= 0 and pos[1] + (x * i) <= 7 and\
                self.LegalMove(pos, (pos[0] + (y * i), pos[1] + (x * i))):
                    moves.append[(pos[0] + (y * i), pos[1] + (x * i))]
                    i += 1
        return moves

class rook(piece):
    def __str__(self):
        return "R" if self.player == 0 else "r"
    def LegalMove(self, start, stop):
        if start[0] == stop[0]:
            if start[1] - stop[1] > 0:
                begin = stop[1]
                end = start[1]
            elif start[1] - stop[1] < 0:
                begin = start[1]
                end = stop[1]
            else:
                return False
            for i in range(begin + 1, end):
                if self.board.grid[stop[0]][i].player != None:
                    return False
            return self.board.grid[stop[0]][stop[1]].player != self.player

        elif start[1] == stop[1]:
            if start[0] - stop[0] > 0:
                begin = stop[0]
                end = start[0]
            elif start[0] - stop[0] < 0:
                begin = start[0]
                end = stop[0]
            else:
                return False
            for i in range(begin + 1, end):
                if self.board.grid[i][stop[1]].player != None:
                    return False
            return self.board.grid[stop[0]][stop[1]].player != self.player
        else:
            return False

    def possibleMoves(self, pos):
        moves = []
        for (x, y) in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            i = 1
            while pos[0] + (y * i) >= 0 and pos[0] + (y * i) <= 7 and\
                pos[1] + (x * i) >= 0 and pos[1] + (x * i) <= 7 and\
                self.LegalMove(pos, (pos[0] + (y * i), pos[1] + (x * i))):
                    moves.append[(pos[0] + (y * i), pos[1] + (x * i))]
                    i += 1
        return moves

class knight(piece):
    def __str__(self):
        return "H" if self.player == 0 else "h"
    def LegalMove(self, start, stop):
        if (abs(start[0] - stop[0]) == 2 and abs(start[0] - stop[0]) == 1) or\
        (abs(start[0] - stop[0]) == 1 and abs(start[0] - stop[0]) == 2):
            return self.board.grid[stop[0]][stop[1]].player != self.player
        return False

    def possibleMoves(self, pos):
        moves = []
        for (x, y) in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            if self.LegalMove(pos, (pos[0] + y, pos[1] + x)):
                moves.append[(pos[0] + y, pos[1] + x)]
        return moves
