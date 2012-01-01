#!/usr/bin/env python3

import itertools

#a set of mines...

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
                        s += '┌'
                    else:
                        s += '├'
                if x==self.w-1:
                    if y==self.h-1:
                        s += '─'*cw+'┐'
                    else:
                        s += '─'*cw+'┤'
                else:
                    if y==self.h-1:
                        s += '─'*cw+'┬'
                    else:
                        s += '─'*cw+'┼'
            s += '\n'
            for x in range(self.w):
                mv = self.mines[x][y]
                mc = "{0}".format(md.get(mv,mv)).center(cw)
                cv = self.covers[x][y]
                if cv == 2:
                    mc = '⚐'.center(cw)
                elif cv == 1:
                    mc = '_'.center(cw)

                if x==0:
                    s += '│'
                s += mc + '│'
            s += '\n'
        for x in range(self.w):
            if x==0:
                s += '└'
            if x==self.w-1:
                s += '─'*cw+'┘'
            else:
                s += '─'*cw+'┴'
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
        for cx,cy in cells:
            if cx==mx and cy==my:
                continue
            if abs(cx-mx) in (1,0,-1) and abs(cy-my) in (1,0,-1):
                d[(cx,cy)] += 1

    for cx,cy in d:
        if d[(cx,cy)] != board.value(cx,cy):
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
        cellsols = itertools.combinations(board.covered_unflagged_neighbours(nx,ny),board.value(nx,ny))
        newsols = set()
        for c in cellsols:
            for a in allsols:
                newsols.add(tuple(set(c).union(a)))
            if len(allsols) == 0:
                newsols.add(c)
        allsols = newsols
        #print("cells:",cells)
        #print("allsols:",allsols)
        validsols = set(s for s in allsols if valid(s,board,cells))
        print("validsols:",validsols)
        for sol in validsols:
            printsol(sol,board)
        allsols = validsols

if __name__=="__main__":
    b = MineField(8,8,set(((0,3),(1,6),(2,0),(2,2),(3,5),(4,1),(4,6),(5,3),(6,1),(7,5))))
    #b = MineField(8,8,set(((0,3),(1,6),(2,0),(2,2),(3,5),(4,1),(4,6),(7,5))))
    #b.leftclick(7,3)
    b.leftclick(7,7)
    print(b)
    advance(b)
    #import pdb
    #pdb.set_trace()
    #print("Sol:",((4,6),(7,5)))
    #print("Cells:",{(5,6),(6,6)})
    #print(valid(((4,6),(7,5)),b,{(5,6),(6,6)}))
