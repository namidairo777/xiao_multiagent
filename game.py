#2016-07-29
#Developed by XIAO TANG
#tangxiao.dalian@gmail.com

#game.py
#

from util import *
import time, os
import traceback
import sys

######################
#                    #
######################

class Agent:
    """
    An agent must define a getAction method

    """
    def __init__(self, index=0):
        self.index = index

    def getAction(self, state):
        return 0
        raiseNotDefined()

class Directions:
    """
    Left and right corresponds to four Directions (north, south, east, west)
    """
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'
    STOP = 'Stop'

    LEFT = {NORTH: WEST,
            SOUTH: EAST,
            EAST: NORTH,
            WEST: SOUTH,
            STOP: STOP}

    RIGHT = dict([(y,x) for x, y in LEFT.items()])

    REVERSE = {NORTH: SOUTH,
                SOUTH: WEST,
                EAST: WEST,
                WEST: EAST,
                STOP: STOP}

class Configuration:
    """
    A Configuration holds the (x,y) coordinate of a character, along with its traveling direction.
    position
    direction

    """
    
    def __init__(self, pos):
        self.pos = pos
        # self.direction = direction

    def getPosition(self):
        return (self.pos)

    def setPosition(self, pos):
        self.pos = pos

    #def getDirection(self):
     #   return self.direction

    def isInteger(self):
        x, y = self.pos
        return x == int(x) and y == int(y)

    def __eq__(self, other):
        if other == None: return False
        return (self.pos == other.pos and self.direction == other.direction)

    def __hash__(self):
        x = hash(self.pos)
        y = hash(self.direction)
        return hash(x + 13 * y)

    def __str__(self):
        return "(x,y)="+str(self.pos)

    def generateSuccessor(self, pos):
        """
        Generate a new Configuration reached by translating the current configuration by the action vector. 
        This is a low-level call and does not attempt to respect the legality of the movement
        Actions are movement vectors.
        """

        return Configuration(pos)

class AgentState:
    """
    AgentStates hold the state of an agent (configuration, speed, etc)

    """

    def __init__(self, startConfiguration, isTarget):
        self.start = startConfiguration
        self.configuration = startConfiguration
        self.isTarget = isTarget
        self.numCarrying = 0
        self.numReturned = 0

    def __str__(self):
        if self.isTarget:
            return "Target: "+str( self.configuration)
        else:
            return "Pursuer: "+str(self.configuration)

    def __eq__(self, other):
        if other == None:
            return False
        return self.configuration == other.configuration and self.scaredTimer == other.scaredTimer

    def __hash__(self):
        state = AgentState(self.start, self.isPacman)
        state.configuration = self.configuration
        state.numCarrying = self.numCarrying
        state.numReturned = self.numReturned
        return state

    def copy(self):
        state = AgentState(self.start, self.isTarget)
        state.configuration = self.configuration
        state.numCarrying = self.numCarrying
        state.numReturned = self.numReturned
        return state

    def getPosition(self):
        if self.configuration == None: return None
        return self.configuration.getPosition()

    def setPosition(self, pos):
        self.configuration.setPosition(pos)
    #def getDirection(self):
     #   return self.configuration.getDirection()
        
class Grid:
    """
    A 2-dimensional array of objects backed ny a list of lists.
    Data is accessed via grid[x][y] where (x,y) are positions on a Game map with
    x horizontal, y vertical and the origin (0, 0) in the bottom left corner
    """

    def __init__(self, width, height, initialValue = False):
        if initialValue not in [False, True]: raise Exception("Grid can only contain booleans")
        self.CELLS_PER_INT = 30
        self.width = width
        self.height = height
        self.data = [[initialValue for y in range(height)] for x in range(self.width)]

    def __getitem__(self, i):
        return self.data[i]

    def __setitem__(self, key, item):
        self.data[key] = item 

    # def __str__

    # def __eq__

    # def __hash__

    def copy(self):
        g = Grid(self.width, self.height)
        g.data = [x[:] for x in self.data]
        return g

    # def deepCopy()

    # def shallowCopy()

    def count(self, item = True):
        return sum([x.count(item) for x in self.data])

    # def asList

    # def packBits

class Actions:
    """
    A collection of static methods for manipulating move actions.
    """
    _directions = {Directions.NORTH: (0, 1),
                   Directions.SOUTH: (0, -1),
                   Directions.EAST: (1, 0),
                   Directions.WEST: (-1, 0),
                   Directions.STOP: (0, 0)}

    _directionsAsList = _directions.items()

    TOLERANCE = .001

    def reverseDirection(action):
        if action == Directions.NORTH:
            return Directions.SOUTH
        if action == Directions.SOUTH:
            return Directions.NORTH
        if action == Directions.EAST:
            return Directions.WEST
        if action == Directions.WEST:
            return Directions.EAST
        # stop action
        return action

    reverseDirection = staticmethod(reverseDirection)

    def vectorToDirection(vector):
        dx, dy = vector
        if dy > 0:
            return Directions.NORTH
        if dy < 0:
            return Directions.SOUTH
        if dx > 0: 
            return Directions.EAST
        if dx < 0:
            return Directions.WEST
        return Directions.STOP

    vectorToDirection = staticmethod(vectorToDirection)

    def directionToVector(direction, speed = 1.0):
        dx, dy = Actions._directions[direction]
        return (dx * speed, dy * speed)

    directionToVector = staticmethod(directionToVector)

    def getPossibleActions(config, speed, obstacles):
        possible = []
        x, y = config
        if not obstacles[int(x + speed)][y]:
            possible.append((int(x + speed), y))
        if not obstacles[int(x - speed)][y]:
            possible.append((int(x - speed), y))
        if not obstacles[x][int(y + speed)]:
            possible.append((x, int(y + speed)))
        if not obstacles[x][int(y - speed)]:
            possible.append((x, int(y - speed)))
        possible.append((x, y))
        return possible

    getPossibleActions = staticmethod(getPossibleActions)


    def getPossibleNeighborActions(config, speed, obstacles):
        possible = []
        x, y = config
        if not obstacles[int(x + speed)][y]:
            possible.append((int(x + speed), y))
        if not obstacles[int(x - speed)][y]:
            possible.append((int(x - speed), y))
        if not obstacles[x][int(y + speed)]:
            possible.append((x, int(y + speed)))
        if not obstacles[x][int(y - speed)]:
            possible.append((x, int(y - speed)))
        return possible

    getPossibleNeighborActions = staticmethod(getPossibleNeighborActions)



    def getLegalNeighbors(position, walls):
        x, y = position
        x_int, y_int = int(x + 0.5), int(y + 0.5)
        neighbors = []
        for dir, vec in Actions._directionsAsList:
            dx, dy = vec
            next_x = x_int + dx
            if next_x < 0 or next_x == walls.width:
                continue
            next_y = y_int + dy
            if next_y < 0 or next_y == walls.height:
                continue
            if not walls[next_x][next_y]:
                neighbors.append((next_x, next_y))
        return neighbors

    getLegalNeighbors = staticmethod(getLegalNeighbors)

    def getSuccessor(position, action):
        dx, dy = Actions.directionToVector(action)
        x, y = position
        return (x + dx, y + dy)

    getSuccessor = staticmethod(getSuccessor)


class GameStateData:
    """
    GameState.data
    """
    def __init__(self, prevState = None):
        """
        Generates a new data packet by copying information from its predecessor
        """
        if prevState != None:
            self.agentStates = self.copyAgentStates(prevState.agentStates)
            self.layout = prevState.layout
            self.score = prevState.score

        self._agentMoved = None
        self._lose = False
        self._win = False
        self.scoreChange = 0

    def deepCopy(self):
        state = GameStateData(self)
        state.layout = self.layout.deepCopy()
        state._agentMoved = self._agentMoved
        return state

    def copyAgentStates(self, agentStates):
        copiedStates = []
        for agentState in agentStates:
            copiedStates.append(agentState.copy())
        return copiedStates

    # def __eq__
    # def __hash__
    # def __str__

    def initialize(self, layout, numPursuerAgents):
        """
        Creates an initial game state from a layout array
        """
        self.layout = layout
        self.score = 0
        self.scoreChange = 0

        self.agentStates = []
        numPursuers = 0
        for isTarget, pos in layout.agentPositions:
            if not isTarget:
                if numPursuers == numPursuerAgents:
                    continue
                else:
                    numPursuers += 1
            self.agentStates.append(AgentState(Configuration(pos), isTarget))
        
                    
class Game:
    """
    The Game manages the control flow, soliciting actions from agents.
    """
    def __init__(self, agents, display, rules, startingIndex = 0, muteAgents = False, catchExceptions = False):
        self.agents = agents
        self.display = display
        self.rules = rules
        self.startingIndex = startingIndex
        self.gameOver = False
        self.moveHistory = []
        self.catchExceptions = catchExceptions
        self.turn = 0

    def getProgress(self):
        if self.gameOver:
            return 1.0
        else:
            return self.rules.getProgress(self)

    # def _agentCrashed

    

    def run(self):
        """
        Main control loop for game play

        flow
        loop agents to make plan
        update the GameState
        display   
        

        """
        self.display.initialize(self.state.data)
        self.numMoves = 0
        import time 
            
        agentIndex = self.startingIndex
        numAgents = len(self.agents)

        # time.sleep(10)
        startTime = time.time()
        
        # Rules are different from pacman project
        # turnCount = 0

        while not self.gameOver:
            # make the plan for moving
            observation = self.state.deepCopy()
            ##agentMovement = []
            turnStartTime = time.time()
            for agentIndex in range(len(self.agents)):
                # time for step move
                stepStartTime = time.time()
                agent = self.agents[agentIndex]
                action = agent.getAction(observation, agentIndex)
                self.moveHistory.append((agentIndex, action))
                
                #update GameState
                self.state = self.state.generateSuccessor(action, agentIndex)
                #stepEndTime = time.time()
                #self.writeStepTimeLog(stepEndTime - stepStartTime)
                self.display.update(self.state.data, agentIndex, self.turn)
                if agentIndex != 0: 
                    if self.rules.collide(self.state, agentIndex):
                        endTime = time.time()
                        cost = endTime - startTime
                        print "time cost: ", cost
                        self.gameOver = True
                        
                        #write game time
                        self.writeLog(self.turn)
                        #write log
                        break
                # 10 for roundMap
                if self.turn > 1000:
                    self.gameOver = True
                    # self.writeLog("NAN")
                    break

            
            self.turn += 1
            
            while (time.time() - turnStartTime) <= 0.1:
                pass
            """
            Real-time constraints 
            """

            #update GameState
            #self.state = self.state.generateSuccessor(action, agentIndex)


            # display for moving 
        
        

        # Inform a learning agent of the game result
        for agentIndex, agent in enumerate(self.agents):
            if "final" in dir(agent):
                try:
                    self.mute(agentIndex)
                    agent.final(self.state)
                    self.unmute()
                except Exception, data:
                    if not self.catchExceptions: raise
                    self._agentCrash(agentIndex)
                    self.unmute()
                    return
        self.display.finish()
    
    def writeLog(self, log):
        import csv
        with open('logs/turn_count_maze1_astar_3pursuer.csv', 'a') as csvfile:
            spamwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            spamwriter.writerow([log])
    def writeStepTimeLog(self, log):
        import csv
        with open('logs/step_time_speedupcra.csv', 'a') as csvfile:
            spamwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            spamwriter.writerow([log])







