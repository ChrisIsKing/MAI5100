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
    """
    # Stack for DFS frontier - stores (state, actions) pairs
    # where actions is the path to reach the state
    frontier = util.Stack()
    
    # Initialize with the start state and empty action list
    startState = problem.getStartState()
    frontier.push((startState, []))
    
    # Set to keep track of visited states (for graph search)
    visited = set()
    
    while not frontier.isEmpty():
        # Get the current state and actions to reach it
        currentState, actions = frontier.pop()
        
        # Check if we've reached the goal
        if problem.isGoalState(currentState):
            return actions
        
        # Skip if we've already visited this state
        if currentState in visited:
            continue
        
        # Mark current state as visited
        visited.add(currentState)
        
        # Explore successors (DFS)
        for successor, action, stepCost in problem.getSuccessors(currentState):
            if successor not in visited:
                # Create new action sequence by adding the new action
                newActions = actions + [action]
                frontier.push((successor, newActions))
    
    # If no solution is found
    return []

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the shallowest nodes in the search tree first.
    
    BFS guarantees the shortest path in unweighted graphs or 
    graphs where all edges have the same cost.
    """
    # Queue for BFS frontier - stores (state, actions) pairs
    frontier = util.Queue()
    
    # Initialize with the start state and empty action list
    startState = problem.getStartState()
    frontier.push((startState, []))
    
    # Set to keep track of visited states (for graph search)
    # For BFS, we need to mark states as visited when we *enqueue* them,
    # not when we dequeue them, to avoid redundant paths to the same state
    visited = set([startState])
    
    while not frontier.isEmpty():
        # Get the current state and actions to reach it
        currentState, actions = frontier.pop()
        
        # Check if we've reached the goal
        if problem.isGoalState(currentState):
            return actions
        
        # Explore successors (breadth-first)
        for successor, action, stepCost in problem.getSuccessors(currentState):
            if successor not in visited:
                # Mark successor as visited immediately to avoid duplicates in the queue
                visited.add(successor)
                
                # Create new action sequence by adding the new action
                newActions = actions + [action]
                frontier.push((successor, newActions))
    
    # If no solution is found
    return []

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the node of least total cost first.
    
    UCS guarantees the shortest path in terms of total path cost,
    which makes it optimal even for graphs with varying edge costs.
    """
    # PriorityQueue for UCS frontier - stores (state, actions, totalCost) tuples
    # Priority is determined by the totalCost
    frontier = util.PriorityQueue()
    
    # Initialize with the start state, empty action list, and zero cost
    startState = problem.getStartState()
    frontier.push((startState, [], 0), 0)  # (state, actions, cost), priority=cost
    
    # Dictionary to keep track of visited states and their lowest costs
    # Using a dict instead of a set allows us to update if we find a lower cost path
    visited = {}  # state -> lowest cost seen so far
    
    while not frontier.isEmpty():
        # Get the current state, actions to reach it, and total cost
        currentState, actions, currentCost = frontier.pop()
        
        # Check if we've reached the goal
        if problem.isGoalState(currentState):
            return actions
        
        # Skip if we've already visited this state with a lower cost
        if currentState in visited and visited[currentState] < currentCost:
            continue
        
        # Mark current state as visited with its cost
        visited[currentState] = currentCost
        
        # Explore successors (lowest cost first)
        for successor, action, stepCost in problem.getSuccessors(currentState):
            # Calculate the total cost to reach the successor
            newCost = currentCost + stepCost
            
            # Only consider if we haven't visited or found a lower cost path
            if successor not in visited or newCost < visited[successor]:
                # Create new action sequence by adding the new action
                newActions = actions + [action]
                frontier.push((successor, newActions, newCost), newCost)
    
    # If no solution is found
    return []

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """
    Search the node that has the lowest combined cost and heuristic first.
    
    A* search combines the actual path cost g(n) with a heuristic estimate h(n)
    of the cost to reach the goal, using f(n) = g(n) + h(n) as the priority.
    If h(n) is admissible (never overestimates), A* is optimal.
    """
    # PriorityQueue for A* frontier - stores (state, actions, g_cost) tuples
    # Priority is determined by f(n) = g(n) + h(n)
    frontier = util.PriorityQueue()
    
    # Initialize with the start state, empty action list, and zero g_cost
    startState = problem.getStartState()
    # Calculate initial f(n) = g(n) + h(n), where g(n) = 0 for start state
    startHeuristic = heuristic(startState, problem)
    frontier.push((startState, [], 0), 0 + startHeuristic)  # (state, actions, g_cost), priority=f_cost
    
    # Dictionary to keep track of visited states and their lowest g_costs
    visited = {}  # state -> lowest g_cost seen so far
    
    while not frontier.isEmpty():
        # Get the current state, actions to reach it, and g_cost (cost so far)
        currentState, actions, g_cost = frontier.pop()
        
        # Check if we've reached the goal
        if problem.isGoalState(currentState):
            return actions
        
        # Skip if we've already visited this state with a lower g_cost
        if currentState in visited and visited[currentState] < g_cost:
            continue
        
        # Mark current state as visited with its g_cost
        visited[currentState] = g_cost
        
        # Explore successors
        for successor, action, stepCost in problem.getSuccessors(currentState):
            # Calculate the g(n) to reach the successor (cost so far)
            new_g_cost = g_cost + stepCost
            
            # Only consider if we haven't visited or found a lower g_cost path
            if successor not in visited or new_g_cost < visited[successor]:
                # Create new action sequence by adding the new action
                newActions = actions + [action]
                
                # Calculate f(n) = g(n) + h(n)
                h_cost = heuristic(successor, problem)  # Heuristic estimate to goal
                f_cost = new_g_cost + h_cost
                
                frontier.push((successor, newActions, new_g_cost), f_cost)
    
    # If no solution is found
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
