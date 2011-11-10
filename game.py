#!/usr/bin/python
#coding=utf8
"""
Created on Nov 10, 2011

@author: CVi
"""

import curses
from time import sleep
from board import board

message = "No Message"

def main(screen):
    gameBoard = board()
    drawBoard(screen)
    for row in range(8):
        for col in range(8):
           drawSquare(screen, col, row, str(gameBoard.grid[row][col]))
    winner = -1
    while not winner + 1:
        if gameBoard.check(gameBoard.player):
                screen.addstr(20, 1, "".join([" "] * 80))
                screen.addstr(20, 1, "Check player %s" % str(gameBoard.player + 1))
                screen.refresh()
                if gameBoard.mate():
                    global message
                    message = "Player %s, you lost." % str(gameBoard.player + 1)

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
                run = False
        run = True
        while run and not RS:
            event = screen.getch()
            if event >= ord("1") and event <= ord("8"):
                screen.addstr(chr(event).upper() + "-")
                sy = event - ord("1")
                run = False
        start = (sy, sx)
        run = True
        while run:
            event = screen.getch()
            if event >= ord("a") and event <= ord("h"):
                screen.addstr(chr(event).upper())
                sx = event - ord("a")
                run = False
        run = True
        while run:
            event = screen.getch()
            if event >= ord("1") and event <= ord("8"):
                screen.addstr(chr(event).upper())
                sy = event - ord("1")
                run = False
        stop = (sy, sx)

        if gameBoard.move(start, stop):
            if gameBoard.check(1 if gameBoard.player == 0 else 0):
                gameBoard.abort()
                screen.addstr(20, 1, "".join([" "] * 80))
                screen.addstr(20, 1, "Illegal Move - You can't check yourself")
            else:
                screen.addstr(20, 1, "".join([" "] * 80))
                screen.addstr(20, 1, "Move Completed")
                while len(gameBoard.dirty) > 0:
                    sq = gameBoard.dirty.pop()
                    drawSquare(screen, sq[1], sq[0], str(gameBoard.grid[sq[0]][sq[1]]))
                    screen.refresh()
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
    x = 6 + (col * 4)
    y = 2 + (row * 2)
    screen.addstr(y, x, char)
    screen.refresh()

def boolInput(txt):
    i = raw_input(txt + " Y/N").lower()
    while (i != "y") and (i != "n"):
        print "What does \"%s\" mean? type Y or N" % i
        i = raw_input(txt + " Y/N").lower()
    return True if i == "y" else False


while 1:
    curses.wrapper(main)
    print message
    if not boolInput("Another Game?"): break
