Name: Yehonathan Jacob
ID: 316304740
date: 12/11/2019

Q1: I've made the evaluationFunction to first check if we are going to a ghost
    by cheking the packmen next sep + ghost next and current step.
    Then, if we are next ghost; don't go this deriction.
    After we check for some food, if there is no food, it will stop (by giving priority to stop)
    I there is some food, give back rate in ratio to food disstance, but give less point to a place we checked.
    Finaly, to the next selected move, mark in the numberOfVisit dictionary, another time we have been there.

Q2: The function get_direction_from_minimax is getting best minimax value + action to go there, to the selected agent
    The way of going is by every depth, run the recursion on all the agent. so number of recursion is:
    (number of agent)*(number of max depth).
    When it get to maximum depth, so for each agent, it bring back the evaluationFunction.
    Then each agent return the min or max (dependent if it is packmen or ghost) of all the branch.

Q3: The alpha beta algorithem is keeping for each itteration the highest and the lowest respectively.
    For the packmen agent the agent kips in alpha the maximum value that was found, and there if there was found
    higher than beta it send it back (because the ghost wont take more than beta).
    For the ghost we use it as minimum agent for the algorithim.
    Even if the 'parent' of the ghost agent is not the packmen, we will return the first value that will
    be biger than beta because eventialy, this beate come from the packmen.

Q4: For this ghost, because we don't know the actual decision of the ghost, so we pick a randomais choice
    from the actions results.

