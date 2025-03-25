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
    # Initialize the stack with the start state
    stack = [(problem.getStartState(), [])]
    visited = set()
    while stack:
        state, path = stack.pop()
        # Check if the state has been visited
        if state in visited:
            continue
        # Mark the state as visited
        visited.add(state)
        # Check if the current state is the goal
        if problem.isGoalState(state):
            return path
        # Get successors and add them to the stack
        for successor, action, step_cost in problem.getSuccessors(state):            
            new_path = path + [action]
            stack.append((successor, new_path))
    return []

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from collections import deque
    # Initialize the queue with the start state and an empty path
    queue = deque([(problem.getStartState(), [])])
    visited = set()

    while queue:
        state, path = queue.popleft()
        print("Current state:", state)
        print("Current path:", path)

        # Check if the state has been visited
        if state in visited:
            continue

        # Mark the state as visited
        visited.add(state)

        # Check if the current state is the goal state
        if problem.isGoalState(state):
            print("Goal found:", state)
            return path

        # Get successors of the current state
        successors = problem.getSuccessors(state)
        print("Successors of", state, ":", successors)

        # Add successors to the queue
        for successor, action, cost in successors:
            new_path = path + [action]
            queue.append((successor, new_path))

    return []
import heapq
def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
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
import heapq
def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
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
