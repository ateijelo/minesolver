#!/usr/bin/env python3

import itertools
import random

#a set of mines...

class UserBoard:
    def __init__(self,width,height,minecount):
        self.w = width
        self.h = height

        self.mines = []
        for x in range(self.w):
            self.mines.append([0] * self.h)
        self._minecount = minecount

        self.covers = []
        for x in range(self.w):
            self.covers.append([1] * self.h)

        self.flagcount = 0

    def minecount(self):
        return self._minecount

    def minesleft(self):
        return self._minecount - self.flagcount

    def set(self,x,y,n):
        self.mines[x][y] = n
        self.covers[x][y] = 0

    def __str__(self):
        s = ""
        md = {-1:'■',0:' '} # mine dict
        cw = 3 # content width
        for y in range(self.h-1,-1,-1):
            for x in range(self.w):
                if x==0:
                    if y==self.h-1:
                        if self.covered(x,y):
                            s += '┏'
                        else:
                            s += '┌'
                    else:
                        t = (self.covered(x,y+1),
                             self.covered(x,y))
                        d = {(True,True):'┣',
                             (True,False):'┡',
                             (False,True):'┢',
                             (False,False):'│'}
                        s += d[t]
                if x==self.w-1:
                    if y==self.h-1:
                        if self.covered(x,y):
                            s += '━'*cw+'┓'
                        else:
                            s += '─'*cw+'┐'
                    else:
                        if self.covered(x,y) or\
                           self.covered(x,y+1):
                            s += '━'*cw
                        else:
                            s += ' '*cw
                        t = (self.covered(x,y+1),
                             self.covered(x,y))
                        d = {(True,True):'┫',
                             (True,False):'┩',
                             (False,True):'┪',
                             (False,False):'│'}
                        s += d[t]
                else:
                    if y==self.h-1:
                        if self.covered(x,y):
                            s += '━'*cw
                        else:
                            s += '─'*cw
                        t = (self.covered(x,y),
                             self.covered(x+1,y))
                        d = {(True,True):'┳',
                             (True,False):'┱',
                             (False,True):'┲',
                             (False,False):'─'}
                        s += d[t]
                    else:
                        if self.covered(x,y) or\
                           self.covered(x,y+1):
                            s += '━'*cw
                        else:
                            s += ' '*cw
                        t = (1 if self.covered(x,y) else 0,
                             1 if self.covered(x+1,y) else 0,
                             1 if self.covered(x,y+1) else 0,
                             1 if self.covered(x+1,y+1) else 0)
                        d = {(1,1,1,1):'╋',
                             (1,1,1,0):'╋',
                             (1,1,0,1):'╋',
                             (1,1,0,0):'┳',
                             (1,0,1,1):'╋',
                             (1,0,1,0):'┫',
                             (1,0,0,1):'╋',
                             (1,0,0,0):'┓',
                             (0,1,1,1):'╋',
                             (0,1,1,0):'╋',
                             (0,1,0,1):'┣',
                             (0,1,0,0):'┏',
                             (0,0,1,1):'┻',
                             (0,0,1,0):'┛',
                             (0,0,0,1):'┗',
                             (0,0,0,0):' '}
                        s += d[t]
            s += '\n'
            for x in range(self.w):
                mv = self.mines[x][y]
                mc = "{0}".format(md.get(mv,mv)).center(cw)
                cv = self.covers[x][y]
                if cv == 2:
                    mc = '⚑'.center(cw)
                elif cv == 1:
                    mc = ' '.center(cw)

                if x==0:
                    s += '┃' if self.covered(x,y) else '│'
                if x==self.w-1:
                    s += mc + ('┃' if self.covered(x,y) else '│')
                else:
                    s += mc + ('┃' if self.covered(x,y) or
                                  self.covered(x+1,y) else ' ')
            s += '\n'
        # last line
        for x in range(self.w):
            if x==0:
                if self.covered(x,0):
                    s += '┗'
                else:
                    s += '└'
            if x==self.w-1:
                if self.covered(x,0):
                    s += '━'*cw+'┛'
                else:
                    s += '─'*cw+'┘'
            else:
                if self.covered(x,0):
                    s += '━'*cw
                    if self.covered(x+1,0):
                        s += '┻'
                    else:
                        s += '┹'
                else:
                    s += '─'*cw
                    if self.covered(x+1,0):
                        s += '┺'
                    else:
                        s += '─'
        return s

    def neighbours(self,x,y):
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                if dx == dy == 0:
                    continue
                if x+dx < 0 or x+dx >= self.w:
                    continue
                if y+dy < 0 or y+dy >= self.h:
                    continue
                yield (x+dx,y+dy)

    def covered(self,x,y):
        return (self.covers[x][y] > 0)

    def uncovered(self,x,y):
        return not self.covered(x,y)

    def covered_neighbours(self,x,y):
        for nx,ny in self.neighbours(x,y):
            if self.covered(nx,ny):
                yield (nx,ny)

    def covered_unflagged_neighbours(self,x,y):
        for nx,ny in self.covered_neighbours(x,y):
            if not self.flagged(nx,ny):
                yield (nx,ny)

    def flagged(self,x,y):
        return self.covers[x][y] == 2

    def flag(self,x,y):
        self.covers[x][y] = 2
        self.flagcount += 1

    def unflag(self,x,y):
        self.covers[x][y] = 1
        self.flagcount -= 1

    def uncovered_numbers(self):
        for y in range(self.h):
            for x in range(self.w):
                if self.uncovered(x,y) and self.mines[x][y] > 0:
                    yield x,y

    def neighbour_mines_left(self,x,y):
        r = self.value(x,y)
        for nx,ny in self.neighbours(x,y):
            if self.flagged(nx,ny):
                r -= 1
        return r

    def value(self,x,y):
        return self.mines[x][y]

class MineField:
    """
    This class represents the state of a board at some point during the game.
    It has a readonly lower layer of mines, set on the constructor
    and a top layer of covers that can be absent, unflagged and flagged.

    In the lower layer of the board, with the mines and the numbers:
    -1 represents a mine.
    >=0 represents the number of neighbouring mines

    In the upper layer of the board, with the covers:
    0 represents no cover
    1 represents covered and without flag
    2 represents covered and with flag
    This layers starts will all cells covered and unflagged, as in the game.
    """

    def __init__(self,width,height,mines):
        self.w = width
        self.h = height

        self.mines = []
        self.mineset = set(mines)

        for x in range(self.w):
            self.mines.append([0] * self.h)

        for x,y in mines:
            self.mines[x][y] = -1
            for nx,ny in self.neighbours(x,y):
                if (nx,ny) in mines:
                    continue
                self.mines[nx][ny] += 1

        self.covers = []
        for x in range(self.w):
            self.covers.append([1] * self.h)

        self.flagcount = 0

    def minecount(self):
        return len(self.mineset)

    def minesleft(self):
        return len(self.mineset) - self.flagcount

    def __str__(self):
        s = ""
        md = {-1:'■',0:' '} # mine dict
        cw = 3 # content width
        for y in range(self.h-1,-1,-1):
            for x in range(self.w):
                if x==0:
                    if y==self.h-1:
                        if self.covered(x,y):
                            s += '┏'
                        else:
                            s += '┌'
                    else:
                        t = (self.covered(x,y+1),
                             self.covered(x,y))
                        d = {(True,True):'┣',
                             (True,False):'┡',
                             (False,True):'┢',
                             (False,False):'│'}
                        s += d[t]
                if x==self.w-1:
                    if y==self.h-1:
                        if self.covered(x,y):
                            s += '━'*cw+'┓'
                        else:
                            s += '─'*cw+'┐'
                    else:
                        if self.covered(x,y) or\
                           self.covered(x,y+1):
                            s += '━'*cw
                        else:
                            s += ' '*cw
                        t = (self.covered(x,y+1),
                             self.covered(x,y))
                        d = {(True,True):'┫',
                             (True,False):'┩',
                             (False,True):'┪',
                             (False,False):'│'}
                        s += d[t]
                else:
                    if y==self.h-1:
                        if self.covered(x,y):
                            s += '━'*cw
                        else:
                            s += '─'*cw
                        t = (self.covered(x,y),
                             self.covered(x+1,y))
                        d = {(True,True):'┳',
                             (True,False):'┱',
                             (False,True):'┲',
                             (False,False):'─'}
                        s += d[t]
                    else:
                        if self.covered(x,y) or\
                           self.covered(x,y+1):
                            s += '━'*cw
                        else:
                            s += ' '*cw
                        t = (1 if self.covered(x,y) else 0,
                             1 if self.covered(x+1,y) else 0,
                             1 if self.covered(x,y+1) else 0,
                             1 if self.covered(x+1,y+1) else 0)
                        d = {(1,1,1,1):'╋',
                             (1,1,1,0):'╋',
                             (1,1,0,1):'╋',
                             (1,1,0,0):'┳',
                             (1,0,1,1):'╋',
                             (1,0,1,0):'┫',
                             (1,0,0,1):'╋',
                             (1,0,0,0):'┓',
                             (0,1,1,1):'╋',
                             (0,1,1,0):'╋',
                             (0,1,0,1):'┣',
                             (0,1,0,0):'┏',
                             (0,0,1,1):'┻',
                             (0,0,1,0):'┛',
                             (0,0,0,1):'┗',
                             (0,0,0,0):' '}
                        s += d[t]
            s += '\n'
            for x in range(self.w):
                mv = self.mines[x][y]
                mc = "{0}".format(md.get(mv,mv)).center(cw)
                cv = self.covers[x][y]
                if cv == 2:
                    mc = '⚑'.center(cw)
                elif cv == 1:
                    mc = ' '.center(cw)

                if x==0:
                    s += '┃' if self.covered(x,y) else '│'
                if x==self.w-1:
                    s += mc + ('┃' if self.covered(x,y) else '│')
                else:
                    s += mc + ('┃' if self.covered(x,y) or
                                  self.covered(x+1,y) else ' ')
            s += '\n'
        # last line
        for x in range(self.w):
            if x==0:
                if self.covered(x,0):
                    s += '┗'
                else:
                    s += '└'
            if x==self.w-1:
                if self.covered(x,0):
                    s += '━'*cw+'┛'
                else:
                    s += '─'*cw+'┘'
            else:
                if self.covered(x,0):
                    s += '━'*cw
                    if self.covered(x+1,0):
                        s += '┻'
                    else:
                        s += '┹'
                else:
                    s += '─'*cw
                    if self.covered(x+1,0):
                        s += '┺'
                    else:
                        s += '─'
        return s

    def neighbours(self,x,y):
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                if dx == dy == 0:
                    continue
                if x+dx < 0 or x+dx >= self.w:
                    continue
                if y+dy < 0 or y+dy >= self.h:
                    continue
                yield (x+dx,y+dy)

    def setelements(self,matrix):
        for x in range(self.w):
            for y in range(self.h):
                self.b[x][y] = matrix[x][y]

    def covered(self,x,y):
        return (self.covers[x][y] > 0)

    def uncovered(self,x,y):
        return not self.covered(x,y)

    def covered_neighbours(self,x,y):
        for nx,ny in self.neighbours(x,y):
            if self.covered(nx,ny):
                yield (nx,ny)

    def covered_unflagged_neighbours(self,x,y):
        for nx,ny in self.covered_neighbours(x,y):
            if not self.flagged(nx,ny):
                yield (nx,ny)

    def rightclick(self,x,y):
        if self.flagged(x,y):
            self.unflag(x,y)
        else:
            self.flag(x,y)

    def flagged(self,x,y):
        return self.covers[x][y] == 2

    def flag(self,x,y):
        self.covers[x][y] = 2
        self.flagcount += 1

    def unflag(self,x,y):
        self.covers[x][y] = 1
        self.flagcount -= 1

    def leftclick(self,x,y):
        return self.uncover(x,y)

    def uncover(self,x,y):
        self.covers[x][y] = 0
        while True:
            finish = True
            for y in range(self.h):
                for x in range(self.w):
                    if self.covered(x,y):
                        continue
                    if self.mines[x][y] != 0:
                        continue
                    for nx,ny in self.covered_neighbours(x,y):
                        self.covers[nx][ny] = 0
                        finish = False
            if finish:
                break

    def uncovered_numbers(self):
        for y in range(self.h):
            for x in range(self.w):
                if self.uncovered(x,y) and self.mines[x][y] > 0:
                    yield x,y

    def neighbour_mines_left(self,x,y):
        r = self.value(x,y)
        for nx,ny in self.neighbours(x,y):
            if self.flagged(nx,ny):
                r -= 1
        return r

    def value(self,x,y):
        return self.mines[x][y]

def valid(sol,board,cells):
    """Is this solution valid for the given cells on the given board?"""
    if len(sol) > board.minesleft():
        return False
    d = {}
    for c in cells:
        d[c] = 0
    for mx,my in sol:
        #print("mx,my:",mx,my)
        for cx,cy in cells:
            #print("cx,cy:",cx,cy)
            if cx==mx and cy==my:
                continue
            if abs(cx-mx) in (1,0,-1) and abs(cy-my) in (1,0,-1):
                d[(cx,cy)] += 1
        #print(d)

    for cx,cy in d:
        if d[(cx,cy)] != board.neighbour_mines_left(cx,cy):
            return False
    return True

def printsol(sol,board):
    flags = {}
    for cx,cy in sol:
        flags[(cx,cy)] = board.flagged(cx,cy)
        board.flag(cx,cy)
    print(board)
    for cx,cy in sol:
        if not flags[(cx,cy)]:
            board.unflag(cx,cy)

def advance(board):
    # A solution is a set of mines
    allsols = set()
    cells = set()
    first = True
    for nx,ny in board.uncovered_numbers():
        cells.add((nx,ny))
        cellsols = itertools.combinations(board.covered_unflagged_neighbours(nx,ny),board.neighbour_mines_left(nx,ny))
        newsols = set()
        for c in cellsols:
            for a in allsols:
                newsols.add(tuple(set(c).union(a)))
            if len(allsols) == 0:
                newsols.add(c)
        allsols = newsols
        #print("cells:",cells)
        #print("allsols:",allsols)
        #for sol in allsols:
        #    printsol(sol,board)
        validsols = set(s for s in allsols if valid(s,board,cells))
        #print("validsols:",validsols)
        #for sol in validsols:
        #    printsol(sol,board)
        allsols = validsols
    edge = set()
    for nx,ny in board.uncovered_numbers():
        for cx,cy in board.covered_unflagged_neighbours(nx,ny):
            edge.add((cx,cy))
    mines = set()
    spaces = set()
    for x,y in edge:
        count = 0
        for sol in allsols:
            if (x,y) in sol:
                count += 1
        if count == len(allsols):
            mines.add((x,y))
        elif count == 0:
            spaces.add((x,y))
    return mines,spaces

def solve(board):
    while board.minesleft() > 0:
        mines,spaces = advance(board)
        if len(mines) == len(spaces) == 0:
            return False
        for x,y in mines:
            board.flag(x,y)
        for x,y in spaces:
            board.uncover(x,y)
    else:
        return True

def generate(width,height,minecount,start):
    s = set(itertools.product(range(width),range(height)))
    x,y = start
    for dx,dy in itertools.product((-1,0,1),repeat=2):
        s.difference_update(((x+dx,y+dy),))
    mines = set(random.sample(s,minecount))
    b = MineField(width,height,mines)
    b.uncover(x,y)
    return b

if __name__=="__main__":
    while True:
        print("Generating...")
        b = generate(8,8,10,(0,0))
        print("Trying to solve... ")
        if solve(b):
            print(b)
            break
        print("Unsolvable:")
        print(b)
    #b = MineField(8,8,set(((0,3),(1,6),(2,0),(2,2),(3,5),(4,1),(4,6),(5,3),(6,1),(7,5))))
    #b = generate(15,15,30,(0,0))
    #b.uncover(7,7)
    #print(b)
    #b = MineField(8,8,set(((0,3),(1,6),(2,0),(2,2),(3,5),(4,1),(4,6),(7,5))))
    #print(b)
    #b.uncover(7,7)
    #mines,spaces = advance(b)
    #for x,y in mines:
    #    b.flag(x,y)
    #for x,y in spaces:
    #    b.uncover(x,y)
    #print(b)
    #b.uncover(6,5)
    #b.uncover(5,5)
    #b.uncover(4,5)
    #b.flag(7,5)
    #print(valid(((6,4),(3,4),(3,5)),b,((4,5),(5,5),(6,5))))
    #import pdb
    #pdb.set_trace()
    #print("Sol:",((4,6),(7,5)))
    #print("Cells:",{(5,6),(6,6)})
    #print(valid(((4,6),(7,5)),b,{(5,6),(6,6)}))
