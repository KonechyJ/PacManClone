import pygame
from vector import Vector2
from constants import *
from stack import Stack

#The node class to handle all the functionality for each node
class Node(object):
    #these below take in row and col and assign them to tile height and length
    def __init__(self, row, column):
        self.row, self.column = row, column
        self.position = Vector2(column*tileWidth, row*tileHeight)
        #this dictionary is to store the next nodes pacman can go to
        self.neighbors = {UP: None, DOWN: None, LEFT: None, RIGHT: None}
        #variables for the side portals
        self.portalNode = None
        self.portalVal = 0
        self.homeGuide = False
        self.homeEntrance = False
        self.spawnNode = False
        self.pacmanStartNode = False
        self.blinkyStartNode = False
        self.pinkyStartNode = False
        self.inkyStartNode = False
        self.clydeStartNode = False
        self.fruitStartNode = False


    #this render will draw the nodes to the screen
    def render(self, screen):
        #for the number of neighbors and if there are neighbor nodes,
        #then draw them as red dots and connect them with white lines
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.position.asTuple()
                line_end = self.neighbors[n].position.asTuple()
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)
                pygame.draw.circle(screen, RED, self.position.asInt(), 12)

#This class simple creates an object to hold all the nodes
class NodeGroup(object):
    def __init__(self, level):
        self.nodeList = []
        self.homeList = []
        self.level = level
        self.nodeStack = Stack()
        self.portalSymbols = ["1", "2"]
        self.nodeSymbols = ["+", "H", "S", "P", "B", "I", "C", "F"] + self.portalSymbols
        self.grid = self.readMazeFile(level)
        self.homegrid = self.getHomeArray()
        self.createNodeList(self.grid, self.nodeList)
        self.createNodeList(self.homegrid, self.homeList)
        self.setupPortalNodes()
        self.moveHomeNodes()
        self.homeList[0].homeEntrance = True

    #this function will read in the text file to create the ,maze
    def readMazeFile(self, textfile):
        f = open(textfile, "r")
        lines = [line.rstrip('\n') for line in f]
        lines = [line.rstrip('\r') for line in lines]
        return [line.split(' ') for line in lines]

    #This method first finds the first node and then runs a loop as long as the stack is not empty
    # Then we pop that node off the stack and add it to node list
    #Then the function finds all the neighbors of the node until the stack is empty
    def createNodeList(self, grid, nodeList):
        # self.grid = self.readMazeFile(textFile)
        # startNode = self.findFirstNode(len(self.grid), len(self.grid[0]))
        startNode = self.findFirstNode(grid)
        self.nodeStack.push(startNode)
        while not self.nodeStack.isEmpty():
            node = self.nodeStack.pop()
            self.addNode(node, nodeList)
            leftNode = self.getPathNode(LEFT, node.row, node.column - 1, nodeList, grid)
            rightNode = self.getPathNode(RIGHT, node.row, node.column + 1, nodeList, grid)
            upNode = self.getPathNode(UP, node.row - 1, node.column, nodeList, grid)
            downNode = self.getPathNode(DOWN, node.row + 1, node.column, nodeList, grid)
            node.neighbors[LEFT] = leftNode
            node.neighbors[RIGHT] = rightNode
            node.neighbors[UP] = upNode
            node.neighbors[DOWN] = downNode
            self.addNodeToStack(leftNode, nodeList)
            self.addNodeToStack(rightNode, nodeList)
            self.addNodeToStack(upNode, nodeList)
            self.addNodeToStack(downNode, nodeList)

    #This method finds the first node in the grid, all grids point will be a +
    def findFirstNode(self, grid):
        rows = len(grid)
        cols = len(grid[0])
        nodeFound = False
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] in self.nodeSymbols:
                    node = Node(row, col)
                    if grid[row][col] == "B":
                        node.blinkyStartNode = True
                    if grid[row][col] in self.portalSymbols:
                        node.portalVal = grid[row][col]
                    return node
        return None

    #This function will look for a specific node at x & y, and returns the node object if it exists
    def getNode(self, x, y, nodeList=[]):
        for node in nodeList:
            if node.position.x == x and node.position.y == y:
                return node
        return None

    #This method looks for specific nodes in node list.
    #this is needed to avoid having duplicate nodes when the player will revisit nodes
    def getNodeFromNode(self, node, nodelist):
        if node is not None:
            for inode in nodelist:
                if node.row == inode.row and node.column == inode.column:
                    return inode
        return node

    #Returns the Node object or none that is connected to the path that is connected to current node
    def getPathNode(self, direction, row, col, nodeList, grid):
        tempNode = self.followPath(direction, row, col, grid)
        return self.getNodeFromNode(tempNode, nodeList)

    #Simply adds node objects to the node list if it dopesnt already exist in there
    def addNode(self, node, nodeList):
        nodeInList = self.nodeInList(node, nodeList)
        if not nodeInList:
            nodeList.append(node)

    #Adds a node to the stack if it hasnt already been added to nodeList
    def addNodeToStack(self, node, nodeList):
        if node is not None and not self.nodeInList(node, nodeList):
            self.nodeStack.push(node)

    #Returns a true of false if a node is in a list, rather than return an object
    def nodeInList(self, node, nodeList):
        for inode in nodeList:
            if node.position.x == inode.position.x and node.position.y == inode.position.y:
                return True
        return False

    #This method follows the paths laid out in the textfile by checking for the specified symbols
    def followPath(self, direction, row, col, grid):
        rows = len(grid)
        columns = len(grid[0])
        if direction == LEFT and col >= 0:
            return self.pathToFollow(LEFT, row, col, "-", grid)
        elif direction == RIGHT and col < columns:
            return self.pathToFollow(RIGHT, row, col, "-", grid)
        elif direction == UP and row >= 0:
            return self.pathToFollow(UP, row, col, "|", grid)
        elif direction == DOWN and row < rows:
            return self.pathToFollow(DOWN, row, col, "|", grid)
        else:
            return None
    #this function on the other hand, follows the path like above, only now it returns the grid point if a node is found
    def pathToFollow(self, direction, row, col, path, grid):
        tempSymbols = [path]+self.nodeSymbols
        if grid[row][col] in tempSymbols:
            while grid[row][col] not in self.nodeSymbols:
                if direction is LEFT:
                    col -= 1
                elif direction is RIGHT:
                    col += 1
                elif direction is UP:
                    row -= 1
                elif direction is DOWN:
                    row += 1
            node = Node(row, col)
            #assigning each of the nodes in the groupNode a specific job
            if grid[row][col] == "H":
                node.homeGuide = True
            if grid[row][col] == "S":
                node.pinkyStartNode = True
            if grid[row][col] == "P":
                node.pacmanStartNode = True
            if grid[row][col] == "I":
                node.inkyStartNode = True
            if grid[row][col] == "C":
                node.clydeStartNode = True
            if grid[row][col] == "F":
                node.fruitStartNode = True
            if grid[row][col] in self.portalSymbols:
                node.portalVal = grid[row][col]
            return node
        else:
            return None

    #This function loops through the list of nodes, finds the two portals, and links them togther
    def setupPortalNodes(self):
        portalDict = {}
        for i in range(len(self.nodeList)):
            if self.nodeList[i].portalVal != 0:
                if self.nodeList[i].portalVal not in portalDict.keys():
                    portalDict[self.nodeList[i].portalVal] = [i]
                else:
                    portalDict[self.nodeList[i].portalVal] += [i]
        for key in portalDict.keys():
            node1, node2 = portalDict[key]
            self.nodeList[node1].portalNode = self.nodeList[node2]
            self.nodeList[node2].portalNode = self.nodeList[node1]

    #this function defines the nodes used to house the ghost when spawned
    def getHomeArray(self):
        return [['0', '0', 'B', '0', '0'],
                ['0', '0', '|', '0', '0'],
                ['+', '0', '|', '0', '+'],
                ['I', '-', 'S', '-', 'C'],
                ['+', '0', '0', '0', '+']]

    #This function move the home nodes to near the home guide node, then adds the nodes to node list
    def moveHomeNodes(self):
        for node in self.nodeList:
            if node.homeGuide:
                nodeA = node
                break
        nodeB = nodeA.neighbors[LEFT]
        mid = (nodeA.position + nodeB.position) / 2.0
        mid = Vector2(int(mid.x), int(mid.y))
        vec = Vector2(self.homeList[0].position.x, self.homeList[0].position.y)

        for node in self.homeList:
            node.position -= vec
            node.position += mid
            self.addNode(node, self.nodeList)

        A = self.getNodeFromNode(nodeA, self.nodeList)
        B = self.getNodeFromNode(nodeB, self.nodeList)
        H = self.getNodeFromNode(self.homeList[0], self.nodeList)
        A.neighbors[LEFT] = H
        B.neighbors[RIGHT] = H
        H.neighbors[RIGHT] = A
        H.neighbors[LEFT] = B

    #renders the nodes to the screen
    def render(self, screen):
        for node in self.nodeList:
            node.render(screen)
        for node in self.homeList:
            node.render(screen)
