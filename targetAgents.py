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
import game

class LeftTurnTarget(game.Agent):
    "An agent that turns left at every opportunity"

    def getAction(self, state):
        legal = state.getLegalTargetActions()
        print legal
        current = state.getTargetState().configuration.direction
        print current
        if current == Directions.STOP: current = Directions.NORTH
        left = Directions.LEFT[current]
        if left in legal: return left
        if current in legal: return current
        if Directions.RIGHT[current] in legal: return Directions.RIGHT[current]
        if Directions.LEFT[left] in legal: return Directions.LEFT[left]
        return Directions.STOP

class RandomTarget(Agent):

    def getAction(self, state):
        return 0

class SimpleFleeTarget(Agent):

    def getAction(self, state):
        return 0

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



