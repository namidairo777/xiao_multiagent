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
		self.x = 0 				# coordinate x
		self.y = 0				# coordinate y
		self.val = 0
		self.level = level      # abstraction level
		self.isAbstracted = False    # abtracted or not
		self.neighbors = []		# neighbor nodes
		self.children = []		# child nodes (abtraction level - 1)
		self.childrenNeighbors = [] # child's neighbors (abtraction level - 1), convinient for connnect graph

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

	def mapToGraph(self, obstacles):
		"""
		Translate current 2-dimension array to node array
		"""
		# obstacles to node array
		self.height = len(obstacles)
		self.width = len(obstacles[0])
		graph = []
		i = 1
		for x in range(len(obstacles)):
			row = []
			for y in range(len(obstacles[0])):
				node = None
				if not obstacles[x][y]:
					# if (x, y) is not obstacle
					node = Node()
					node.x = x
					node.y = y
					node.val = i
					i += 1 
				row.append(node)
			graph.append(row)
		self.nodeArray = graph
		self.head = nodeArray[0][0]

		
	def addNeighbors(self):
		"""
		Assign neighbors to each node
		"""
		for x in range(len(obstacles)):
			for y in range(len(obstacles[0])):
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
			abstractNode.children.append(node2)
			for neighbor in (node1.neighbors + node2.neighbors):
				if neighbor not in [node1, node2]:
					abstractNode.childrenNeighbors.append(neighbor)
			# Add to list 
			abstractNodeArray.append(abstractNode)
			# set position x and y

		return self.abstractNodeArray

	def getAbstractGraph(self, graph):
		for node in graph:
			
			# Assign every other node which has these neighbor node as this node's neighbor





class Test(object):
	
	"""Test class"""
	def do(self):
		obstacles = [[False for i in range(10)] for j in range(10)]
		a = Abstraction()
		a.mapToGraph(obstacles)




