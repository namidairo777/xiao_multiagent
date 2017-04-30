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
		self.level = level      # abstraction level
		self.isAbstracted = False    # abtracted or not
		self.neighbors = []		# neighbor nodes
		self.children = []		# child nodes ( abtraction level - 1)

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
		for x in range(len(obstacles)):
			row = []
			for y in range(len(obstacles[0])):
				node = None
				if not obstacles[x][y]:
					# if (x, y) is not obstacle
					node = Node()
					node.x = x
					node.y = y
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



	def getAbstractMap(self, obstacles):
		"""
		graph -> abstraction map
		"""
		# map to graph with neighbors
		self.mapToGraph(obstacles)
		self.addNeighbors()

		# Abstract map
		queue = [self.head]
		# First node neighbors
		while len(queue) != 0:
			# node 1
			node1 = queue.pop(0)
			# Add to queue
			for neighbor in node1.neighbors:
				queue.append(neighbor)
			# node 2
			node2 = queue.pop(0)
			for neighbor in node2.neighbors:
				queue.append(neighbor)



		return self.head




class Test(object):
	"""Test class"""
	def do(self):
		obstacles = [[True for i in range(10)] for j in range(10)]
		a = Abstraction()
		a.mapToGraph(obstacles)




