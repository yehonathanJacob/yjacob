Name: Yehonathan Jacob
ID: 316304740
date: 07/11/2019


I ve created a fucntion that search in a graf (named: search_in_a_graph) that in each itteration gos to the top of the structure, and check nod if it is a goal, if not it push his childs to the structure.

Q1: I used search_in_a_graph with structure Stack. Time: O(b^d) Palce: O(b*d). this is efficiant in palce. but don't give optimal result.
Q2: I used search_in_a_graph with structure Queue. Time: O(b^d) Palce: O(b^d). this is not efficiant in plcae such as DFS but, it gives an optimal result.
Q3: I used search_in_a_graph with structure PriorityQueueWithFunction and I gave the function g(n) wich is the cost until this node.
Q4: I used search_in_a_graph with structure PriorityQueueWithFunction and I gave a function that calc also the huristic in it such as f(node) = g(node) + h(node)
	to the openMaze happend that for the first time we use a data that was not declatred or verify yet, this is the actual studing of the agent.
Q5: we change the state from porviding (x,y) to provide ((x,y), rest corner) so in this way every time we give a successors of a node we bring back also wich corner will stay after passing throuw this point.
	plus we are cheking in the isGoalState if the number of corner left is 0.
Q6: we implement the uristic by cheking the distance to the closest corner and from that corner to another, and like this we heurist a length of theoretical path to go throuw all the corners.
Q7: we implement the same heurist from Q6 but this time we use mazeDistance, so to be sure the distnace wont be less then expected to other points.
	And we save the data, so the we wont need to re-calcuate it again.
Q8: we gave the option to the agent to check if he arrive to a corner, and then we implement bfs algorithem on each food, and like this we know what is the closest.
