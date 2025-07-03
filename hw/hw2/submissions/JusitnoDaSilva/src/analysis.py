# analysis.py
# -----------
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


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.
from valueIterationAgents import ValueIterationAgent
from gridworld import getDiscountGrid
import subprocess
import random
def question2a():




    answerNoise=0
    answerDiscount=0
    answerLivingReward=0
    discount=0
    livingReward=0
    noise=0

    noiseArray=[]
    discountArray=[]
    livingRewardArray=[]
    i=0
    '''while noise<0.9:
        noiseArray.append(noise)
        discountArray.append(noise)
        noise=noise+0.1
    while livingReward>=-0.9:
        livingRewardArray.append(livingReward)
        livingReward=livingReward-0.1'''
    while noise<0.2:
        noiseArray.append(0)
        discountArray.append(noise)
        noise=noise+0.1
    print(len(noiseArray),len(discountArray),len(livingRewardArray))
    while livingReward>=-0.2:
        livingRewardArray.append(livingReward)
        livingReward=livingReward-0.2
    count=0

    for discount in discountArray:
        for livingReward in livingRewardArray:
            for noise in noiseArray:
                totalReward=0
                distan=float('inf')
                mdp=getDiscountGrid()
                mdp.livingReward=livingReward
                mdp.noise=noise
                agent=ValueIterationAgent(mdp,discount,100)

                startstate=mdp.getStartState()
                policy=agent.getPolicy(startstate)
                #print(mdp.noise,mdp.livingReward)
                for numberOfSteps in range(25):
                    if mdp.isTerminal(startstate):
                        break;
                    action=agent.getAction(startstate)
                    transProb=mdp.getTransitionStatesAndProbs(startstate,action)
                    if not transProb:
                        break
                    nextState=transProb[0][0]
                    reward=mdp.getReward(startstate,action,nextState)
                    totalReward=totalReward+reward
                    startstate=nextState
                if distan>abs(totalReward-10):
                    answerNoise=noise
                    answerDiscount=discount
                    answerLivingReward=livingReward
                    distant=abs(totalReward-10)




                #print(policy)
                ## use the policy



                #allStates=mdp.getStates()
                '''for state in allStates:
                    agent.getPolicy(state)
                    print(agent.values)
                    #print(" count ",count,"discount:", discount, "noise:", noise, "livingReward:", livingReward, "policy:", policy)
                count=count+1'''

                #print(agent.runValueIteration())

                #print("discount:", discount, "noise:", noise, "livingReward:", livingReward, "policy:", policy)
                #print(startstate)

    # Return the best parameters found
    print("returned values",answerDiscount,answerNoise,answerLivingReward)
    return answerDiscount,answerNoise,answerLivingReward








    '''answerDiscount = -0.2
    answerNoise = 0
    answerLivingReward = -1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'''

def question2b():
    """
      Prefer the close exit (+1), but avoiding the cliff (-10).
    """
    answerNoise=0
    answerDiscount=0
    answerLivingReward=0
    discount=0
    livingReward=0
    noise=0

    noiseArray=[]
    discountArray=[]
    livingRewardArray=[]

    while discount<0.9:
        discountArray.append(discount)
        discount=discount+0.1
    while noise<=0:
        noiseArray.append(noise)
        noise=noise+0.1

    while livingReward<0.4:
        livingRewardArray.append(livingReward)
        livingReward=livingReward+0.1
    count=0

    for discount in discountArray:
        for livingReward in livingRewardArray:
            for noise in noiseArray:
                #print ("totalRewasssssssssssrd",totalReward)
                totalReward=0
                dist=float('-inf')
                mdp=getDiscountGrid()
                mdp.livingReward=livingReward
                mdp.noise=noise
                agent=ValueIterationAgent(mdp,discount,100)

                startstate=mdp.getStartState()
                policy=agent.getPolicy(startstate)
                #print(mdp.noise,mdp.livingReward)
                reward=0
                for numberOfSteps in range(10):
                    if mdp.isTerminal(startstate):
                        break;
                    action=agent.getAction(startstate)
                    transProb=mdp.getTransitionStatesAndProbs(startstate,action)
                    if not transProb:
                        break
                    nextState=transProb[0][0]
                    reward=mdp.getReward(startstate,action,nextState)*numberOfSteps
                    totalReward=totalReward+reward
                    startstate=nextState

                if reward==1 and totalReward> dist:
                    #print(reward,nextState)
                    dist=totalReward
                    answerDiscount=discount
                    answerLivingReward=livingReward







    print("returned values",answerDiscount,answerNoise,answerLivingReward)
    return answerDiscount, answerNoise, answerLivingReward
    #return 'NOT POSSIBLE'
    # If not possible, return 'NOT POSSIBLE'

def question2c():
    """
      Prefer the distant exit (+10), risking the cliff (-10).
    """
    answerDiscount = None
    answerNoise = None
    answerLivingReward = None
    #return answerDiscount, answerNoise, answerLivingReward
    return 'NOT POSSIBLE'

    # If not possible, return 'NOT POSSIBLE'

def question2d():
    """
      Prefer the distant exit (+10), avoiding the cliff (-10).
    """
    answerDiscount = None
    answerNoise = None
    answerLivingReward = None
    #return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'
    return 'NOT POSSIBLE'

def question2e():
    """
      Avoid both exits and the cliff (so an episode should never terminate).
    """
    answerDiscount = None
    answerNoise = None
    answerLivingReward = None
    #return answerDiscount, answerNoise, answerLivingReward
    return 'NOT POSSIBLE'
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    print('Answers to analysis questions:')
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print('  Question %s:\t%s' % (q, str(response)))
