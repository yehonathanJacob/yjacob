from util import Pair
import copy
from propositionLayer import PropositionLayer
from planGraphLevel import PlanGraphLevel
from action import Action
from Parser import Parser

class GraphPlan(object):
  """
  A class for initializing and running the graphplan algorithm
  """

  def __init__(self,domain, problem):
    """
    Constructor
    """
    self.independentActions = []
    self.noGoods = []
    self.graph = []
    p = Parser(domain, problem)
    self.actions, self.propositions = p.parseActionsAndPropositions()   # list of all the actions and list of all the propositions
    self.initialState, self.goal = p.pasreProblem() 					# the initial state and the goal state are lists of propositions
    self.createNoOps() 													# creates noOps that are used to propagate existing propositions from one layer to the next
    self.independent() 													# creates independent actions list and updates self.independentActions
    PlanGraphLevel.setIndependentActions(self.independentActions)
    PlanGraphLevel.setActions(self.actions)
    PlanGraphLevel.setProps(self.propositions)
 
    
  def graphPlan(self): 
    """
    The graphplan algorithm. 
    The code calls the extract function which you should complete below
    """    
    #initialization
    initState = self.initialState
    level = 0
    self.noGoods = [] #make sure you update noGoods in your backward search!
    self.noGoods.append([])
    #create first layer of the graph, note it only has a proposition layer which consists of the initial state.
    propLayerInit = PropositionLayer()
    for prop in initState:
      propLayerInit.addProposition(prop)
    pgInit = PlanGraphLevel()
    pgInit.setPropositionLayer(propLayerInit)
    self.graph.append(pgInit)   
    
    """
    While the layer does not contain all of the propositions in the goal state,
    or some of these propositions are mutex in the layer we,
    and we have not reached the fixed point, continue expanding the graph
    """
   
    while self.goalStateNotInPropLayer(self.graph[level].getPropositionLayer().getPropositions()) or \
        self.goalStateHasMutex(self.graph[level].getPropositionLayer()):
      if self.isFixed(level):
        return None #this means we stopped the while loop above because we reached a fixed point in the graph. nothing more to do, we failed!
        
      self.noGoods.append([])
      level = level + 1
      pgNext = PlanGraphLevel() #create new PlanGraph object
      pgNext.expand(self.graph[level - 1]) #calls the expand function, which you are implementing in the PlanGraph class
      self.graph.append(pgNext) #appending the new level to the plan graph
    
      sizeNoGood = len(self.noGoods[level]) #remember size of nogood table
    
    plan = self.extract(self.graph, self.goal, level) #try to extract a plan since all of the goal propositions are in current graph level, and are not mutex
    while(plan is None): #while we didn't extract a plan successfully       
      level = level + 1 
      self.noGoods.append([])
      pgNext = PlanGraphLevel() #create next level of the graph by expanding
      pgNext.expand(self.graph[level - 1]) #create next level of the graph by expanding
      self.graph.append(pgNext)
      plan = self.extract(self.graph, self.goal, level) #try to extract a plan again
      if (plan is None and self.isFixed(level)): #if failed and reached fixed point
        if sizeNoGood == len(self.noGoods[level]): #if size of nogood didn't change, means there's nothing more to do. We failed.
          return None
        sizeNoGood = len(self.noGoods[level]) #we didn't fail yet! update size of no good
    return plan
   

  def extract(self, Graph, subGoals, level):
    """
    The backsearch part of graphplan that tries
    to extract a plan when all goal propositions exist in a graph plan level.	
    """
    
    if level == 0:
      return []
    if subGoals in self.noGoods[level]:
      return None
    plan = self.gpSearch(Graph, subGoals, [], level)
    if plan is not None:
      return plan
    self.noGoods[level].append([subGoals])
    return None
     
  def gpSearch(self, Graph, subGoals, plan, level):
    if subGoals == []:
      newGoals = []
      for action in plan:
        for prop in action.getPre():
          if prop not in newGoals:
            newGoals.append(prop)						
      newPlan = self.extract(Graph, newGoals, level - 1)
      if newPlan is None:
        return None
      else:
        return newPlan + plan
		
    prop = subGoals[0]
    providers = []
    for action1 in [act for act in Graph[level].getActionLayer().getActions() if prop in act.getAdd()]:
      noMutex = True
      for action2 in plan:
        if Pair(action1, action2) not in self.independentActions:
          noMutex = False
          break
      if noMutex:
        providers.append(action1)
    for action in providers:
      newSubGoals = [g for g in subGoals if g not in action.getAdd()]
      planClone = list(plan)
      planClone.append(action)
      newPlan = self.gpSearch(Graph, newSubGoals, planClone, level)
      if newPlan is not None:
        return newPlan
    return None
    
	
  def goalStateNotInPropLayer(self, propositions):
    """
    Helper function that receives a  list of propositions (propositions) and returns true 
    if not all the goal propositions are in that list    
    """
    for goal in self.goal:
      if goal not in propositions:
        return True
    return False	
	
  def goalStateHasMutex(self, propLayer):
    """
    Helper function that checks whether all goal propositions are non mutex at the current graph level
    """
    for goal1 in self.goal:
      for goal2 in self.goal:
        if propLayer.isMutex(goal1,goal2):
          return True
    return False
	
  def isFixed(self, level):
    """
    Checks if we have reached a fixed point, i.e. each level we'll expand would be the same, thus no point in continuing
    """
    if level == 0:
      return False
    
    if len(self.graph[level].getPropositionLayer().getPropositions()) == len(self.graph[level - 1].getPropositionLayer().getPropositions()) and \
      len(self.graph[level].getPropositionLayer().getMutexProps()) == len(self.graph[level - 1].getPropositionLayer().getMutexProps()):
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
      prop.addProducer(act)
   
  def independent(self):
    """
    Creates a list of independent actions
    """
    for act1 in self.actions:
      for act2 in self.actions:
        if independentPair(act1,act2):
          self.independentActions.append(Pair(act1,act2)) 

  def isIndependent(self, a1, a2):
    return Pair(a1,a2) in self.independentActions  
  
	
  def noMutexActionInPlan(self, plan, act, actionLayer):
    """
    Helper action that you may want to use when extracting plans,
    returns true if there are no mutex actions in the plan
    """
    for planAct in plan:
      if actionLayer.isMutex(Pair(planAct,act)):
        return False
    return True  

def independentPair(a1, a2):
  """
  Returns true if the actions are neither have inconsistent effects
  nor they interfere one with the other.
  You might want to use those functions:
  a1.getPre() returns the pre list of a1
  a1.getAdd() returns the add list of a1
  a1.getDelete() return the del list of a1
  a1.isPreCond(p) returns true is p is in a1.getPre()
  a1.isPosEffect(p) returns true is p is in a1.getAdd()
  a1.isNegEffect(p) returns true is p is in a1.getDel()
  """

  # first we will check if a1 != a2 because other wise, we can expect them to not contradict each other.
  if a1 == a2:
    return True

  # for each of the action (a1 then a2) we will check that each precondition that action delete,
  # dose not apper in the precondition list od add list of the other action (a2 then a1)
  for ai, aj in zip([a1,a2],[a2,a1]): # first we will check a1 to a2 and then other wisw
    if not check_precondition(ai,aj):
      return False

  # if they dont contradict each other, we will return True
  return True

def check_precondition(ai,aj):
  """
  ai: action to check the delete list
  aj: action to check the add and precondition list
  :return: False if aj contradict ai, or True other wise.
  """
  for precondition in ai.getDelete():
    if aj.isPreCond(precondition) or aj.isPosEffect(precondition):
      return False
  return True

if __name__ == '__main__':  
  import sys
  import time
  if len(sys.argv) != 1 and len(sys.argv) != 3:
    print("Usage: GraphPlan.py domainName problemName")
    exit()
  domain = 'dwrDomain.txt'
  problem = 'dwrProblem.txt'
  if len(sys.argv) == 3:
    domain = str(sys.argv[1])
    problem = str(sys.argv[2])

  gp = GraphPlan(domain, problem)
  start = time.time()
  plan = gp.graphPlan()
  elapsed = time.time() - start
  if plan is not None:
    print("Plan found with %d actions in %.2f seconds" % (len([act for act in plan if not act.isNoOp()]), elapsed))
  else:
    print("Could not find a plan in %.2f seconds" %  elapsed)
 
