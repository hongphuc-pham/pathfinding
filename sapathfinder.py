from collections import deque
from sys import argv
import numpy as np
import random as rand
import math as mt

# Get arguments
## File name
# Get arguments
mapFile = argv[1]
# specifies the initial path to a map
init = argv[2]
#  initial  temperature
tini = float(argv[3])
#  final temperature
tfin = float(argv[4])
#  cooling rate
alpha = float(argv[5])
# segment length
d = int(argv[6])


# mapFile = open(map, "r")
with open(mapFile) as infile_object:
    lines = infile_object.read().splitlines()

# Generate 2D array map
rowSize = int(lines[0].split(" ")[0])
colSize = int(lines[0].split(" ")[1])
map = np.empty((rowSize, colSize), str)

# Create a 2D map array
for pointer in range(3, len(lines)):
    col = 0
    for char in lines[pointer].split(" "):
        map[pointer-3][col] = char
        col += 1



# Function to check if a next point
# is be visited or not and valid
def isValid( row, col,vistedMap):
    # Check if cell is not on map
    if (row < 0 or col < 0 or row >= rowSize or col >= colSize):
        return False

    # Check if cell is already visited
    if (vistedMap[row][col]):
        return False

    if ( map[row][col].lower() == 'x'):
        return False

    # Otherwise
    return True


class Point:
    g = 0.0
    head = None
    def __init__(self, x: float, y: float, val: float):
        self.x = x
        self.y = y
        self.val = val

    def __lt__(self, other):
        return self.g < other.g

    def __eq__(self, other):
        if (isinstance(other, Point)):
            return (self.x, self.y) == (other.x, other.y)
        return False

    def addHead(self, pt):
        assert isinstance(pt, Point)
        self.head = pt


    def addG(self, g: float):
        self.g = g

    def updatePoint(self, parent, gcost: int):
        self.head = parent
        self.g = gcost


#Calculate cost
def calculateCost(curr: Point, next: Point):

    if(curr.val < next.val):
        return 1.0 + next.val - curr.val

    return 1.0


# Print map function
def printMap(map):
    for i in range (0, rowSize):
        for j in range (0, colSize):
            if(j == colSize -1):
                print(map[i][j])
            else:
                print(map[i][j], end = ' ')


def resetVisit(map):
    map = [[False for i in range(colSize)] for i in range(rowSize)][:]


# These arrays are used to get next cells in 4 direction Up, Down, Left Right
rowNum = [-1, 1, 0, 0]
colNum = [0, 0, -1, 1]

# Get start and end point corr by extracting text file
startX = int(lines[1].split(" ")[0]) -1
startY = int(lines[1].split(" ")[1]) -1
endX = int(lines[2].split(" ")[0]) -1
endY = int(lines[2].split(" ")[1]) -1
# Init start and end variable
start = Point(startX, startY, int(map[startX][startY]))
end = Point(endX, endY, int(map[endX][endY]))


def changeDirectionOrder():
    directionL = ['U', 'D', 'R','L']

    for i in range(0,4):
        direct = directionL.pop(rand.randrange(len(directionL)))

        if direct == 'U':
            rowNum[i] = -1
            colNum[i] = 0
        elif direct == 'D':
            rowNum[i] = 1
            colNum[i] = 0
        elif direct == 'L':
            rowNum[i] = 0
            colNum[i] = -1
        elif direct == 'R':
            rowNum[i] = 0
            colNum[i] = 1

def visitedMapGenerator():
    return [[False for i in range(colSize)] for i in range(rowSize)]

# Breadth first search function
def bfs(start: Point, end: Point, vMap):

    # Marked start point
    vMap[start.x][start.y] = True

    # Create a queue
    q = []

    # Distance of start point(or cell) is 0
    q.append(start)  # Enqueue start point( or cell)

    while q:

        curr = q.pop(0)  # Dequeue the front point

        if curr.x == end.x and curr.y == end.y:
            return curr


        # Otherwise enqueue its neighbour points
        for i in range(4):
            row = curr.x + rowNum[i]
            col = curr.y + colNum[i]

            # if neighbour point is valid, has path
            # and not visited yet, enqueue it.
            if (isValid(row, col,vMap)):
                vMap[row][col] = True
                childPoint = Point(row, col, int(map[row][col]))
                childPoint.addHead(curr)
                childPoint.addG(curr.g + calculateCost(curr,childPoint))
                q.append(childPoint)

        # Return -1 if destination cannot be reached

    return Point(endX + 1,endY + 1 ,endX)


def pathToList(pt: Point):
    sequence = []
    path = deque()
    path.append(pt)
    while path:
        pointer = path.popleft()
        sequence.append(pointer)
        if(isinstance(pointer, Point)):
            path.append(pointer.head)
        else:
            break

    return sequence[0:len(sequence) -1]

def updateVisited(vMap, path, sBreak, eBreak):

    for i in range(0, len(path)):
        if( i < sBreak  or i > eBreak):
            vMap[path[i].x][path[i].y] = True


def randomPathAjust(path, d: int,):

    randNo = rand.randint(0,len(path) - 1)
    endNo = randNo + d if randNo + d < len(path) else len(path) - 1
    vMap = visitedMapGenerator()

    sPoint = path[randNo]
    ePoint = path[endNo]

    resetVisit(vMap)
    updateVisited(vMap, path, randNo, endNo)

    newPath = pathToList(bfs(sPoint, ePoint,vMap))[::-1]

    if(endNo != len(path) - 1 ):
        rightPart = path[endNo + 1: len(path)]
        previousNode = newPath[len(newPath) - 1]
        for node in rightPart:
            if(isinstance(previousNode, Point)):
                node.updatePoint(previousNode, previousNode.g + calculateCost(previousNode,node))

                newPath.append(node)
                previousNode = node

    return newPath

def annealing(path, tList, cList):
    current_temp = tini
    current = path

    while current_temp > tfin:

        tList.append(current_temp)
        cList.append(current[len(current) - 1].g)

        # Random direction
        changeDirectionOrder()
        propose = randomPathAjust(current, d)
        costDiff = current[len(current) - 1].g - propose[len(propose) - 1].g

        if costDiff > 0:
            current = propose
        else:
            try:
                if(rand.uniform(0,1)< mt.exp(costDiff/current_temp)):
                    current = propose
            except OverflowError:
                if (rand.uniform(0,1) < float('inf')):
                    current = propose


        current_temp *= alpha


    return current

# Driver code
def main():
    vistedMap = visitedMapGenerator()

    path = pathToList(bfs(start, end, vistedMap))[::-1]

    temperature, cost = [],[]

    optimised = annealing(path, temperature, cost)

    # Print map and tempList and costList
    for pt in optimised:
        map[pt.x][pt.y] = "*"

    printMap(map)

    for i in range(0,len(temperature)):
        print('T = {temp:.6f}, cost = {cost}'.format(temp = temperature[i], cost = int(cost[i])))


main()