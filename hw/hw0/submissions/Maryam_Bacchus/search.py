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
    # s = Directions.SOUTH
    # w = Directions.WEST
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

    explored_nodes = []
    stack = []
 
    if problem.isGoalState(problem.getStartState()):
        return []

    stack.append((problem.getStartState(), []))

    while stack:
        (node, direction) = stack.pop(-1)
        if node in explored_nodes:
            continue
        explored_nodes.append(node)

        if problem.isGoalState(node):
            return direction

        for successor_node, successor_direction, cost in problem.getSuccessors(node):
            if successor_node not in explored_nodes:
                new_path = direction + [successor_direction]
                stack.append((successor_node, new_path)) 
    return 0

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    explored_nodes = []
    stack = []

    if problem.isGoalState(problem.getStartState()):
        return []

    stack.append((problem.getStartState(), []))

    while stack:
        (node, direction) = stack.pop(0)

        if node in explored_nodes:
            continue
        explored_nodes.append(node)

        if problem.isGoalState(node):
            return direction

        for successor_node, successor_direction, cost in problem.getSuccessors(node):
            if successor_node not in explored_nodes:
                new_path = direction + [successor_direction]
                stack.append((successor_node, new_path))

    return []

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    explored_nodes = []
    stack = []
    
    if problem.isGoalState(problem.getStartState()):
        return []

    stack.append((problem.getStartState(), [], 0))

    while stack:
        stack.sort(key=lambda node_obj: node_obj[2])
        (node, direction, cost) = stack.pop(0)
        
        if node in explored_nodes:
            continue
        explored_nodes.append(node)

        if problem.isGoalState(node):
           return direction

        for successor_node, successor_direction, successor_cost in problem.getSuccessors(node):
            if successor_node not in explored_nodes:
                new_path = direction + [successor_direction]
                new_cost = cost + successor_cost
                stack.append((successor_node, new_path, new_cost))

    return []

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """

    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    explored_nodes = []
    queue = util.PriorityQueue()
    best_path = {}

    if problem.isGoalState(problem.getStartState()):
        return []

    queue.push((problem.getStartState(), [], 0), 0 + heuristic(problem.getStartState(), problem))
    best_path[(str(problem.getStartState()))] = 0

    while not queue.isEmpty():
        (node, direction, cost) = queue.pop()        
        node_str = str(node)
        if problem.isGoalState(node):
            return direction

        for successor_node, successor_direction, successor_cost in problem.getSuccessors(node):
            new_cost = cost + successor_cost
            successor_node_str = str(successor_node)
            if successor_node_str not in best_path or new_cost < best_path[successor_node_str]:
                new_path = direction + [successor_direction]
                best_path[successor_node_str] = new_cost
                priority = new_cost + heuristic(successor_node, problem)
                queue.push((successor_node, new_path, new_cost), priority)
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
