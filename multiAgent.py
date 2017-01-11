# multiAgent research main 
# 2016/11/16

"""
multiAgent.py holds the logic for this simulation of my resaearch

"""
from game import GameStateData
from game import Game
from game import Directions
from game import Actions
from util import nearestPoint
from util import manhattanDistance
import util, layout
from layout import Layout
import sys, types, time, random, os

#########################
# Interface to this world
#####################

class GameState:
    """
    A state specifies the full game state
    
    States can be uesed by Puresure/Target to capture the actual state of this game

    """    

    #######################
    # Accessor method: use these to access state data
    ###########################

    explored = set()
    def getAndResetExplored():
        tmp = GameState.explored.copy()
        GameState.explored = set()
        return tmp
    getAndResetExplored = staticmethod(getAndResetExplored)

    def getLegalActions(self, agentIndex = 0):
        """
        Returns the legal actions for the pursuer specified
        """
        if self.isWin() or self.isLose(): return []
        if agentIndex == 0:
            return TargetRules.getLegalActions(self)
        else:
            return PursuerRules.getLegalActions(self, agentIndex)


    def generateSuccessor(self, action, agentIndex):
        """
        Returns the successor state after the specified pursuer takes action
        """
        # Check that successors exist
        if self.isWin() or self.isLose(): 
            # time.sleep(2)
            raise Exception('Game over')

        # Copy current state
        state = GameState(self)

        # Let agent's logic deal with its action's effects on the board
        if agentIndex == 0:  # Pacman is moving
            # state.data._eaten = [False for i in range(state.getNumAgents())]
            TargetRules.applyAction( state, action )
        else:                # A ghost is moving
            PursuerRules.applyAction( state, action, agentIndex )


        # Book keeping
        #state.data._agentMoved = agentIndex
        state.data.score += state.data.scoreChange
        GameState.explored.add(self)
        GameState.explored.add(state)
        return state


    def getLegalTargetActions(self, agentIndex = 0):
        return self.getLegalActions(agentIndex)

    def generateTargetSuccessor(self, action):
        """
        Generates the successor state after specified target move
        """
        return self.generateSuccessor(0, action)

    def getTargetState(self):

        return self.data.agentStates[0].copy()

    def geTargetPosition(self):
        return self.data.agentStates[0].getPosition()

    def getPursuerStates(self):
        return self.data.agentStates[1:]

    def getPursuerState(self, agentIndex): 
        if agentIndex == 0:
            raise Exception("Pacman index passed to get pursuer state")
        return self.data.agentStates[agentIndex]


    def getPursuerPosition(self, agentIndex):
        if agentIndex == 0:
            raise Exception("Pacman index passed to get pursuer position")
        return self.data.agentStates[agentIndex].getPosition()

    def getPursuerPositions(self):
        return [s.getPosition() for s in self.getPursuerStates()]

    def getNumAgents(self):
        return len(self.data.agentStates)

    def getScore(self):
        """
        by time? plus agent num
        """
    def getWalls(self):
        """
        walls = state.getWalls()
        if walls[x][y] == True: ....
        """

    def hasWall(self, x, y):
        return self.data.layout.walls[x][y]

    def isLose(self):
        return self.data._lose

    def isWin(self):
        return self.data._win

    ###################
    # Helper methods
    ####################
    def __init__(self, prevState = None):
        """
        Generates a new state by copying information from its predecessor
        """
        if prevState != None:
            self.data = GameStateData(prevState.data)
        else:
            self.data = GameStateData()

    def __hash__(self):
        return hash(self.data)

    def deepCopy(self):
        state = GameState(self)
        state.data = self.data.deepCopy()
        return state

    def initialize(self, layout, numPursuers):
        """
        Creates an initial game state from a layout array
        """
        self.data.initialize(layout, numPursuers)




    #    reference to pacman project

#########################
# Hidden secret of this world
#########################
# May not be uesful
COLLISION_TOLERANCE = 1.0

class ClassicGameRules:
    """
    These game rules manage the control flow of a game, deciding when and how the game starts and ends
    """
    def __init__(self, timeout = 30):
        self.timeout = timeout

    def newGame(self, layout, targetAgent, pursuerAgents, display, catchExceptions = False):
        
        agents = [targetAgent] + pursuerAgents[:layout.getNumPursuers()]
        
        initState = GameState()
        initState.initialize(layout, len(pursuerAgents))
        game = Game(agents, display, self, catchExceptions = catchExceptions)
        game.state = initState
        self.initialState = initState.deepCopy()
        return game
    def process(self, state, game):
        """
        Checks to see whether it is time to end the game
        """

        if state.isWin(): self.win(state, game)
        if state.isLose(): self.lose(state, game)

    def win(self, state, game):
        game.gameOver = True

    def lose(self, state, game):
        game.gameOver = True

    def getProgress(self, game):
        # returns how much used in percentage,
        return "nihao"

    # def agentCrash
    def getMaxTotalTime(self, agentIndex):
        return self.timeout

    def getMaxStartupTime(self, agentIndex):
        #return self,@,
        return self.timeout
    def getMoveWarningTime(self, agentIndex):
        return self.timeout

    def getMovetimeout(self, agentIndex):
        return self.timeout
    
    def getMaxtimeWarnings(self, agentIndex):
        return 0

    def collide(self, state, agentIndex):
        if state.data.agentStates[0].getPosition() == state.data.agentStates[agentIndex].getPosition():
            state.data._win = True
            return True
        else:
            return False

class TargetRules:
    """
    Theese functions govern how pacman interacts with his environment under the classic game rules
    """
    TARGET_SPEED = 1

    def getLegalActions( state):
        """
        returns a list of possible actions
        """
        return Actions.getPossibleActions(state.getTargetState().getPosition(), TargetRules.TARGET_SPEED, state.data.layout.obstacles)

    getLegalActions = staticmethod(getLegalActions)

    def applyAction(state, action):
        """
        Edits the actions to reflect the results of the actions.
        """
        legal = TargetRules.getLegalActions(state)
        if action not in legal:
            raise Exception("Illegal action" + str(action))
        targetState = state.data.agentStates[0]

        # Update configuration
        # vector = Actions.directionToVector(action, TargetRules.TARGET_SPEED)
        targetState.configuration = targetState.configuration.generateSuccessor(action)
        #
    applyAction = staticmethod(applyAction)


    # consume function in pacman


class PursuerRules:
    """
    These functions dictate how ghosts interact with their environment.
    """
    PURSUER_SPEED = 1.0

    def getLegalActions(state, pursuerIndex):
        """
        Ghost in pacman can not turn around unless they reach dead end 
        But in our research, pursuer acts just like agent and human
        """
        return Actions.getPossibleActions(state.data.agentStates[pursuerIndex].getPosition(), PursuerRules.PURSUER_SPEED, state.data.layout.obstacles)
    
    getLegalActions = staticmethod(getLegalActions)

    def applyAction(state, action, pursuerIndex):
        #legal = PursuerRules.getLegalActions(state, pursuerIndex)
        
        #if action not in legal:
        #    raise Exception("Illegal pursuer action" + str(action))

        pursuerState = state.data.agentStates[pursuerIndex]
        # speed = PursuerRules.PURSUER_SPEED
        #vector = Actions.directionToVector(action, speed)
        pursuerState.configuration = pursuerState.configuration.generateSuccessor(action)
        

    applyAction = staticmethod(applyAction)

    

        



################################
# Framework to start this world
##############################

def readCommand(param):
    """

    """
    
    args = dict()
    if len(param) > 3:
        args["numAgents"] = int(param[2])
        print "numAgents: ", args["numAgents"]
    args["layout"] = layout.getLayout(param[0] + ".lay", args["numAgents"])
    import targetAgents as targets
    import pursuerAgents as pursuers
    import graphicsDisplay as graphics
    args["target"] = targets.SimpleFleeTarget()
    # creat several pursuers
    # print "agent num", args["layout"].getNumPursuers()
    # print args["layout"].getNumPursuers()
    if param[1] == "astar":
        args["pursuers"] = [pursuers.AstarPursuer() for i in range(1, args["layout"].getNumPursuers() + 1)]
    elif param[1] == "cra":
        args["pursuers"] = [pursuers.CRAPursuer() for i in range(1, args["layout"].getNumPursuers() + 1)]
    elif param[1] == "speedupcra":
        args["pursuers"] = [pursuers.SpeedUpCRAPursuer() for i in range(1, args["layout"].getNumPursuers() + 1)]

    args["display"] = graphics.MultiAgentGraphics()
    if len(param) > 3:
        args["numGames"] = int(param[3])
    
    return args

def loadAgent():
    # auto-agent or keyboard-agent
    pythonPathStr = os.path.expandvars("$PYTHONPATH")



# def replay():

def runGames():
    
    rules = ClassicGameRules()
    games = []
    args = readCommand(sys.argv[1:])
    for i in range(args["numGames"]):
        args = readCommand(sys.argv[1:])
        # print args["layout"].getNumPursuers() 
        game = rules.newGame(args["layout"], args["target"], args["pursuers"], args["display"])
        game.run()


    return games

if __name__ == '__name__':

    #args = readCommand(sys.argv[1:])
    #run(**args)

    runGames(readCommand())

    pass
    
# args = readCommand(sys.argv[1:])

runGames()
