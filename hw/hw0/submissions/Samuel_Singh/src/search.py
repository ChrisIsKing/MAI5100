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

        priority_queue = []  # Priority queue (list)
        visited = {}

        initialState = problem.getStartState()
        priority_queue.append((0, [], initialState))  # (cost, path, state) 
        print("initial queue:", priority_queue)

        count = 0

        while priority_queue:
            count+=1
            print("\n", count)

            priority_queue.sort()  # Sort queue by cost (low-cost first)

            print("Sorted queue at start:", priority_queue)

            cost, path, currentState = priority_queue.pop(0)  # Pop the lowest-cost node

            print("Current: ", currentState)

            if currentState in visited:
                print("already visited current")
                continue
            
            #visited.add(currentState)
            visited[currentState] = cost
            print("Visited: ", visited)

            if problem.isGoalState(currentState):
                print("Goal Found: ", path)
                return path  # Return the solution

            Options = problem.getSuccessors(currentState)
            print("Options:", Options)

            for next_state, action, step_cost in Options:

                if next_state not in visited:
                    new_cost = cost + step_cost
                    priority_queue.append((new_cost, path + [action], next_state))  # Add the path cpst and next state to the queue
            
            if count < 5:
                print("Queue at end of iteration:", priority_queue)
        
    return (ucs())
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:


    def astar():

        priority_queue = []  # Priority queue (list)
        visitedPos = {}  # Dictionary to track lowest cost to each noed

        initialState = problem.getStartState()
        manhattan = heuristic(initialState, problem)
        priority_queue.append((0 + manhattan, 0, [], initialState))  
        # (f(n) = g(n) + h(n), g(n), path, state)

        print("Initial queue", priority_queue)

        count = 0
        
        while priority_queue:
            count +=1
            print("\n", count)

            priority_queue.sort()  # Sort queue by first index (lowest val at start of queue
        
            if count <5:
                print("Sorted queue at start:", priority_queue)
           
            f_value, cost, path, currentState = priority_queue.pop(0)  # Pop the current val out. 

            print("Current", currentState)

            if currentState in visitedPos and visitedPos[currentState] <= cost:
                print("Current state already visited or lower cost path already explored.")
                continue  
            
            visitedPos[currentState] = cost  # Add the current state and teh cost to VisitedPos
            print("VisitedPOS current state", visitedPos, visitedPos[currentState])

            if problem.isGoalState(currentState):
                return path  # Return the solution

            Options = problem.getSuccessors(currentState)
            print("Options:", Options)

            for next_state, action, step_cost in Options:
                new_cost = cost + step_cost
                manhattan = heuristic(next_state, problem)
                f_value = new_cost + manhattan  # f(n) = g(n) + h(n)
                print("State", next_state," Cost:", cost, " step_cost", step_cost, " manhattan:", manhattan, " total cost:", f_value)
                priority_queue.append((f_value, new_cost, path + [action], next_state))  # append queue

            if count <5:
                print("Queue at end of iter:", priority_queue)

    return astar()
    #return ["West"] #debugging


    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
