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
import heapq #for priority queue

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
    
    """s = Directions.SOUTH
    w = Directions.WEST
    n = Directions.NORTH
    e = Directions.EAST"""


    visitedPos = []
    initialState = problem.getStartState()
    finalCardinal = []
    currentState = [initialState,0,0]
    
    def dfs(currentState):
        
        #check if we've found the goal state
        if problem.isGoalState(currentState[0]):
            visitedPos.append(currentState[0])
            finalCardinal.append(currentState[1])
            print("Goal reached: ", visitedPos)
            return visitedPos, finalCardinal

        #if not append visitedpositions array
        else:
            visitedPos.append(currentState[0])
            finalCardinal.append(currentState[1])
            Options = problem.getSuccessors(currentState[0])

            #check if we got to some kind of dead end ie only one option for movement (eg moving backwards)....
            if len(Options) == 1:
                print("Possible deadend reached...", "options: ", Options[0][1])

                #if there is only one option check to see if that option is the goal state eg. the goal is immediately next ot the start pos.
                if (problem.isGoalState(Options[0][0])):
                    visitedPos.append(Options[0][0])
                    print("Goal reached from deadend: ", visitedPos)
                    finalCardinal.append((Options[0][1]))
                    return visitedPos, finalCardinal

                #if there is only one option, ensure it isnt an already visited state. if it is not then go to it. eg a possible one way path??? B>D
                if Options[0][0] in visitedPos:
                    print(" already visited:", Options[0][0])

                else:
                    print("Going: ", Options[0])
                    temp = []
                    temp = dfs(Options[0])

                    if temp:
                        return temp
                #return
            
            for i in range (len(Options)): #iterate over each element in option
                print("OPtions: ",Options)

                for j in range(len(Options)):
                    if (problem.isGoalState(Options[j][0])) == (Options[j][0]):
                        visitedPos.append(Options[0][0])
                        print("Goal found in options: ", visitedPos)
                        finalCardinal.append((Options[0][1]))
                        return visitedPos, finalCardinal

                if Options[i][0] in visitedPos: #check if the available ith option has already been visited.
                    print(" already visited:", Options[i][0])
                    continue

                else:
                    print("Going: ", Options[i])
                    temp = []
                    temp = dfs(Options[i])
                    
                    #print("This is temp:", temp)
                    if temp:
                        return temp
            
            visitedPos.pop()
            finalCardinal.pop()

    dfs(currentState)
    return(finalCardinal[1:])

    util.raiseNotDefined()
    

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    def bfs():
        my_queue = []
        my_queue.append([((problem.getStartState()), ('None', 0))]) #append dummy vals to start position tuple. 
        #print(my_queue)
        visitedPos = []  #hold visited pos
        count = 0 #to track iterations/ tiers.

        while len(my_queue) > 0:
            count += 1
            print("\n", count)

            current = my_queue.pop(0)

            #print("my_queue after popping = ", my_queue)
            print("current = ", current[0][0])

            if current[0][0] in [pos[0] for pos in visitedPos]: #if the current node was alreadyu visited, then skip the turn.
                print("current val already visited", current[0][0])
                continue


            #check if the current state is our goal state
            if problem.isGoalState(current[0][0]):
                print("Goal found in parent")

                nested_tuple = current
                print(nested_tuple)
                inverted_path = []

                # Loop to extract each tuple
                while isinstance(nested_tuple, tuple):
                    inverted_path.append(
                        nested_tuple[0])  # Add the first element of the tuple
                    nested_tuple = nested_tuple[
                        1]  # Move to the next nested tuple

                #reverse the list to move from start to goal
                final_path = inverted_path[::-1]
                final_path = [tup[1] for tup in final_path]  #give me the second index of tuple.

                #print("final path = ", final_path)
                return final_path

            #if current[0] not in visitedPos:
            visitedPos.append(current[0])

            if count < 10:
                print("visitedPos = ", visitedPos)

            Options = problem.getSuccessors(current[0][0])
            print("Options = ", Options)

            for i in range(len(Options)):

                if Options[i][0] in [pos[0] for pos in visitedPos]:
                    print("already visited", Options[i][0])
                    continue

                else:

                    path = current
                    #print("Path", path)
                    print("enqueueing option: ", Options[i][0])

                    my_queue.append((Options[i], path))  #[i][0] = current, [i][2] = previous path, [i][1] = previous previous path

                    if problem.isGoalState(Options[i][0]):
                        print("Goal found in child")
                        #print("Full queue", my_queue)
                        #goal_found = True

                    #display a partial output...for debugging.....
                    if count<3:    
                        print("my_queue after = ", my_queue)


    #print("final_path:", bfs())

    return bfs()
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"


    def ucs():

        priority_queue = []
        visitedPos = {}
        parent = {}

        initialState = problem.getStartState()
        heapq.heappush(priority_queue, (0, initialState)) #push teh start state and the cost=0 to the queue for inititalizing
       # print(priority_queue)

        count = 0
        while priority_queue:
            count+=1
            print("\n", count)
            cost, currentState = heapq.heappop(priority_queue)
            print("Cost and current state:", cost, currentState)

            if problem.isGoalState(currentState):
                print("Goal Found!")
                #heapq.heappush(priority_queue,(new_cost, next_state))
                visitedPos[currentState] = cost
                #print("VisitedPos at goal:", visitedPos)
                print("queue at Goal:", priority_queue, "\n")


                goal = currentState
                path = []
                while goal != initialState:
                    prev_state, action = parent[goal]
                    path.append(action)  # Add the action to the path
                    goal = prev_state
                # Reverse the path since we backtracked
                path.reverse()

                # Output the path
                print("Path to the goal:", path)
                return path


            visitedPos[currentState] = cost

            Options = problem.getSuccessors(currentState)

            for next_state, action, step_cost in Options:
                
                print("next_state, action, step_cost:", next_state, action, step_cost)
               # print(next_state[0])
                new_cost = cost+step_cost


                if isinstance(next_state, tuple) and isinstance(next_state[0], tuple):
                    # Return the first element which is the coordinates (x, y)
                    next_state_for_comparision = next_state[0]
                    print("updated ns", next_state_for_comparision)
                # Otherwise, return the state itself assuming it's already in the form (x, y)
                else:
                    next_state_for_comparision = next_state


                
                if count >9 and count <12:
                    print("cnt 11: ", next_state, visitedPos, new_cost)


                if (next_state_for_comparision not in visitedPos) or (new_cost < visitedPos[next_state_for_comparision]):
                    #heapq.heappush(priority_queue,(new_cost, next_state_for_comparision))
                    #parent[next_state_for_comparision] = (currentState, action)  # Store the parent state and action
                    heapq.heappush(priority_queue, (new_cost, next_state))
                    visitedPos[next_state_for_comparision] = new_cost
                    parent[next_state_for_comparision] = (currentState, action)

        print("no goal found?")
        return ["West","East","East", "South", "South", "West", "West"]  #for debuggging
        
    return (ucs())
    #util.raiseNotDefined()

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
