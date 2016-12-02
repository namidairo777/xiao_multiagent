# Target Agent algorithm 
# 2016/11/16

####################
# We have several algorithms to run away
# 1. Simple flee
# 2. Dynamic Abstract Minimax
# 3. Minimax
# 4. Greedy
#####################

from util import manhattanDistance
from game import Directions
import random, util
from game import Agent
from game import Actions
import game


"""
random move
"""
class LeftTurnTarget(game.Agent):
    "An agent that turns left at every opportunity"

    def getAction(self, state):
        legal = state.getLegalTargetActions()
        import random
        return legal[random.randint(0, len(legal) - 1)]


class RandomTarget(Agent):
    "Return random legal neightbor point"

    def getAction(self, state, agentIndex):
        legal = state.getLegalTargetActions()
        import random
        return legal[random.randint(0, len(legal) - 1)]


class SimpleFleeTarget(Agent):

    def getAction(self, state, agentIndex):
        neighbors = Actions.getPossibleActions(state.data.agentStates[0].getPosition(), 1.0, state.data.layout.obstacles)
        #print "neighbors", neighbors
        maxDistance = 0
        maxNeighbor = state.data.agentStates[0].getPosition()
        for i in range(len(neighbors)):
            distance = 0
            for j in range(1, len(state.data.agentStates)):
                distance += manhattanDistance(neighbors[i], state.data.agentStates[j].getPosition())
            #print "neighbor", i, "distance", distance
            if distance > maxDistance:
                maxNeighbor = neighbors[i]
                maxDistance = distance
        #print "simple flee position", maxNeighbor
        return maxNeighbor



class DAMTarget(Agent):
    def getAction(self, state):
        return 0

class MinimaxTarget(Agent):
    def getAction(self, state):
        return 0

class GreedyTarget(Agent):

    def getAction(self, state):
        return 0
def scoreEvaluation(state):
    return state.getScore()



