# mapAbstraction.py
# 2017.4.27
# XIAO TANG
# tangxiao.dalian@gmail.com
"""
Map -> Node -> abstract
"""
class Node(object):
    """A node is representative for a position"""
    def __init__(self, level, val):
        self.position = None               # coordinate 
        self.val = val
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
    """
    A class for map abstraction
    Function description: 
    1. mapToGraph: obstacle 2-d array -> node array (no neighbor)
    2. addNeighbors: node array (no neighbor) -> node array (with neighbors)
    3. getAbstractArray: node array (with neighbors) -> abstracted node array (no neighbor)
    4. getAbstractGraph: abstracted node array (no neighbor) -> abstracted node array (with neighbors)

    """
    def __init__(self):
        self.width = 0   
        self.height = 0  
        self.head = None      # Graph head pointer
        self.nodes = None     # all nodes array, easy to find the node pointer
        self.nodeArray = None # 2-d node array

    def mapToGraph(self, obstacles):
        """
        Translate current 2-dimension array to node array
        """
        # obstacles to node array
        self.height = obstacles.height
        self.width = obstacles.width
        graph = []
        first = True # Assign first node to self.head attribute
        count = 1
        for y in range(self.height):
            row = []
            for x in range(self.width):
                node = None                
                if not obstacles[x][y]:
                    # if (x, y) is not obstacle
                    node = Node(0, count)
                    node.position = (x, y)
                    if first: 
                    	# Assign first node to self.head attribute
                    	self.head = node
                    	first = False
                    count += 1
                row.append(node)
            graph.append(row)
        self.nodeArray = graph

        
    def addNeighbors(self):
        """
        Assign neighbors to each node
        """
        for y in range(self.width):
            for x in range(self.height):
                if self.nodeArray[x][y]:
                    currentNode = self.nodeArray[x][y]
                    # 4 direction
                    # left
                    if x-1 >= 0:
                        if self.nodeArray[x-1][y]:
                            currentNode.neighbors.append(self.nodeArray[x-1][y])
                    # down
                    if y+1 < self.width:
                        if self.nodeArray[x][y+1]:
                            currentNode.neighbors.append(self.nodeArray[x][y+1])
                    # right
                    if x+1 < self.height:
                        if self.nodeArray[x+1][y]:
                            currentNode.neighbors.append(self.nodeArray[x+1][y])
                    # up
                    if y-1 >= 0:
                        if self.nodeArray[x][y-1]:
                            currentNode.neighbors.append(self.nodeArray[x][y-1])
                    
                    
        """
        for x in self.nodeArray:
        	temp = ""
        	for y in x:
        	    if y is None: 
        	    	temp += " **" 
        	    else: 
        	    	# print y.val, "neighbors: ", [neighbor.val for neighbor in y.neighbors]
        	    	temp += " %2.d" % (y.val)
        	print temp
        """
    def getAbstractArray(self):
        """
        graph -> abstraction map
        """
        print "get abstraction map"
        # map to graph with neighbors
        
        abstractNodeArray = []
        # Abstract map
        queue = [self.head]
        count = 1
        # First node neighbors
        while len(queue) != 0:
            
            # node 1
            node1 = queue.pop(0)
            node1.isAbstracted = True # mark
            # Add node1 neighbors to queue
            singleNode = True
            for neighbor in node1.neighbors:
                if neighbor.isAbstracted is False:
                    if neighbor not in queue:
                    	queue.append(neighbor)
                    singleNode = False

            if singleNode:
                abstractNode = Node(node1.level + 1, count)
                count += 1
                abstractNode.children.append(node1)

                if node1.level > 0:	            	              	
                	abstractNode.positions += node1.positions
                else:
                	abstractNode.positions.append(node1.position)
                for neighbor in node1.neighbors:
                	if neighbor not in [node1]:
                		abstractNode.childrenNeighbors.append(neighbor)
                abstractNodeArray.append(abstractNode)
                continue
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
                    break   
            # print [i.positions for i in queue]
            for neighbor in node2.neighbors:
                if neighbor not in queue and not neighbor.isAbstracted:
                    queue.append(neighbor)

            abstractNode = Node(node1.level + 1, count)
            count += 1
            abstractNode.children.append(node1)
            abstractNode.children.append(node2)
            if node1.level > 0:
                abstractNode.positions += node1.positions
            else:
                abstractNode.positions.append(node1.position)
            if node1.level > 0:
                abstractNode.positions += node2.positions
            else:
               	abstractNode.positions.append(node2.position)

            for neighbor in (node1.neighbors + node2.neighbors):
                if neighbor not in [node1, node2]:
                    abstractNode.childrenNeighbors.append(neighbor)
            # Add to lis
            # print "abstract from graph" 
            abstractNodeArray.append(abstractNode)
            # print [node.val for node in abstractNode.children]
        # print "count", count
        self.nodes = abstractNodeArray
        print "level ndoes: ", len(self.nodes)

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
                    	# print child.val, " -> ", neighborNode.val
                        node.neighbors.append(neighborNode)
        # for node in self.nodes:
        	# print , node.childrenNeighbors
        #for node in self.nodes:
	     #   print [child.val for child in node.children]

    def getAbstractMap(self, obstacles):
    	self.mapToGraph(obstacles)
        self.addNeighbors()
        self.getAbstractArray()
        self.getAbstractGraph()
        self.abstractHead = self.nodes[0]
        # return self.head

    def levelUp(self, abstractHead):
    	self.head = abstractHead
    	# print "second level up"
    	self.getAbstractArray()
        self.getAbstractGraph()
        self.abstractHead = self.nodes[0]
        # for i in self.nodes:
        #     print i.positions
        # print "level", abstractHead.level
        # return self

    def getNode(self, position):
        for node in self.nodes:
            if position in node.positions:
                # print "found node"
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




