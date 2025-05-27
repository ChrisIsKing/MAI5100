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
        discount factor.  The Bird is in the tree
        Roy can jump. The dog can jump. The goat can jump.
        Pat can jump.  I am with daddy. I am with granny.
        I am with sister.
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
        self.values =util.Counter() # A Counter is a dict with default 0




        self.runValueIteration()

    def runValueIteration(self):
        """
          Run the value iteration algorithm. Note that in standard
          value iteration, V_k+1(...) depends on V_k(...)'s.
        """
        "*** YOUR CODE HERE ***"
        # get available actions  of the gridworld :
        allStates=self.mdp.getStates()

        for iteration in  range (self.iterations):


            #for each state  calulate Vpi(s)=Qpi(s') if the posittion is not terminal
            # get all actions to take from a given postions
            tempvalues=util.Counter()
            #if iteration==1:
            #print([item for item in tempvalues])
            for currentState  in allStates:
                 #update the mdp value array "self.values" for each state if it better that the last iteration
                 #if a state is nt terminal calculate Qpi(s') else leave as 0(default)
                 if self.mdp.isTerminal(currentState):
                     #print("printing terminalState ",self.values[currentState])
                     prints="kello"
                 else:
                     #get all possible actions of current state
                     actionsOnStates=self.mdp.getPossibleActions(currentState)

                     maxQvalue=float('-inf')

                     #calculate Qvalues  for all sates by executing an action
                     for action in actionsOnStates:
                         if iteration==0:
                             nextStateProbability=self.mdp.getTransitionStatesAndProbs(currentState,action)
                             #print("action",currentState,action,[[result,prob] for result,prob in nextStateProbability])

                         Qvalue=self.getQValue(currentState,action)
                         if Qvalue>maxQvalue:
                             maxQvalue=Qvalue

                         #if the newwly calculater is different from the current vlaue update it.  else leave it the same ( think it  chcking agaisns difference rather than grather )'''
                         '''if Qvalue>self.values[currentState]:
                             self.values[currentState]=Qvalue'''
                     #print("printing tempvalues",tempvalues)
                     tempvalues[currentState]=maxQvalue
            self.values=tempvalues






    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):

        Qvalue=0

        #print("Printing Initial values",[item for item in self.values])
        #calculete SUM { T(s,a,s')[R(s,a s')+lamda V(s')]}
        #nextStateProbability contains all possible states from  current state if we take the  action "action" passed as parameter
        nextStateProbability=self.mdp.getTransitionStatesAndProbs(state,action)

        for nextState in nextStateProbability:
            #get reward for the transiton what

            '''transitonProbability=nextState[1]# transition Probabilty
            reward=self.mdp.getReward(state,action,nextState[0])#Immediate
            VsPrime=self.discount*self.values[nextState[0]] # was looking at the current state  looking back at the formula  its the next not the current
            Qvalue=transitonProbability*(reward+VsPrime)'''

            transitonProbability=nextState[1]# transition Probabilty
            reward=self.mdp.getReward(state,action,nextState[0])#Immediate
            VsPrime=self.discount*self.values[nextState[0]] # was looking at the current state  looking back at the formula  its the next not the current
            Qvalue=Qvalue+transitonProbability*(reward+VsPrime)



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
        maxQvalue=float('-inf')
        bestAction=None

        if self.mdp.isTerminal(state):
            return 0

        actionsOnStates=self.mdp.getPossibleActions(state)

        for action in actionsOnStates:
             #for  i in range(self.iterations):
             Qvalue=self.getQValue(state,action)

             if Qvalue>maxQvalue:

                 #print("printting when different",self.values[state])
                 bestAction=action
                 maxQvalue=Qvalue
                 bestAction=action

        '''tempvalues=[]
        #calculate Qvalues  for all sates by executing an action

        for action in actionsOnStates:

            Qvalue=self.getQValue(state,action)

            tempvalues.append((Qvalue,action))


        maxi=-float('-inf')
        for k,v in tempvalues:
            if k<maxi:
                bestAction=v'''


        return bestAction
        #return self.values[state]







        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
