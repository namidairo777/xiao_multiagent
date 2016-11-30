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


class RandomPursuer( PursuerAgent ):
    "A pursuer that chooses a legal action uniformly at random."
    def getDistribution( self, state ):
        dist = util.Counter()
        for a in state.getLegalActions( self.index ): dist[a] = 1.0
        dist.normalize()
        return dist

class AstarPursuer(Agent):
    def getAction(self, state):
        return 0

class MTSPursuer(Agent):
    def getAction(self, state):
        return 0

class CRAPursuer(Agent):
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