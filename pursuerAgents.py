# Multi-Pursuer Agent algorithm 
# 2016/11/16

#################
# We have some algorithm for single-Agent and multiAgent
# Single: 
# 1. a star
# 2. moving target search
# multiple:
# 1. CRA
# 2. Multiple Agent moving target search MA-MTS
##########
from game import Agent
from game import Actions
from game import Directions
import random
from util import manhattanDistance
import util

class PursuerAgent( Agent ):
    def __init__( self, index ):
        self.index = index

    def getAction( self, state ):
        dist = self.getDistribution(state)
        if len(dist) == 0:
            return Directions.STOP
        else:
            return util.chooseFromDistribution( dist )

    def getDistribution(self, state):
        "Returns a Counter encoding a distribution over actions from the provided state."
        util.raiseNotDefined()



class RandomPursuer(Agent):
    "An agent that turns left at every opportunity"

    def getAction(self, state, agentIndex):
        legal = state.getLegalTargetActions(agentIndex)
        import random
        return legal[random.randint(0, len(legal) - 1)]


class AstarPursuer(Agent):
    """
    A* algorithm, using manhattanDistance as heuristic function
    g: total cost from start to current
    h: heuristic cost from current to goal
    f: g + h
    openList: is going to be calculated
    closeList: already been calculated
    """
    def getAction(self, state, agentIndex):

        return self.aStar(state.data.layout.obstacles, state.data.agentStates[agentIndex].getPosition(), state.data.agentStates[0].getPosition())

    def aStar(self, obstacles, startPos, goalPos):
        # dist{"position": (1, 2), "g": 1, "h": 2, "f": 3}
        openList = []
        closedList = []

        openList.append(Position(startPos, 0, 0, 0))

        while len(openList) > 0:
            lowId = 0

            # find the lowest value of f(x) in openList
            for i in range(len(openList)):
                if openList[i].f < openList[lowId].f:
                    lowId = i
            currentPoint = openList[lowId]

            # go to goal
            if currentPoint.position == goalPos:
                temp = currentPoint
                result = []
                while temp.parent != None:
                    result.append(temp)
                    temp = temp.parent
                return result[len(result) - 1].position

            for i in range(len(openList)):
                if openList[i].position == currentPoint.position:
                    openList = openList[:i] + openList[i + 1:]
                    break
            closedList.append(currentPoint)
            neighbors = Actions.getPossibleActions(currentPoint.position, 1.0, obstacles)

            for i in range(len(neighbors)):
                neighbor = Position(neighbors[i], 0, 0, 0)
                if self.find_point(closedList, neighbor):
                    continue
                gScore = currentPoint.g + 1
                gScoreIsBest = False

                if not self.find_point(openList, neighbor):
                    gScoreIsBest = True
                    neighbor.h = manhattanDistance(neighbor.position, goalPos)
                    openList.append(neighbor)
                if gScore < neighbor.g:
                    gScoreIsBest = True
                if gScoreIsBest:
                    neighbor.parent = currentPoint
                    neighbor.g = gScore
                    neighbor.f = neighbor.g + neighbor.h



    def find_point(self, dataList, point):
        for i in range(len(dataList)):
            if dataList[i].position == point.position:
                return True
        return False



class Position:
    def __init__(self, position, g, h, f, parent = None):
        self.position = position
        self.g = g
        self.h = h
        self.f = h
        self.parent = parent

class MTSPursuer(Agent):
    def getAction(self, state):
        return 0

class CRAPursuer(Agent):
    """
    CRA:
    Smax 
    Spra*
    Cmax
    Cpra*    
    """
    def getAction(self, state):

        return 0
    def calculateCover():
        return 0

    def stateAbstraction():
        return 0

    def CRP():
        """

        """
        return 0


class MinimaxPursuer(Agent):
    def getAction(self, state):
        return 0


class MAMTSPursuer(Agent):
    def getAction(self, state):
        return 0

class AlphaBetaPursuer(Agent):
    def getAction(self, state):
        return 0

class ExpectimaxPursuer(Agent):
    def getAction(self, state):
        return 0


def scoreEvaluationFunction(state):
	return 0