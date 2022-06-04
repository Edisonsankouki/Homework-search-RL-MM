import random

random.seed(42)
import copy
from optparse import OptionParser
import util


class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        """
        Value 1 indicates the position of queen
        """
        self.numberOfRuns = numberOfRuns
        self.verbose = verbose
        self.lectureCase = [[]]
        if lectureExample:
            self.lectureCase = [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [1, 0, 0, 0, 1, 0, 0, 0],
                [0, 1, 0, 0, 0, 1, 0, 1],
                [0, 0, 1, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]

    def solve(self):
        solutionCounter = 0
        for i in range(self.numberOfRuns):
            if self.search(Board(self.lectureCase), self.verbose).getNumberOfAttacks() == 0:
                solutionCounter += 1
        print("Solved: %d/%d" % (solutionCounter, self.numberOfRuns))

    def search(self, board, verbose):
        """
        Hint: Modify the stop criterion in this function
        """
        newBoard = board
        i = 0
        consecutiveMoves = 0
        while True:
            if verbose:
                print("iteration %d" % i)
                print(newBoard.toString())
                print("# attacks: %s" % str(newBoard.getNumberOfAttacks()))
                print(newBoard.getCostBoard().toString(True))
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()

            "when reach the goal (no attacks)"
            if 0 == currentNumberOfAttacks:
                break

            (newBoard, newNumberOfAttacks, newRow, newCol) = newBoard.getBetterBoard()
            i += 1

            "allow up to 100 consecutive moves"
            if currentNumberOfAttacks < newNumberOfAttacks:
                break
            if currentNumberOfAttacks == newNumberOfAttacks:
                if consecutiveMoves > 100:
                    break
                consecutiveMoves += 1
            if currentNumberOfAttacks > newNumberOfAttacks:
                consecutiveMoves = 0

        return newBoard


class Board:
    def __init__(self, squareArray=[[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray

    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [[0 for i in range(8)] for j in range(8)]
        for i in range(8):
            tmpSquareArray[random.randint(0, 7)][i] = 1
        return tmpSquareArray

    def toString(self, isCostBoard=False):
        """
        Transform the Array in Board or cost Board to printable string
        """
        s = ""
        for i in range(8):
            for j in range(8):
                if isCostBoard:  # Cost board
                    cost = self.squareArray[i][j]
                    s = (s + "%3d" % cost) if cost < 9999 else (s + "  q")
                else:  # Board
                    s = (s + ". ") if self.squareArray[i][j] == 0 else (s + "q ")
            s += "\n"
        return s

    def getCostBoard(self):
        """
        First Initalize all the cost as 9999.
        After filling, the position with 9999 cost indicating the position of queen.
        """
        costBoard = Board([[9999 for i in range(8)] for j in range(8)])
        for r in range(8):
            for c in range(8):
                if self.squareArray[r][c] == 1:
                    for rr in range(8):
                        if rr != r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = 0
                            testboard.squareArray[rr][c] = 1
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        from numpy.random import randint
        costBoard = self.getCostBoard()
        betterBoard = copy.deepcopy(self)
        minNumOfAttack = int(min([y for x in costBoard.squareArray for y in x ]))
        argmins = []
        for r in range(8):
            for c in range(8):
                if costBoard.squareArray[r][c] == minNumOfAttack:
                    argmins.append((r, c))
        argmin = argmins[randint(len(argmins))]
        newRow, newCol = argmin
        for r in range(8):
            if 1 == betterBoard.squareArray[r][newCol]:
                betterBoard.squareArray[r][newCol] = 0
        betterBoard.squareArray[newRow][newCol] = 1
        return (betterBoard, minNumOfAttack, newRow, newCol)




    def getNumberOfAttacks(self):
        attack = 0
        for x in range(0,8):
            for y in range(0,8):
                if self.squareArray[x][y] == 1:
                    horizon = []
                    vertical = []
                    rightslope = []
                    leftslope = []
                    for y1 in range(0,8):
                        if y1 != y:
                            vertical.append((x,y1))
                    for x1 in range(0,8):
                        if x1 != x:
                            horizon.append((x1,y))
                    rbias = y-x
                    lbias = y+x
                    for x2 in range(0,8):
                        y2 = x2+rbias
                        if x2!=x and y2!=y and x2<8 and x2>=0 and y2 < 8 and y2 >=0:
                            rightslope.append((x2,y2))
                    for x3 in range(0,8):
                        y3 = -x3+lbias
                        if x3!=x and y3!=y and x3<8 and y3<8 and y3>=0 and x3>=0:
                            leftslope.append((x3,y3))
                    for a in horizon:
                        if self.squareArray[a[0]][a[1]] == 1:
                            attack+=1
                    for b in vertical:
                        if self.squareArray[b[0]][b[1]] == 1:
                            attack+=1
                    for c in rightslope:
                        if self.squareArray[c[0]][c[1]] == 1:
                            attack+=1
                    for d in leftslope:
                        if self.squareArray[d[0]][d[1]] == 1:
                            attack+=1

        return int(attack/2)




if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    random.seed(1)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    EightQueensAgent = SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)
    EightQueensAgent.solve()
