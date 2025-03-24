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
    #create stack to store postions
    #check to see if the node was already passed
    #the path packman takes to eat items. 
    
    """Search the deepest nodes in the search tree first."""

    '''This function pushes non-visited nodes onto the stack.
    Nodes are popped one by one, and the following steps are performed:
    1. The node is marked as visited.
    2. If it is a goal node, the loop stops, and the solution is obtained by backtracking using stored parents.
    3. If it is not a goal node, it is expanded.
    4. If the successor node is not visited, then it is pushed onto the stack and its parent is stored.'''

    # initializations

    # "visited" contains nodes which have been popped from the stack,
    # and the direction from which they were obtained
      # "visited" contains nodes which have been popped from the stack,
    # and the direction from which they were obtained
    # state whether  cell has been visited or not
    #search tree, holds parent, direction  drom parent, state 
    
    visited = {}
    # "solution" contains the sequence of directions for Pacman to get to the goal state
    solution = []
    # "stack" contains triplets of: (node in the fringe list, direction, cost)
    stack = []
    parents={}
    lastPosition=(0,0)
    
    #getStartState returns pacmanStart psition 
    StartPosition=problem.getStartState()
    stack.append([StartPosition,'home',0])
    
    goal=False
    count=0;
    if problem.isGoalState(StartPosition):
        return solution
        
    while stack and goal !=True:
        currentNode=stack.pop()
        visited[currentNode[0]]=currentNode[1]
        if problem.isGoalState(currentNode[0]):
            lastPosition=currentNode[0]
            goal=True
            break
        #list of three elements
        #get all children(Postition(x,y)
        #Direction to get to each child
        #cost to get to each chile 
        for child in problem.getSuccessors(currentNode[0]):
            if child[0] not in visited.keys():
                parents[child[0]]=currentNode[0]
                stack.append(child)
    while lastPosition in parents.keys():
        lastPosition_parent=parents[lastPosition]
        solution.insert(0,visited[lastPosition])
        #Last Position Becomes newParentNode 
        lastPosition=lastPosition_parent
    
    return solution    
    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
      
    visited = {}
    # "solution" contains the sequence of directions for Pacman to get to the goal position
    solution = []
    # "stack" contains triplets of: (node in the fringe list, direction, cost)
    queue = []
    parents={}
    lastPosition=(0,0)
    
    #getStartState returns pacmanStart psition 
    StartPosition=problem.getStartState()
    queue.append([StartPosition,'home',0])
    goal=False
    
    if problem.isGoalState(StartPosition):
        return solution
    while goal!=True and queue:
        #remove first element from queue as we are doing a breat first search
        currentPosition=queue.pop(0)
        #mark node as visited 
        visited[currentPosition[0]]=currentPosition[1]
        if problem.isGoalState(currentPosition[0]):
            #set goal to true to exit loop as we found a solution
            goal=True
            
            lastPosition=currentPosition[0]
            break
        
        for child in problem.getSuccessors(currentPosition[0]):
            if child[0] not in visited.keys()and child[0] not in parents.keys():
               queue.append(child)
               parents[child[0]]=currentPosition[0]
    
    while lastPosition in parents:
         lastPosition_parent=parents[lastPosition]
         solution.insert(0,visited[lastPosition])
         lastPosition=lastPosition_parent
   
        
  
    return solution
    util.raiseNotDefined()
  
def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
   
    visited = {}
    # "solution" contains the sequence of directions for Pacman to get to the goal state
    solution = []
    # "queue" contains triplets of: (nodes in the fringe list, direction, cost)
    queue = util.PriorityQueue()
    # "parents" contains nodes and their parents
    parents = {}
    # "cost" contains nodes and their corresponding costs
    cost = {}

    # start state is obtained and added to the queue
    start = problem.getStartState()
    queue.push((start, 'Home', 0), 0)
    
    
    # cost of start state is 0
    cost[start] = 0
    lastPosition=(0,0)
    goal = False;
    while queue and goal != True:
        # expolre the top of the queue
        currentlocation = queue.pop()
        # set the direction to get to node
        visited[currentlocation[0]] = currentlocation[1]
        # check if by reacahing this location it reaches a goal state
        if problem.isGoalState(currentlocation[0]):
            lastPosition = currentlocation[0]
            goal = True
            break
        # expand node
        for child in problem.getSuccessors(currentlocation[0]):
            # if successor is not visited, calculate its new cost
            if child[0] not in visited.keys():
                costToChild = currentlocation[2] + child[2]
                # if the child in queue but has not been expanded as  check if the new routecost is less the the current routecost
                #cost it is less than leave it bee proceed to next child
                if child[0] in cost.keys():
                    if cost[child[0]] <= costToChild:
                        continue
                #proceed to update que if the  costToChild is less than cost in queue
                #child,direction,costtochild
                queue.push((child[0], child[1], costToChild), costToChild)
                #update cost if its less tha prvious cost  or set queue is its new location
                cost[child[0]] = costToChild
                # set parent of child as current locaiton
                parents[child[0]] = currentlocation[0]

    # finding and storing the path
    while lastPosition in parents.keys():
        # find parent
        lastPosition_parent = parents[lastPosition]
        # prepend direction to solution
        solution.insert(0, visited[lastPosition])
        # go to previous node
        lastPosition = lastPosition_parent

    return solution

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
