Name:   Yehonathan Jacob
Id:     316304740
Date:   09/01/2020
*****

Q1).  First I have created a check_precondition function, that check for each deleted precondition in ai if it is exist in
    the precondition or adding los of aj. If so, it return False (mean they are mutex), else it return True.
    After that I send a2 to be cheked with the deleted list of a1, and the opposed.

Q2).  I checked for each a1 precondition and a2 precondition if they are in mutexProps if so, mean a1 and a2 are mutex, so I sand back True
    otherwise I send False.

Q3).  For each action in propositions 1 and 2, we check if they are mutex. We return True if we find at least one pair that is not.

Q4).  For each action that is not in this actionLayer and was in the previous one. We will add it to this layer too (as noOp).

Q5).  For each action i and j in curent action layer, if they are mutex, and not in mutex actions list, we will add them to it.

Q6).  Adding for each proposition that are in the add list of the action in this layer- to the layer's propositions,
    and adding the action that added the proposition to the proposition action list.

Q7).  For each couple of propositions, we check three things: That they are different, not in mutex list alredy, and are actualy mutex.
    Then we add those couple as a Pair to the mutex propositions list.

Q8).  Calling the algorithem: First we update all possible action from previous propositions.
    Then we mark all the mutex between actions. We update all possible propositions from those action + adding old ones.
    Finally we mark all mutex between propositions.

Q9).  In the first domain, I let for the goals to be two different goal.
    For the second I put in goal to opposite goal.

Q10). Implementting some basic getting successors functions.

Q11). Implementting the max heuristics by its logic.

Q12). Implementting the sum heuristics by its logic.

Q13). Creatting an hanoi problem.
    In Propositions, adding the cases: each peg is clear, each disk can be on top/bottom of peg, each disk can be on top a bigger one.
    In Actions adding the cases: move a disk from empty peg to another empty peg, move a disk form top of another disk to empty peg,
    and form empty peg to another biger disk, and last the option moving a disk from a biger disk to another bigger disk.

Q14). Creating the porblem, by define the initial state (Put all disk on a, one top the other, first and last on top and bottom).
    Then define the goal state (Put all disk on c, one top the other, first and last on top and bottom).