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
from mapRefinement import Refinement

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
        
        return self.aStar(state.data.layout.obstacles, state.data.agentStates[agentIndex].getPosition(), state.data.agentStates[0].getPosition(), False, None)

    def getAbstractionAction(self, abstractions, start, goal):
        return Refinement.refine(abstractions, start, goal)



    def aStar(self, obstacles, startPos, goalPos, abstracted=False, abstractionMap=None):
        # dist{"position": (1, 2), "g": 1, "h": 2, "f": 3}
        if startPos == goalPos:
            return startPos
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
                return result[-1].position

            for i in range(len(openList)):
                if openList[i].position == currentPoint.position:
                    openList = openList[:i] + openList[i + 1:]
                    break
            closedList.append(currentPoint)
            if abstracted:
                # print "current position", currentPoint.position
                neighbors = Actions.getPossibleAbstractedNeighbors(currentPoint.position, abstractionMap)
                
            else:
                
                neighbors = Actions.getPossibleNeighborActions(currentPoint.position, 1.0, obstacles)
                # print "neighbors", neighbors

            for i in range(len(neighbors)):
                neighbor =  Position(neighbors[i], 0, 0, 0)
                if self.find_point(closedList, neighbor):
                    continue

                gScore = currentPoint.g + 1
                if abstracted:
                    # print "current and neighbor:", currentPoint.position, neighbor.position
                    gScore = currentPoint.g + manhattanDistance(currentPoint.position, neighbor.position) 

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


# A star class
class Position:
    def __init__(self, position, g, h, f, parent = None):
        self.position = position
        self.g = g
        self.h = h
        self.f = h
        self.parent = parent

class CRAPursuer(Agent):
    """
    CRA:
    Smax 
    Spra*
    Cmax
    Cpra*    
    """


    def getAction(self, state, agentIndex):
        return self.calculateSuccessorSet(agentIndex, state, state.data.layout)

    
    def calculateCover(self, agentIndex, state, layout):
        # targetSet = 0
        pursuerSet = 0
        priorityQueue = []
        time = 0

        # Initial layout from obstacle map
        locations = layout.deepCopy()
        
        # Push initial target into queue
        priorityQueue.append({"position": state.data.agentStates[0].getPosition(), "type": "target", "time": time})
        x, y = state.data.agentStates[0].getPosition()
        locations.obstacles[x][y] = "target-set"
        
        # Push initial pursuers into queue
        for i in range(1, layout.getNumPursuers() + 1):
            priorityQueue.append({"position": state.data.agentStates[i].getPosition(), "type": "pursuer", "time": time})
            x, y = state.data.agentStates[i].getPosition()
            locations.obstacles[x][y] = "pursuer-set"
            pursuerSet += 1 # add 1 to pursuer set count
        #print priorityQueue

        # Loop until queue is null
        while len(priorityQueue) != 0:
            #print priorityQueue[0]
            try:
                while len(priorityQueue) != 0 and priorityQueue[0]["time"] == time:
                    temp = priorityQueue.pop(0)
                    (agent_x, agent_y) = temp["position"]
                    typeName = temp["type"]

                    neighbors = Actions.getPossibleNeighborActions((agent_x, agent_y), 1.0, layout.obstacles)
                    #print neighbors
                    for neighbor in neighbors:
                        x, y = neighbor
                        if locations.obstacles[x][y] not in ["target-set", "pursuer-set"]:
                            # push to queue
                            priorityQueue.append({"position": neighbor, "type": typeName, "time": time + 1}) 
                            if typeName == "target":
                                locations.obstacles[x][y] = "target-set"
                            else:
                                locations.obstacles[x][y] = "pursuer-set"
                                pursuerSet += 1 # set added by 1
                time += 1
            except IndexError:
                #print priorityQueue
                print "length of queue", len(priorityQueue), "list over"
        return pursuerSet

    def calculateSuccessorSet(self, agentIndex, state, layout):

        """
        ratio = 0.3
        import random
        if random.random() < ratio:
            return AstarPursuer().getAction(state, agentIndex)
        """
        # max value for pursuer-set
        maxValue = 0
        values = []
        successors = Actions.getPossibleActions(state.data.agentStates[agentIndex].getPosition(), 1.0, layout.obstacles)
        
        # Frome 4 possible successors, choose one with best value 
        for successor in successors:
            tempGameState = state.deepCopy()
            tempGameState.data.agentStates[agentIndex].setPosition(successor)
            import time
            startTime = time.time()
            res = self.calculateCover(agentIndex, tempGameState, layout)

            endTime = time.time()
            writeStepTimeLog('cra.csv', endTime - startTime)
            values.append(res)
        return successors[values.index(max(values))]

class SpeedUpCRAPursuer(Agent):
    """
    CRA:
    Smax 
    Spra*
    Cmax
    Cpra*    
    """


    def getAction(self, state, agentIndex):
        return self.calculateSuccessorSet(agentIndex, state, state.data.layout)

    
    def calculateCover(self, agentIndex, state, layout):
        targetSet = 0
        targetQueue = []
        pursuerQueue = []
        time = 0
        locations = layout.deepCopy()
        #print type(agentIndex) #state.data.agentStates[agentIndex].getPosition()
        targetQueue.append({"position": state.data.agentStates[0].getPosition(), "time": time})
        x, y = state.data.agentStates[0].getPosition()
        locations.obstacles[x][y] = "target-set"
        targetSet += 1
        #print targetQueue
        for i in range(1, layout.getNumPursuers() + 1):
            pursuerQueue.append({"position": state.data.agentStates[i].getPosition(), "time": time})
            x, y = state.data.agentStates[i].getPosition()
            locations.obstacles[x][y] = "pursuer-set"
        #print targetQueue
        while len(targetQueue) != 0 :

            #print "len of target:", len(targetQueue), "len of pursuer", len(pursuerQueue)
            # current target
            #print len(targetQueue)
            while len(targetQueue) > 0 and targetQueue[0]["time"] == time:
                temp = targetQueue.pop(0)
                (target_x, target_y) = temp["position"]
                tempTime = temp["time"]
                #print "time", tempTime 
                #print targetQueue

                neighbors = Actions.getPossibleNeighborActions((target_x, target_y), 1.0, layout.obstacles)
                #print neighbors
                for neighbor in neighbors:
                    x, y = neighbor
                    if locations.obstacles[x][y] not in ["target-set", "pursuer-set"]:
                        targetQueue.append({"position": neighbor, "time": time + 1}) 
                        locations.obstacles[x][y] = "target-set"
                        targetSet += 1


            # current pursuer
            #print "targetset", targetSet
            #print len(pursuerQueue)
            while len(pursuerQueue) > 0 and pursuerQueue[0]["time"] == time:
                (pursuer_x, pursuer_y) = pursuerQueue.pop(0)["position"]

                neighbors = Actions.getPossibleNeighborActions((pursuer_x, pursuer_y), 1.0, layout.obstacles)
                for neighbor in neighbors:
                    x, y = neighbor
                    if locations.obstacles[x][y] not in ["target-set", "pursuer-set"]:
                        pursuerQueue.append({"position": neighbor, "time": time + 1}) 
                        locations.obstacles[x][y] = "pursuer-set"
            time += 1
            #print targetQueue
        #print "overCalculate targetset"
        return targetSet

    def calculateSuccessorSet(self, agentIndex, state, layout):
        minValue = 0
        values = []
        successors = Actions.getPossibleActions(state.data.agentStates[agentIndex].getPosition(), 1.0, layout.obstacles)
        # print "successors", successors
        # print len(successors)

        for successor in successors:
            tempGameState = state.deepCopy()
            tempGameState.data.agentStates[agentIndex].setPosition(successor)
            # time of calculate
            import time
            startTime = time.time()
            res = self.calculateCover(agentIndex, tempGameState, layout)
            endTime = time.time()
            # writeStepTimeLog('maze1_speedupcra.csv', endTime - startTime)
            values.append(res)
        # print max(values)
        if max(values) == min(values):
            #print "Go astar", state.data.agentStates[2].getPosition()
            return AstarPursuer().getAction(state, agentIndex)
        else:
            #print "surrounding"
            return successors[values.index(min(values))]

class AbstractCoverPursuer(Agent):
    """
    Abstract to a higher level
    """
    def __init__(self, abstractions):
        self.abstractions = abstractions

    def getAction(self, state, agentIndex):
        # if self.useAstar:
        #     return AstarPursuer().getAction(state, agentIndex)
        return self.calculateSuccessorSet(agentIndex, state, state.data.layout)

    def calculateCover(self, agentIndex, state, layout):
        """
        We use node pointer instead of coordinate position
        """
        targetSet = 0
        targetQueue = []
        pursuerQueue = []
        time = 0
        locations = layout.deepCopy()
        # print type(agentIndex) #state.data.agentStates[agentIndex].getPosition()
        

        for i in range(1, layout.getNumPursuers() + 1):
            pursuerNode = None
            if i == agentIndex:
                pursuerNode = self.abstractions[-1].getNodeByPosition(state.data.agentStates[i].getPosition())
            else:
                pursuerNode = self.abstractions[-1].getNode(state.data.agentStates[i].getPosition())
            pursuerQueue.append({"node": pursuerNode, "time": time})
            pursuerNode.markAs = "pursuer-set"

        targetNode = self.abstractions[-1].getNode(state.data.agentStates[0].getPosition())
        if targetNode.markAs not in ["target-set", "pursuer-set"]:
            targetQueue.append({"node": targetNode, "time": time})
            targetNode.markAs = "target-set"
            targetSet += len(targetNode.children)

        while len(targetQueue) != 0 :
            while len(pursuerQueue) > 0 and pursuerQueue[0]["time"] == time:
                tempNode = pursuerQueue.pop(0)["node"]
                for neighbor in tempNode.neighbors:
                    if neighbor.markAs not in ["target-set", "pursuer-set"]:
                        pursuerQueue.append({"node": neighbor, "time": time + 1}) 
                        neighbor.markAs = "pursuer-set"
            while len(targetQueue) > 0 and targetQueue[0]["time"] == time:
                temp = targetQueue.pop(0)
                tempNode = temp["node"]
                #tempTime = temp["time"]
                for neighbor in tempNode.neighbors:
                    if neighbor.markAs not in ["target-set", "pursuer-set"]:
                        targetQueue.append({"node": neighbor, "time": time + 1}) 
                        neighbor.markAs = "target-set"
                        targetSet += 1
                
            
            time += 1
            #print targetQueue
        #print "overCalculate targetset"
        self.abstractions[-1].clearMark()
        return targetSet

    def calculateSuccessorSet(self, agentIndex, state, layout):
        """
        main function
        """
        # print "before all data: ", state.data
        minValue = 0
        values = []
        # print "abstraction calculate successor set"
        # successors = Actions.getPossibleActions(state.data.agentStates[agentIndex].getPosition(), 1.0, layout.obstacles)

        successors = Actions.getPossibleAbstractedNeighborsByChildPosition(state.data.agentStates[agentIndex].getPosition(), self.abstractions[-1])
        # get abstraction possible successors  
        # print "successors", successors
        # print len(successors)

        for successor in successors:
            # For every Abstracted successors
            tempGameState = state.deepCopy()
            tempGameState.data.agentStates[agentIndex].setPosition(successor)
            #print "agent index", agentIndex
            #print "temp game data", tempGameState.data
            # time of calculate
            import time
            startTime = time.time()
            res = self.calculateCover(agentIndex, tempGameState, layout)
            endTime = time.time()
            # writeStepTimeLog('maze1_abstraction.csv', endTime - startTime)
            values.append(res)

        # print successors
        #print successors
        #print values
        #if max(values) == min(values):
        if max(values) == min(values):  
            a = AstarPursuer()
            # return a.getAction(state, agentIndex)
            #print "aster agent: ", agentIndex
            goal = a.getAbstractionAction(self.abstractions, state.data.agentStates[agentIndex].getPosition(), state.data.agentStates[0].getPosition())
            result = a.aStar(state.data.layout.obstacles, state.data.agentStates[agentIndex].getPosition(), goal)
            #print state.data.agentStates[agentIndex].getPosition(), "->", result
            #result = a.aStar(state.data.layout.obstacles, state.data.agentStates[agentIndex].getPosition(), state.data.agentStates[0].getPosition())
            # print "astar after refinement:", result
            #print "A star - agent:", agentIndex
            #print state.data.agentStates[agentIndex].getPosition(), " -> ", result
            return result
        
        else:
            #print "cover agent: ", agentIndex
            # print "min-target-cover-set", successors[values.index(min(values))]
            # print "surrounding"
            a = AstarPursuer()
            #nextAbstractionPosition = successors[values.index(min(values))]
            nextNode = self.abstractions[-1].getNodeByPosition(successors[values.index(min(values))])
            #print nextNode
            nextPosition = nextNode.getRandomChildPosition()
            result = a.aStar(state.data.layout.obstacles, state.data.agentStates[agentIndex].getPosition(), nextPosition)
            #print state.data.agentStates[agentIndex].getPosition(), "->", result
            #print "Cover - agent:", agentIndex
            #print state.data.agentStates[agentIndex].getPosition(), " -> ", result
            return result
            # return result


class MTSPursuer(Agent):
    def getAction(self, state):
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

def writeStepTimeLog(title, log):
    import csv
    with open('logs/' + title, 'a') as csvfile:
        spamwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        spamwriter.writerow([log])
