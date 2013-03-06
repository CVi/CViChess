#!/usr/bin/python
#coding=utf8
"""
Created on Nov 10, 2011

@author: CVi
"""

import curses
from time import sleep
from board import board

import syslog
syslog.openlog("Python")

message = "No Message"

def main(screen):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    gameBoard = board()
    drawBoard(screen)
    for row in range(8):
        for col in range(8):
           drawSquare(screen, col, row, str(gameBoard.grid[row][col]))
    winner = -1
    while not winner + 1:
        while len(gameBoard.dirty) > 0:
            sq = gameBoard.dirty.pop()
            drawSquare(screen, sq[1], sq[0], str(gameBoard.grid[sq[0]][sq[1]]))
            screen.refresh()

        if gameBoard.check(gameBoard.player):
                screen.addstr(20, 1, "".join([" "] * 80))
                screen.addstr(20, 1, "Check player %s" % str(gameBoard.player + 1))
                screen.refresh()
                curses.beep()
                if gameBoard.mate():
                    global message
                    message = "Player %s, you lost." % str(gameBoard.player + 1)
                    winner = 1 if gameBoard.player == 0 else 0

        screen.addstr(21, 1, "".join([" "] * 80))
        screen.addstr(21, 1, "Your move player %s: " % str(gameBoard.player + 1))
        screen.refresh()
        RS = False
        run = True
        while run:
            event = screen.getch()
            if event >= ord("a") and event <= ord("h"):
                screen.addstr(chr(event).upper())
                sx = event - ord("a")
                break
        while run and not RS:
            event = screen.getch()
            if event >= ord("1") and event <= ord("8"):
                screen.addstr(chr(event).upper() + "-")
                sy = event - ord("1")
                break
        start = (sy, sx)
        if gameBoard.grid[sy][sx].player != gameBoard.player:
            screen.addstr(20, 1, "".join([" "] * 80))
            screen.addstr(20, 1, "Not your piece")
            continue
        else:
            blinkSquare(screen, sx, sy, str(gameBoard.grid[sy][sx]))
            gameBoard.dirty.append(start)
            for move in gameBoard.grid[sy][sx].possibleMoves(start):
                gameBoard.dirty.append(move)
                if gameBoard.grid[move[0]][move[1]].player == None:
                    drawGreen(screen, move[1], move[0], "X")
                else:
                    drawRed(screen, move[1], move[0], str(gameBoard.grid[move[0]][move[1]]))
        while run:
            event = screen.getch()
            if event >= ord("a") and event <= ord("h"):
                screen.addstr(chr(event).upper())
                sx = event - ord("a")
                break

        for move in gameBoard.grid[start[0]][start[1]].possibleMoves(start):
            if move[1] == sx:
                if gameBoard.grid[move[0]][move[1]].player == None:
                    drawGreenBlink(screen, move[1], move[0], "X")
                else:
                    drawRedBlink(screen, move[1], move[0], str(gameBoard.grid[move[0]][move[1]]))
        while run:
            event = screen.getch()
            if event >= ord("1") and event <= ord("8"):
                screen.addstr(chr(event).upper())
                sy = event - ord("1")
                break
        stop = (sy, sx)

        if run and gameBoard.move(start, stop):
            if gameBoard.check(1 if gameBoard.player == 0 else 0):
                gameBoard.abort()
                screen.addstr(20, 1, "".join([" "] * 80))
                screen.addstr(20, 1, "Illegal Move - You can't check yourself")
                curses.flash()
            else:
                screen.addstr(20, 1, "".join([" "] * 80))
                screen.addstr(20, 1, "Move Completed")
                syslog.syslog(syslog.LOG_ALERT, str(start) + " " + str(stop))
        else:
            screen.addstr(20, 1, "Illegal Move %s-%s to %s-%s" % (start[0], start[1], stop[0], stop[1]))
    sleep(10)

def drawBoard(screen):
    screen.erase()
    div = "".join(["-"] * 41 + ["\n"])
    head = []
    for i in ["#", "A", "B", "C", "D", "E", "F", "G", "H", "#"]:
        head.append("| %s " % i)
    head.append("|\n")
    head = "".join(head)

    rows = []
    for i in range(1, 9):
        rows.append("".join(["| %s " % i] + ["|   "] * 8 + ["| %s |" % i] + ["\n"]))

    screen.addstr(0, 0, div.join([head] + rows + [head]))
    screen.refresh()

def drawSquare(screen, col, row, char):
    x = 5 + (col * 4)
    y = 2 + (row * 2)
    screen.addstr(y, x, char)
    screen.refresh()

def blinkSquare(screen, col, row, char):
    mypos = screen.getyx()
    x = 5 + (col * 4)
    y = 2 + (row * 2)
    screen.addstr(y, x, char, curses.A_BLINK)
    screen.move(mypos[0], mypos[1])
    screen.refresh()

def drawRed(screen, col, row, char):
    mypos = screen.getyx()
    x = 5 + (col * 4)
    y = 2 + (row * 2)
    screen.addstr(y, x, char, curses.color_pair(1))
    screen.move(mypos[0], mypos[1])
    screen.refresh()

def drawGreen(screen, col, row, char):
    mypos = screen.getyx()
    x = 6 + (col * 4)
    y = 2 + (row * 2)
    screen.addstr(y, x, char, curses.color_pair(2))
    screen.move(mypos[0], mypos[1])
    screen.refresh()

def drawRedBlink(screen, col, row, char):
    mypos = screen.getyx()
    x = 5 + (col * 4)
    y = 2 + (row * 2)
    screen.attron(curses.A_REVERSE)
    screen.attron(curses.color_pair(1))
    screen.addstr(y, x, char)
    screen.move(mypos[0], mypos[1])
    screen.refresh()
    screen.attroff(curses.A_REVERSE)
    screen.attroff(curses.color_pair(1))

def drawGreenBlink(screen, col, row, char):
    mypos = screen.getyx()
    x = 6 + (col * 4)
    y = 2 + (row * 2)
    screen.attron(curses.A_REVERSE)
    screen.attron(curses.color_pair(2))
    screen.addstr(y, x, char)
    screen.move(mypos[0], mypos[1])
    screen.refresh()
    screen.attroff(curses.A_REVERSE)
    screen.attroff(curses.color_pair(2))

def boolInput(txt):
    i = raw_input(txt + " Y/N").lower()
    while (i != "y") and (i != "n"):
        print "What does \"%s\" mean? type Y or N" % i
        i = raw_input(txt + " Y/N").lower()
    return True if i == "y" else False

if __name__ == "__main__":
    while True:
        curses.wrapper(main)
        print message
        if not boolInput("Another Game?"): break
