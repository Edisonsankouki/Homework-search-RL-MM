import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        #update the values

        states = self.mdp.getStates()

        for i in range(0,iterations):
            value = util.Counter()
            for s in states:
                action = self.getAction(s)
                if action != None:
                    value[s] = self.getQValue(s,action)
            self.values = value
        # Write value iteration code here
        "*** YOUR CODE HERE ***"


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # Q(s,a) = sum(s') * T(s,a,s;)*[R(s,a,s')+V_
        result = 0
        TransitionStatesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)

        for x in TransitionStatesAndProbs:
            transition = x[0]
            prob = x[1]
            R = self.mdp.getReward(state, action, transition)
            value = self.getValue(transition)
            result+=prob*(R+self.discount*value)
        return result






    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        def getkey(elem):
            return elem[1]
        actions = self.mdp.getPossibleActions(state)
        if self.mdp.isTerminal(state):
            return None
        else:
            maxarray = []
            for action in actions:
                Qvalue = self.getQValue(state,action)
                maxarray.append([action,Qvalue])
            maxarray.sort(key=getkey,reverse=True)
            return maxarray[0][0]




    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
