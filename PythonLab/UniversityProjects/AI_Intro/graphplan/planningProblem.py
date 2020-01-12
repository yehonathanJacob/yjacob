from util import Pair
import copy
from propositionLayer import PropositionLayer
from planGraphLevel import PlanGraphLevel
from Parser import Parser
from action import Action

try:
  from search import SearchProblem
  from search import aStarSearch

except:
  from  CPF.search import SearchProblem
  from  CPF.search import aStarSearch

class PlanningProblem():
  def __init__(self, domain, problem):
    """
    Constructor
    """
    p = Parser(domain, problem)
    self.actions, self.propositions = p.parseActionsAndPropositions()	
                                            # list of all the actions and list of all the propositions
    self.initialState, self.goal = p.pasreProblem() 				
                                            # the initial state and the goal state are lists of propositions
    self.createNoOps() 											# creates noOps that are used to propagate existing propositions from one layer to the next
    PlanGraphLevel.setActions(self.actions)
    PlanGraphLevel.setProps(self.propositions)
    self._expanded = 0
   
    
  def getStartState(self):
    return self.initialState
    
  def isGoalState(self, state):
    """
    Hint: you might want to take a look at goalStateNotInPropLayer function
    """
    propositions = state
    return not self.goalStateNotInPropLayer(propositions)
    
  def getSuccessors(self, state):
    """   
    For a given state, this should return a list of triples, 
    (successor, action, stepCost), where 'successor' is a 
    successor to the current state, 'action' is the action
    required to get there, and 'stepCost' is the incremental 
    cost of expanding to that successor, 1 in our case.
    You might want to this function:
    For a list of propositions l and action a,
    a.allPrecondsInList(l) returns true if the preconditions of a are in l
    """
    self._expanded += 1
    results = []
    for a in self.actions:
      # if an action is not an noOp, and all preconditions are met in the current state
      if a.isNoOp():
        continue
      if a.allPrecondsInList(state):
        successor = [p for p in a.getAdd() if p not in state]
        successor.extend(state)
        successor = [p for p in successor if p not in a.getDelete()]
        results.append((successor, a, 1))

    return results

  def getCostOfActions(self, actions):
    return len(actions)
    
  def goalStateNotInPropLayer(self, propositions):
    """
    Helper function that returns true if all the goal propositions 
    are in propositions
    """
    for goal in self.goal:
      if goal not in propositions:
        return True
    return False

  def createNoOps(self):
    """
    Creates the noOps that are used to propagate propositions from one layer to the next
    """
    for prop in self.propositions:
      name = prop.name
      precon = []
      add = []
      precon.append(prop)
      add.append(prop)
      delete = []
      act = Action(name,precon,add,delete, True)
      self.actions.append(act)  
      
def maxLevel(state, problem):
  """
  The heuristic value is the number of layers required to expand all goal propositions.
  If the goal is not reachable from the state your heuristic should return float('inf')  
  A good place to start would be:
  propLayerInit = PropositionLayer()          #create a new proposition layer
  for prop in state:
    propLayerInit.addProposition(prop)        #update the proposition layer with the propositions of the state
  pgInit = PlanGraphLevel()                   #create a new plan graph level (level is the action layer and the propositions layer)
  pgInit.setPropositionLayer(propLayerInit)   #update the new plan graph level with the the proposition layer
  """
  propLayerInit = PropositionLayer()
  for prop in state:
    propLayerInit.addProposition(prop)
  pgInit = PlanGraphLevel()
  pgInit.setPropositionLayer(propLayerInit)

  graph = []  # list of PlanGraphLevel objects
  graph.append(pgInit)
  level = 0
  while True:
    # check if this level has the goal
    if problem.goalStateNotInPropLayer(graph[level].getPropositionLayer().getPropositions()):
      break
    # else if the goal is not in this level, and we finished to max graph, meens we vant reach the goal.
    elif isFixed(graph, level):
      return float('inf')

    pgNext = PlanGraphLevel()
    pgNext.expandWithoutMutex(graph[level])
    graph.append(pgNext)
    level += 1
  # if we got into break meens last level contain goal. So lets return the level.
  return level

def levelSum(state, problem):
  """
  The heuristic value is the sum of sub-goals level they first appeared.
  If the goal is not reachable from the state your heuristic should return float('inf')
  """
  propLayerInit = PropositionLayer()
  for prop in state:
    propLayerInit.addProposition(prop)
  pgInit = PlanGraphLevel()
  pgInit.setPropositionLayer(propLayerInit)

  graph = []  # list of PlanGraphLevel objects
  graph.append(pgInit)
  level = 0
  leftGoals = problem.goal.copy()
  level_sum = 0

  while True:
    # if leftGoals is empty, means we reached all the goals.
    if len(leftGoals) == 0:
      break
    # else if the goal is not in this level, and we finished to max graph, meens we vant reach the goal.
    elif isFixed(graph, level):
      return float('inf')
    props = graph[level].getPropositionLayer().getPropositions()
    # check for each goal if it is in the next props. If so, remove it from the left golas, and add the level to the sum
    for goal in leftGoals:
      if goal in props:
        level_sum += level
        leftGoals.remove(goal)

    pgTemp = PlanGraphLevel()
    pgTemp.expandWithoutMutex(graph[level])
    graph.append(pgTemp)
    level += 1
  # adding last level to the sum, and return it
  level_sum += level
  return level_sum

  
def isFixed(Graph, level):
  """
  Checks if we have reached a fixed point,
  i.e. each level we'll expand would be the same, thus no point in continuing
  """
  if level == 0:
    return False  
  return len(Graph[level].getPropositionLayer().getPropositions()) == len(Graph[level - 1].getPropositionLayer().getPropositions())  
      
if __name__ == '__main__':
  import sys
  import time
  if len(sys.argv) != 1 and len(sys.argv) != 4:
    print("Usage: PlanningProblem.py domainName problemName heuristicName(max, sum or zero)")
    exit()
  domain = 'dwrDomain.txt'
  problem = 'dwrProblem.txt'
  heuristic = lambda x,y: 0
  if len(sys.argv) == 4:
    domain = str(sys.argv[1])
    problem = str(sys.argv[2])
    if str(sys.argv[3]) == 'max':
      heuristic = maxLevel
    elif str(sys.argv[3]) == 'sum':
      heuristic = levelSum
    elif str(sys.argv[3]) == 'zero':
      heuristic = lambda x,y: 0
    else:
      print("Usage: PlanningProblem.py domainName problemName heuristicName(max, sum or zero)")
      exit()

  prob = PlanningProblem(domain, problem)
  start = time.time()
  plan = aStarSearch(prob, heuristic)
  elapsed = time.time() - start
  if plan is not None:
    print("Plan found with %d actions in %.2f seconds" % (len(plan), elapsed))
  else:
    print("Could not find a plan in %.2f seconds" %  elapsed)
  print("Search nodes expanded: %d" % prob._expanded)
 
