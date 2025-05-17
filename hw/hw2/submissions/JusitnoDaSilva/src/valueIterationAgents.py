# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp: mdp.MarkovDecisionProcess, discount = 0.9, iterations = 100):
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
        self.runValueIteration()

    def runValueIteration(self):
        """
          Run the value iteration algorithm. Note that in standard
          value iteration, V_k+1(...) depends on V_k(...)'s.
        """
        "*** YOUR CODE HERE ***"
        #available actions:

        allStates=self.mdp.getStates()
        maxQvalue=0
        bestAction=None

        for currentState  in allStates:
             #print(currentState)
             actionsOnStates=self.mdp.getPossibleActions(currentState)
            #calculate Qvalues  for all sates
             for action in actionsOnStates:
                 Qvalue=self.getQValue(currentState,action)
                 if Qvalue>maxQvalue:
                     maxQvalue=Qvalue
                     bestAction=action
        return maxQvalue,action

                 #Get the  reachable states and the  there robability of  reaching these states
                 #probablity=self.mdp.getTransitionStatesAndProbs(currentState,action)
                 #for nextstate in probablity:
                    #get reward for for transiton
                    #reward=self.mdp.getReward(currentState,action,nextstate[0])

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        reward=0
        transitonProbability=0
        Qvalue=0
        #Q value is the expected utility at a chance node

        if self.mdp.isTerminal(state):
            #return Q Value as 0 if the state is a TERMINAL_STATE
            return 0
        else:
            #if is not terminal  calculate  SUM { T(s,a,s')[R(s,a s')+lamda V(s')]}
            #nextStateProbability contains all possible states from  current state
            # if we take action "action"
            nextStateProbability=self.mdp.getTransitionStatesAndProbs(state,action)

            for nextState in nextStateProbability:
                #get reward for the transiton what is lamda()
                transitonProbability=nextState[1]# transition Probabilty
                reward=reward+self.mdp.getReward(state,action,nextState[0])#Immediate
                VsPrime=self.discount*(reward)

                Qvalue=Qvalue+transitonProbability*(reward+VsPrime)
                print(transitonProbability,reward,VsPrime)
            #print(Qvalue)
            return Qvalue


        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def computeActionFromValues(self, state):

        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """

        "*** YOUR CODE HERE ***"
       #we have a state and need an action
        maxQvalue=0
        bestAction=None
        if self.mdp.isTerminal(state):
            return "exit"

        actionsOnStates=self.mdp.getPossibleActions(state)
        #calculate Qvalues  for all sates
        for action in actionsOnStates:
             Qvalue=self.getQValue(state,action)
             if Qvalue>maxQvalue:
                 maxQvalue=Qvalue
                 bestAction=action
                 maxQvalue=Qvalue
        print(action,maxQvalue)
        return bestAction



        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
