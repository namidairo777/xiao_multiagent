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
		# map 
		

	def mapToGraph(self, obstacles):
		"""
		Translate current 2-dimension array to node array
		"""
		# obstacles to node array
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

		# Assign neighbors
		for x in range(len(obstacles)):
			for y in range(len(obstacles[0])):
				self.nodeArray[][]
				if node[x][y]:
					
					node = Node()
					node.x = x
					node.y = y
				row.append(node)
			graph.append(row)

	def getAbstractMap(self):
		"""
		graph -> abstraction map

		"""



