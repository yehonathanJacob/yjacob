# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import random
import util

from util import manhattanDistance
from game import Agent


class ReflexAgent(Agent):
	"""
	  A reflex agent chooses an action at each choice point by examining
	  its alternatives via a state evaluation function.
  
	  The code below is provided as a guide.  You are welcome to change
	  it in any way you see fit, so long as you don't touch our method
	  headers.
	"""

	def __init__(self):
		# a dictionery to save how many time we have visited a place, so it wont stack on the same palce.
		self.numberOfVisit = {}

	def __cal_ghost_next_position(self, ghost):
		"""
		:param ghost: ghost to calc position + next move
		:return: the next move
		"""
		current = ghost.getPosition()
		direction = ghost.getDirection()
		if direction == 'East':
			return (current[0] + 1, current[0])
		elif direction == 'North':
			return (current[0], current[0] + 1)
		elif direction == 'South':
			return (current[0], current[0] - 1)
		elif direction == 'West':
			return (current[0] - 1, current[0])
		return current

	def getAction(self, gameState):
		"""
		You do not need to change this method, but you're welcome to.
	
		getAction chooses among the best options according to the evaluation function.
	
		Just like in the previous project, getAction takes a GameState and returns
		some Directions.X for some X in the set {North, South, West, East, Stop}
		"""
		# Collect legal moves and successor states
		legalMoves = gameState.getLegalActions()

		# Choose one of the best actions
		scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
		bestScore = max(scores)
		bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
		chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

		"Add more of your code here if you want to"
		selectedActiont = legalMoves[chosenIndex]
		successorGameState = gameState.generatePacmanSuccessor(selectedActiont)
		newPos = successorGameState.getPacmanPosition()
		self.numberOfVisit[newPos] += 1
		return selectedActiont

	def evaluationFunction(self, currentGameState, action):
		"""
		Design a better evaluation function here.
	
		The evaluation function takes in the current and proposed successor
		GameStates (pacman.py) and returns a number, where higher numbers are better.
	
		The code below extracts some useful information from the state, like the
		remaining food (oldFood) and Pacman position after moving (newPos).
		newScaredTimes holds the number of moves that each ghost will remain
		scared because of Pacman having eaten a power pellet.
	
		Print out these variables to see what you're getting, then combine them
		to create a masterful evaluation function.
		"""
		# Useful information you can extract from a GameState (pacman.py)
		successorGameState = currentGameState.generatePacmanSuccessor(action)
		newPos = successorGameState.getPacmanPosition()
		oldFood = currentGameState.getFood()
		newGhostStates = successorGameState.getGhostStates()

		# adding this position to visiting list
		if newPos not in self.numberOfVisit:
			self.numberOfVisit[newPos] = 0

		# check if we are nex to a ghost
		for ghost in newGhostStates:
			currentGhostPosition = ghost.getPosition()
			nextGhostPosition = self.__cal_ghost_next_position(ghost)
			if currentGhostPosition == newPos or nextGhostPosition == newPos:
				# if it's sceard eat it, else run away
				if ghost.scaredTimer == 0:
					return float('-inf')
				else:
					return float('inf')

		# if there is no ghost , now check if there is any food to go to.
		if oldFood.count() == 0:
			# if there is no ghost and no food, give priority only to 'Stop'
			if action == 'Stop':
				return 1
			else:
				return -1
		else:
			# if there is food, give back value of the closest food, and don't permit Stop
			if action == 'Stop':
				return float('-inf')
			closest = min([manhattanDistance(newPos, food) for food in oldFood.asList()])
			# send back the negative of the distance, so the closets will picked up + successor so we wont go back on our way
			return (-1 * closest) - self.numberOfVisit[newPos]


def scoreEvaluationFunction(currentGameState):
	"""
	  This default evaluation function just returns the score of the state.
	  The score is the same one displayed in the Pacman GUI.
  
	  This evaluation function is meant for use with adversarial search agents
	  (not reflex agents).
	"""
	return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
	"""
	  This class provides some common elements to all of your
	  multi-agent searchers.  Any methods defined here will be available
	  to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.
  
	  You *do not* need to make any changes here, but you can if you want to
	  add functionality to all your adversarial search agents.  Please do not
	  remove anything, however.
  
	  Note: this is an abstract class: one that should not be instantiated.  It's
	  only partially specified, and designed to be extended.  Agent (game.py)
	  is another abstract class.
	"""

	def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
		self.index = 0  # Pacman is always agent index 0
		self.evaluationFunction = util.lookup(evalFn, globals())
		self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
	"""
	  Your minimax agent (question 2)
	"""

	def getAction(self, gameState):
		"""
		  Returns the minimax action from the current gameState using self.depth
		  and self.evaluationFunction.
	
		  Here are some method calls that might be useful when implementing minimax.
	
		  gameState.getLegalActions(agentIndex):
			Returns a list of legal actions for an agent
			agentIndex=0 means Pacman, ghosts are >= 1
	
		  Directions.STOP:
			The stop direction, which is always legal
	
		  gameState.generateSuccessor(agentIndex, action):
			Returns the successor game state after an agent takes an action
	
		  gameState.getNumAgents():
			Returns the total number of agents in the game
		"""
		minimaxRes = self.get_direction_from_minimax(gameState, 0, 0)
		return minimaxRes[1]

	def get_direction_from_minimax(self, gameState, agent_number, depth):
		"""
		:param game_state: the curent game state.
		:param agent_number: agent_number % gameState.getNumAgents() == 0 for packmer, else for ghost
		:param depth: depth of game we are
		:return: minimax value, and action to this minimax
		"""
		# check if there is where to go deap more: if we are over depth, or if there is no legal action to this agent, or game over- we win or lose.
		if depth >= self.depth or len(
				gameState.getLegalActions(agent_number)) == 0 or gameState.isWin() or gameState.isLose():
			return self.evaluationFunction(gameState), 'Stop'

		nextAgentNumber = agent_number + 1
		# if nextAgentNumber == gameState.getNumAgents() means we have expose all agent in this action, so we are going to next depth
		if nextAgentNumber == gameState.getNumAgents():
			nextAgentNumber = 0
			nextDepth = depth + 1
		else:
			nextDepth = depth

		# generate all next posiable [sates, action]
		minimaxList = []
		for action in gameState.getLegalActions(agent_number):
			if action != 'Stop':
				nextGameSate = gameState.generateSuccessor(agent_number, action)
				minimaxValue = self.get_direction_from_minimax(nextGameSate, nextAgentNumber, nextDepth)[0]
				minimaxList.append([minimaxValue, action])

		if agent_number == 0:
			return max(minimaxList, key=lambda ls: ls[0])
		else:
			return min(minimaxList, key=lambda ls: ls[0])


class AlphaBetaAgent(MultiAgentSearchAgent):
	"""
	  Your minimax agent with alpha-beta pruning (question 3)
	"""

	def getAction(self, gameState):
		"""
		  Returns the minimax action using self.depth and self.evaluationFunction
		"""
		minimaxRes = self.get_direction_from_minimax(gameState, 0, 0, float('-inf'), float('inf'))
		return minimaxRes[1]

	def get_direction_from_minimax(self, gameState, agent_number, depth, a, b):
		"""
		:param game_state: the curent game state.
		:param agent_number: agent_number % gameState.getNumAgents() == 0 for packmer, else for ghost
		:param depth: depth of game we are
		:return: minimax value, and action to this minimax
		"""
		# check if there is where to go deap more: if we are over depth, or if there is no legal action to this agent, or game over- we win or lose.
		if depth >= self.depth or len(
				gameState.getLegalActions(agent_number)) == 0 or gameState.isWin() or gameState.isLose():
			return self.evaluationFunction(gameState), 'Stop'

		nextAgentNumber = agent_number + 1
		# if nextAgentNumber == gameState.getNumAgents() means we have expose all agent in this action, so we are going to next depth
		if nextAgentNumber == gameState.getNumAgents():
			nextAgentNumber = 0
			nextDepth = depth + 1
		else:
			nextDepth = depth

		# generate all next posiable [sates, action]
		minimaxList = []
		for action in gameState.getLegalActions(agent_number):
			if action != 'Stop':
				nextGameSate = gameState.generateSuccessor(agent_number, action)
				minimaxValue = self.get_direction_from_minimax(nextGameSate, nextAgentNumber, nextDepth, a, b)[0]
				if agent_number == 0:  # case, I agent looks for maximum, and parent look for minimum
					if minimaxValue >= b:
						return [minimaxValue, action]  # this wont return less then minimaxValue
					a = max(a, minimaxValue)
				else:  # case, I agent looks for minimum, and parent look for maximum
					if minimaxValue <= a:
						return [minimaxValue, action]  # this wont return more then minimaxValue
					b = min(b, minimaxValue)
				minimaxList.append([minimaxValue, action])

		if agent_number == 0:
			return max(minimaxList, key=lambda ls: ls[0])
		else:
			return min(minimaxList, key=lambda ls: ls[0])


class ExpectimaxAgent(MultiAgentSearchAgent):
	"""
	  Your expectimax agent (question 4)
	"""

	def getAction(self, gameState):
		"""
		  Returns the expectimax action using self.depth and self.evaluationFunction
	
		  All ghosts should be modeled as choosing uniformly at random from their
		  legal moves.
		"""
		minimaxRes = self.get_direction_from_minimax(gameState, 0, 0)
		return minimaxRes[1]

	def get_direction_from_minimax(self, gameState, agent_number, depth):
		"""
		:param game_state: the curent game state.
		:param agent_number: agent_number % gameState.getNumAgents() == 0 for packmer, else for ghost
		:param depth: depth of game we are
		:return: minimax value, and action to this minimax
		"""
		# check if there is where to go deap more: if we are over depth, or if there is no legal action to this agent, or game over- we win or lose.
		if depth >= self.depth or len(
				gameState.getLegalActions(agent_number)) == 0 or gameState.isWin() or gameState.isLose():
			return self.evaluationFunction(gameState), 'Stop'

		nextAgentNumber = agent_number + 1
		# if nextAgentNumber == gameState.getNumAgents() means we have expose all agent in this action, so we are going to next depth
		if nextAgentNumber == gameState.getNumAgents():
			nextAgentNumber = 0
			nextDepth = depth + 1
		else:
			nextDepth = depth

		# generate all next posiable [sates, action]
		minimaxList = []
		for action in gameState.getLegalActions(agent_number):
			if action != 'Stop':
				nextGameSate = gameState.generateSuccessor(agent_number, action)
				minimaxValue = self.get_direction_from_minimax(nextGameSate, nextAgentNumber, nextDepth)[0]
				minimaxList.append([minimaxValue, action])

		if agent_number == 0:
			return max(minimaxList, key=lambda ls: ls[0])
		else:
			# ghost will pick random from minimaxList
			return random.choice(minimaxList)


def betterEvaluationFunction(currentGameState):
	"""
	  Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
	  evaluation function (question 5).
  
	  DESCRIPTION: <write something here so we know what you did>
	"""
	"*** YOUR CODE HERE ***"
	util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction


class ContestAgent(MultiAgentSearchAgent):
	"""
	  Your agent for the mini-contest
	"""

	def getAction(self, gameState):
		"""
		  Returns an action.  You can use any method you want and search to any depth you want.
		  Just remember that the mini-contest is timed, so you have to trade off speed and computation.
	
		  Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
		  just make a beeline straight towards Pacman (or away from him if they're scared!)
		"""
		"*** YOUR CODE HERE ***"
		util.raiseNotDefined()
