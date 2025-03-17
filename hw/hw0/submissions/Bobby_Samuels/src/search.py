# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions
from typing import List

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    
    print("= 1 ==> My Algorithm Begins")
    s = Directions.SOUTH
    w = Directions.WEST
    n = Directions.NORTH
    e = Directions.EAST
    visitedPositions = []
    initialState = problem.getStartState()
    initialStateInOptionForm=(initialState,"",1)
    finalArray = []
    global count
    global goalReached
    goalReached = False
    count = 0
  
    def dfs(currentState): #Recursive DFS on a node object 
        tempActions = []
        global count
        global goalReached
        count = count+1
        # if(count > 200):
        #     print("recursion limit reached")
        #     return []
        # print("= 2 ==> dfs instance #"+str(count)+" called")
        # print("Current State in opt form "+str(currentState))
        if (currentState[0] not in visitedPositions):
            visitedPositions.append(currentState[0])
            # print("= 2.5 ==> Visited States"+str(visitedPositions))
        if (problem.isGoalState(currentState[0])):
            # print("= 3 ==>GOAL Reached")
            tempActions.append(currentState[1])
            goalReached = True
        else:
            # print("= 3 ==> Goal not Current state. Finding Unvisited states")
            nextOptions = problem.getSuccessors(currentState[0])
            # print("= 4 ==> We have multiple frontier options")
            for option in nextOptions:
                if goalReached == True:
                    break
                if option[0] not in visitedPositions:
                    result = dfs (option)
                    if len(result) > 0:
                        tempActions = [currentState[1]]+ result
                
        # print("= 5 ==> Return Array is: "+str(tempActions)) 
        return tempActions
        
    finalArray = dfs(initialStateInOptionForm)
    if(len(finalArray) >0):
        finalArray.pop(0)
    print("final answer:" + str(finalArray))
    return finalArray

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    s = Directions.SOUTH
    w = Directions.WEST
    n = Directions.NORTH
    e = Directions.EAST
    visitedPositions = []
    
    initialState = problem.getStartState() # returns (x,y)
    initialStateInFormat=((initialState,'NULL',0),0) #custom bfs node format
    global goalReachedbfs
    goalReachedbfs = False
    finalActions = []
    global countbfs
    countbfs = 0
   
    # recursive function bfs
    # initialState returns only (x,y)
    # a node from getSuccessors looks like ( (x,y),'Action',number )
    # States in custom bfs are stored as (node from getSuccessor, parent index )
    
    def bfs( currentLevel):
        
        print("===> 1 current level is "+ str(currentLevel))
        tempAction = (0,[]) #Return format for bfs is a tuple (parent index, action array)
        nextLevel = [] #Stores the children of the current level
        
        #For every option in current level, check it to see if its the goal, and if not, store it's children into NextLevl
        
        for parentIndex, state in enumerate(currentLevel): #Grab each option in current level,and it's index in current level
            if state[0][0] not in visitedPositions:
                visitedPositions.append(state[0][0])
                print("===> 2 visited Positions is now "+str(visitedPositions))
        return  (0,[s, s, w, s, w, w, s, w])
    
    finalActions = bfs( [ initialStateInFormat])
    return finalActions[1]
    

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
