import search

def UnConsistency(state,problem=None):
	"""
	h(n) <= c(n,a,n') + h(n')	X
	h(n) <= h*(n)				V
		   [B,4]
	    1/      \1
	[A,5]	      [D,1] -1- [E,0]
		 1\     /2
	       [C,0]
	"""
	dic = {'A': 5, 'B': 4, 'C': 0, 'D': 1, 'E': 0}
	return dic[state]

def Consistency(state,problem=None):
	"""
	h(n) <= c(n,a,n') + h(n')	X
	h(n) <= h*(n)				V
		   [B,3]
	    1/      \1
	[A,5]	      [D,1] -1- [E,0]
		 1\     /2
	       [C,4]
	"""
	dic = {'A': 5, 'B': 3, 'C': 4, 'D': 1, 'E': 0}
	return dic[state]

class DumyProblem():

	def __init__(self):
		self.successors = {'A':[['B','up->B',1],['C','down->C',1]],
						   'B':[['D','down->D',1]],
						   'C':[['D','up->D',2]],
						   'D':[['E','right->E',1]]}
	def getStartState(self):
		return 'A'
	def isGoalState(self,state):
		return state == 'E'
	def getSuccessors(self,state):
		return self.successors[state]

if __name__ == '__main__':
	problem = DumyProblem()
	heuristic = UnConsistency
	print(search.aStarSearch(problem, heuristic))

