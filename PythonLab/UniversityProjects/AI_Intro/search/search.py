# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
	"""
	This class outlines the structure of a search problem, but doesn't implement
	any of the methods (in object-oriented terminology: an abstract class).

	You do not need to change anything in this class, ever.
	"""

	def getStartState(self):
		"""
		Returns the start state for the search problem
		"""
		util.raiseNotDefined()

	def isGoalState(self, state):
		"""
		  state: Search state

		Returns True if and only if the state is a valid goal state
		"""
		util.raiseNotDefined()

	def getSuccessors(self, state):
		"""
		  state: Search state

		For a given state, this should return a list of triples,
		(successor, action, stepCost), where 'successor' is a
		successor to the current state, 'action' is the action
		required to get there, and 'stepCost' is the incremental
		cost of expanding to that successor
		"""
		util.raiseNotDefined()

	def getCostOfActions(self, actions):
		"""
		 actions: A list of actions to take

		This method returns the total cost of a particular sequence of actions.  The sequence must
		be composed of legal moves
		"""
		util.raiseNotDefined()


def tinyMazeSearch(problem):
	"""
	Returns a sequence of moves that solves tinyMaze.  For any other
	maze, the sequence of moves will be incorrect, so only use this for tinyMaze
	"""
	from game import Directions
	s = Directions.SOUTH
	w = Directions.WEST
	return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
	"""
	Search the deepest nodes in the search tree first [p 74].

	Your search algorithm needs to return a list of actions that reaches
	the goal.  Make sure to implement a graph search algorithm [Fig. 3.18].

	To get started, you might want to try some of these simple commands to
	understand the search problem that is being passed in:

	print "Start:", problem.getStartState()
	print "Is the start a goal?", problem.isGoalState(problem.getStartState())
	print "Start's successors:", problem.getSuccessors(problem.getStartState())
	"""
	# implementing the DFS by giving the stack as a structure
	structure = util.Stack()
	first_node = [problem.getStartState(), [], 0]
	structure.push(first_node)
	return search_in_a_graph(problem, structure)


def breadthFirstSearch(problem):
	"Search the shallowest nodes in the search tree first. [p 74]"
	# implementing the BFS by giving the Queue as a structure
	structure = util.Queue()
	first_node = [problem.getStartState(), [], 0]
	structure.push(first_node)
	return search_in_a_graph(problem, structure)


def uniformCostSearch(problem):
	"Search the node of least total cost first. "
	# implementing the UCS by giving the PriorityQueue as a structure,
	# and setting the function to just take the 3 argument ( [ ,  , the cost] )
	structure = util.PriorityQueueWithFunction(lambda node: node[2])
	first_node = [problem.getStartState(), [], 0]
	structure.push(first_node)
	return search_in_a_graph(problem, structure)


def nullHeuristic(state, problem=None):
	"""
	A heuristic function estimates the cost from the current state to the nearest
	goal in the provided SearchProblem.  This heuristic is trivial.
	"""
	return 0


def aStarSearch(problem, heuristic=nullHeuristic):
	"Search the node that has the lowest combined cost and heuristic first."
	# implementing the A* by giving the PriorityQueue as a structure,
	# and setting the function to clac: f(node) = g(node) + h(node) : cost + heuristic(state,problem)
	structure = util.PriorityQueueWithFunction(lambda node: node[2] + heuristic(node[0], problem))
	first_node = [problem.getStartState(), [], 0]
	structure.push(first_node)
	return search_in_a_graph(problem, structure)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch


def search_in_a_graph(problem, structure):
	"""
	This method implement the algorithm of searching in a graph, using a given structure.
	The algorithm in each itterate (until the structure is empty), take the top node in the structure,
		and look if it is the goal, if not, it enter node of each child.
		It check before working on a node, if the node was explored already.
		Each node in the structure is typle(state, actions, cost)
	:param problem: the game state that gives information about the world.
	:param structure: a structure that implement pop,push,isEmpty function, in different ways.
	:return: list of actions to goal.
	"""
	explord = set()
	while not structure.isEmpty():
		node = structure.pop()
		parent_state = node[0]
		parent_actions = node[1]
		parent_cost = node[2]
		if parent_state not in explord:
			explord.add(parent_state)
			if problem.isGoalState(parent_state):
				return parent_actions
			# else: means there is nothing to do with parent but we will use it as a path to his children
			for child_state, child_action, child_cost in problem.getSuccessors(parent_state):
				node = [child_state, parent_actions + [child_action], parent_cost + child_cost]
				structure.push(node)
	return []
