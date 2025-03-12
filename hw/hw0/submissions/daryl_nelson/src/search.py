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
    visited_states = set()
    actions = [(problem.getStartState(), [])]

    while actions:
        current_state, path = actions.pop()

        if problem.isGoalState(current_state):
            return path

        if current_state not in visited_states:
            visited_states.add(current_state)

        for successor, action, stepCost in problem.getSuccessors(current_state):
            if successor not in visited_states:
                new_path = path + [action]
                actions.append((successor, new_path))

    return []

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    queue = [(problem.getStartState(), [])]
    visited = set()

    while queue:
        state, path = queue.pop(0)

        if problem.isGoalState(state):
            return path

        if state not in visited:
            visited.add(state)

            for successor, action, stepCost in problem.getSuccessors(state):
                queue.append((successor, path + [action]))

    return []

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    queue = [(problem.getStartState(), [])]
    visited = set()

    while queue:
        print(queue)
        current_state, path = queue.pop(0)

        if problem.isGoalState(current_state):
            return path

        if current_state not in visited:
            visited.add(current_state)

            secondary_queue = problem.getSuccessors(current_state)


            for x in range(1, len(secondary_queue)):
                array_value = secondary_queue[x][2]
                array_key = secondary_queue[x]
                j = x - 1

                while j >= 0 and secondary_queue[j][2] > array_value:
                    secondary_queue[j + 1] = secondary_queue[j]
                    j -= 1

                secondary_queue[j + 1] = array_key

            print(secondary_queue)
            queue = secondary_queue + queue

            print(queue)
            exit()









    # while actions:
    #     print(actions)
    #     current_state, path = actions.pop()
    #     cheapest_node = []
    #
    #     if problem.isGoalState(current_state):
    #         return path
    #
    #     if current_state not in visited_states:
    #         visited_states.add(current_state)
    #
    #
    #     for successor, action, stepCost in problem.getSuccessors(current_state):
    #
    #         if not cheapest_node or stepCost < cheapest_node[2] and successor not in visited_states:
    #            cheapest_node = [successor, action, stepCost]
    #
    #     if cheapest_node:
    #         new_path = path + [cheapest_node[1]]
    #         actions.append((cheapest_node[0], new_path))
    #     else:
    #         actions.append((current_state, path))
    #
    #     print(cheapest_node)
    #     print(new_path)
    #     print(actions)
    #     count += 1
    #     if count > 2:
    #         exit()
    #
    #
    #
    # return []




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
