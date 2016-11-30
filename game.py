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
    
    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = direction

    def getPosition(self):
        return (self.pos)

    def getDirection(self):
        return self.direction

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
        return "(x,y)="+str(self.pos)+", "+str(self.direction)

    def generateSuccssor(self, vector):
        """
        Generate a new Configuration reached by translating the current configuration by the action vector. 
        This is a low-level call and does not attempt to respect the legality of the movement
        Actions are movement vectors.
        """

        x, y = self.pos
        dx, dy = vector
        direction == Actions.vectorToDirection(vector)
        if direction == Directions.STOP:
            direction = self.direction
        return Configuration((x + dx, y + dy), direction)

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

    def getDirection(self):
        return self.configuration.getDirection()
        
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
        # print len(self.data)
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

    def getPossibleActions(config, obstacles):
        possible = []
        x, y = config.pos
        x_int, y_int = int(x + 0.5), int(y + 0.5)

        # In between grid points, all agents must continue straight
        if (abs(x - x_int) + abs(y - y_int)  > Actions.TOLERANCE):
            return [config.getDirection()]

        for dir, vec in Actions._directionsAsList:
            dx, dy = vec
            next_y = y_int + dy
            next_x = x_int + dx
            if not obstacles[next_x][next_y]: possible.append(dir)

        return possible

    getPossibleActions = staticmethod(getPossibleActions)


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
            self.agentStates.append(AgentState(Configuration(pos, Directions.STOP), isTarget))

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
        self.muteAgents = muteAgents
        self.catchExceptions = catchExceptions

    def getProgress(self):
        if self.gameOver:
            return 1.0
        else:
            return self.rules.getProgress(self)

    # def _agentCrashed

    OLD_STDOUT = None
    OLD_STDERR = None

    def mute(self, agentIndex):
        if not self.muteAgents: return 
        global OLD_STDOUT, OLD_STDERR
        import cStringIO
        OLD_STDOUT = sys.stdout
        OLD_STDERR = sys.stderr
        sys.stdout = self.agentOutput[agentIndex]
        sys.stderr = self.agentOutput[agentIndex]

    def unmute(self):
        if not self.muteAgents: return 
        global OLD_STDOUT, OLD_STDERR
        # Revert stdout/stderr to originals
        sys.stdout = OLD_STDOUT
        sys.stderr = OLD_STDERR

    def run(self):
        """
        Main control loop for game play
        """
        self.display.initialize(self.state.data)
        self.numMoves = 0
        import time 

        for i in range(len(self.agents)):
            agent = self.agents[i]
            """
            if not agent:
                # if agent is null, meaning it failed to load
                self.mute(i)
                print >>sys.stderr, "Agent %d failed to load" % i
                self.unmute()
                # self._agentCrash(i, quiet = True)
                return
            if ("registerInitialState" in dir(agent)):
                self.mute(i)
                if self.catchExceptions:
                    try:
                        timed_func = TimeoutFunction(agent.registerInitialState, int(self.rules.getMaxStartupTime(i)))
                        try:
                            start_time = time.time()
                            timed_func(self.state.deepCopy())
                            time_taken = time.time() - start_time
                            self.totalAgentTimes[i] += time_taken
                        except TimeoutFunctionException:
                            print >>sys.stderr, "Agent %d ran out of time on startup!" % i
                            self.unmute()
                            self.agentTimeout = True
                            self._agentCrash(i, quiet = True)
                            return
                    except Exception, data:
                        self._agentCrash(i, quiet = False)
                        self.unmute()
                        return
                else:
                    agent.registerInitialState(self.state.deepCopy())
                self.unmute()
            """
        agentIndex = self.startingIndex
        numAgents = len(self.agents)

        timeCount = 0
        #while not self.gameOver:
        while timeCount < 50000:
            # Fetch the next agent
            agent = self.agents[agentIndex]
            move_time = 0
            skip_action = False
            # Generate an observation of the state
            if "observatioinFunction" in dir(agent):
                self.mute(agentIndex)
                if self.catchExceptions:
                    try:
                        # timed_func = TimeoutFunction(agent.)
                        try:
                            start_time = time.time()
                        except Exception, data:
                        	return
                    except Exception, data:
                       	return
            observation = self.state.deepCopy()
            # Solicit an action
            action = None
            self.mute(agentIndex)

            action = agent.getAction(observation)
            self.unmute()

            # Execute the action
            self.moveHistory.append((agentIndex, action))
            self.state = self.state.generateSuccessor(agentIndex, action)
        
            # Change the display
            print "Before update display"

            self.display.update(self.state.data)
            # Allow for game specific conditions ( winning, losing)
            #print "After display"
            self.rules.process(self.state, self)

            print "After update Display"
            # Track progress
            if agentIndex == numAgents + 1: self.numMoves += 1

            # Next agent
            agentIndex = (agentIndex + 1) % numAgents

            timeCount += 1
            if timeCount % 1000 == 0: print timeCount


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
        






