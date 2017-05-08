# mapAbstraction.py
# 2017.4.27
# XIAO TANG
# tangxiao.dalian@gmail.com
"""
Map -> Node -> abstract
"""
class Node(object):
    """A node is representative for a position"""
    def __init__(self, level):
        self.position = None               # coordinate 
        self.val = 0
        self.level = level      # abstraction level
        self.isAbstracted = False    # abtracted or not
        self.neighbors = []        # neighbor nodes
        self.children = []        # child nodes (abtraction level - 1)
        self.positions = []
        self.childrenNeighbors = [] # child's neighbors (abtraction level - 1), convinient for connnect graph
        self.markAs = None      # mark as none, target-set, pursuer-set

    def addNeighbors(self, node):
        """
        Append neighbor to current node's neighbors list
        """
        self.neighbor.append(node)

class Abstraction(object):
    """A class for map abstraction"""
    def __init__(self):
        self.width = 0
        self.height = 0
        self.head = None
        self.nodes = None
        self.nodeArray = None

    def mapToGraph(self, obstacles):
        """
        Translate current 2-dimension array to node array
        """
        # obstacles to node array
        self.height = obstacles.height
        self.width = obstacles.width
        graph = []
        i = 1
        first = True
        for x in range(self.width):
            row = []
            for y in range(self.height):
                node = None
                
                if not obstacles[x][y]:
                    # if (x, y) is not obstacle
                    node = Node(1)
                    node.position = (x, y)
                    node.val = i
                    i += 1 
                    if first: 
                    	self.head = node
                    	first = False
                row.append(node)
            graph.append(row)
        self.nodeArray = graph

        
    def addNeighbors(self):
        """
        Assign neighbors to each node
        """
        for x in range(self.width):
            for y in range(self.height):
                if self.nodeArray[x][y]:
                    currentNode = self.nodeArray[x][y]
                    # 4 direction
                    # left
                    if x-1 >= 0:
                        if self.nodeArray[x-1][y]:
                            currentNode.neighbors.append(self.nodeArray[x-1][y])
                    # up
                    if y-1 >= 0:
                        if self.nodeArray[x][y-1]:
                            currentNode.neighbors.append(self.nodeArray[x][y-1])
                    # right
                    if x+1 < self.height:
                        if self.nodeArray[x+1][y]:
                            currentNode.neighbors.append(self.nodeArray[x+1][y])
                    # down
                    if y+1 < self.width:
                        if self.nodeArray[x][y+1]:
                            currentNode.neighbors.append(self.nodeArray[x][y+1])

    def getAbstractArray(self, obstacles):
        """
        graph -> abstraction map
        """
        # map to graph with neighbors
        self.mapToGraph(obstacles)
        self.addNeighbors()
        abstractNodeArray = []
        print self.head
        # Abstract map
        queue = [self.head]
        # First node neighbors
        while len(queue) != 0:
            # node 1
            node1 = queue.pop(0)
            node1.isAbstracted = True # mark
            # Add node1 neighbors to queue
            singleNode = True
            for neighbor in node1.neighbors:
                if neighbor not in queue and not neighbor.isAbstracted:
                    queue.append(neighbor)
                    singleNode = False
            if singleNode:
                abstractNode = Node(node1.level + 1)
                abstractNode.children.append(node1)
                abstractNode.positions.append(node1.position)
                break
            # Easy to pop
            def popNode(node, array):
                for i in range(len(array)):
                    if array[i] is node:
                        array.pop(i)
                        break
                return

            # node 2
            node2 = None
            for node in node1.neighbors:
                if not node.isAbstracted:
                    node2 = node
                    node2.isAbstracted = True # mark
                    popNode(node, queue)            
            # Add node1 neighbors to queue
            for neighbor in node2.neighbors:
                if neighbor not in queue and not neighbor.isAbstracted:
                    queue.append(neighbor)

            abstractNode = Node(node1.level + 1)
            abstractNode.children.append(node1)
            abstractNode.positions.append(node1.position)
            abstractNode.children.append(node2)
            abstractNode.positions.append(node2.position)
            for neighbor in (node1.neighbors + node2.neighbors):
                if neighbor not in [node1, node2]:
                    abstractNode.childrenNeighbors.append(neighbor)
            # Add to list 
            abstractNodeArray.append(abstractNode)
            # set position x and y

        self.nodes = abstractNodeArray


    def getAbstractGraph(self):
        """
        Translate unconnectec graph to connected graph
        O()
        """
        # Assign every other node which has these neighbor node as this node's neighbor 
        for node in self.nodes:
            # for every node, check wether in 
            for child in node.children:
                for neighborNode in self.nodes:
                    if child in neighborNode.childrenNeighbors and neighborNode not in node.neighbors:
                        node.neighbors.append(neighborNode)

    def getAbstractMap(self, obstacles):
        self.getAbstractArray(obstacles)
        self.getAbstractGraph()
        return self.head


    def getNode(self, position):
        for node in self.nodes:
            if position in node.positions:
            	return node
    def clearMark(self):
        for node in self.nodes:
            node.markAs = None

class Test(object):
    
    """Test class"""
    def do(self):
        obstacles = [[False for i in range(10)] for j in range(10)]
        a = Abstraction()
        a.mapToGraph(obstacles)




