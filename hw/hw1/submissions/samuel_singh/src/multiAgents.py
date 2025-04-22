# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood() #this is an tuple of all food pos. 
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        """
        Initialize score as the base score from the successor game state

        Convert the new food grid into a list of coordinates

        If the food list is not empty:
            For each food item in the list:
                Compute Manhattan distance from Pacman to the food
                Store this distance in a list called foodDistances
        
            Get the minimum food distance from foodDistances
            Increase score by (10.0 / minFoodDist) to prioritize closer food

        For each ghost in the list of new ghost states:
            Get corresponding scared time
            Compute Manhattan distance from Pacman to the ghost

            If the ghost is not scared (scaredTime == 0):
                If the ghost is within a distance of 2:
                    Subtract 500 from score to penalize being too close
            Else (ghost is scared):
                Add (2.0 / ghostDist) to the score to slightly encourage approaching scared ghosts

        If the number of food items has decreased (i.e., food was eaten):
            Add 20 to the score

        Return the final score
        """


        print("newPos", newPos)
        # print("newFood", newFood)
        print("newGhostStates", newGhostStates)
        print("newScaredTimes", newScaredTimes)

        #return successorGameState.getScore() default

        score = successorGameState.getScore()

        
        foodList = newFood.asList()
        print("food list", foodList)
        
        if foodList: #while there is some food on the map
            for food in foodList: #check the list of food
                foodDistances = [manhattanDistance(newPos, food)]
                print("food Distance", foodDistances)

                minFoodDist = min(foodDistances)
                score += 10.0 /minFoodDist #give higher weight for food priority.


        for i in range(len(newGhostStates)):
            ghost = newGhostStates[i]
            scaredTime = newScaredTimes[i]
            ghostDist = manhattanDistance(newPos, ghost.getPosition())
            
            if scaredTime == 0:
                if ghostDist <= 2:
                    score -= 500  # penalize getting too close
            else:
                score += 2.0 / ghostDist  # approach scared ghosts slightly

        if currentGameState.getNumFood() > successorGameState.getNumFood():
            score += 20
        
        return score


def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """


    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        """
        Check if the game is over or we've reached the maximum search depth:
        
        If Pacman has won, lost, or reached the allowed depth,
         Return the evaluation score of the current state.
        
        Get the total number of agents in the game.
        (Pacman is always agent 0; ghosts follow.)
        If it's Pacman turn (agentIndex = 0):
            Initialize the best score to negative infinity (since Pacman wants to maximize the score).
        
        For each legal action Pacman can take:
            Generate the resulting game state after that move.
            Recursively call minimax for the first ghost's turn with the new state.
             Keep track of the highest score Pacman can achieve from all possible moves.
        
        Return the best score found.
        
        If its a ghosts turn (agentIndex > 0):
            Determine the next agent (the next ghost or Pacman again).
        
        If wee at the last ghost, start a new turn and increase the depth.
        
        Initialize the best score to positive infinity (since ghosts want to minimize Pacman's score).
        
        For each legal action the ghost can take:
            Generate the resulting game state after that move.
            Recursively call minimax for the next agent.
            Keep track of the lowest score the ghosts can force Pacman into.
        
        Return the lowest score found.

        At the very beginning of the game (root level):
        Initialize the best action as nothing yet.
        Set the best score to negative infinity.
        For each possible move Pacman can make:
        Generate the next game state after that move.
        Use the minimax function to simulate what the ghosts would do in response.
        If this move results in a better score than previous moves: Update the best score and remember the best action.
        After checking all moves, return the move that gave the best score.

        """




        def minimax(agentIndex, depth, state):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            numAgents = state.getNumAgents()

            if agentIndex == 0:  # Pacman's turn (maximize)
                bestScore = float('-inf')
                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)
                    score = minimax(1, depth, successor)
                    bestScore = max(bestScore, score)
                return bestScore

            else:  # Ghost's turn (minimize)
                nextAgent = agentIndex + 1
                if nextAgent == numAgents:
                    nextAgent = 0
                    depth += 1
                bestScore = float('inf')
                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)
                    score = minimax(nextAgent, depth, successor)
                    bestScore = min(bestScore, score)
                return bestScore

        # Root call: find best action for Pacman
        bestAction = None
        bestScore = float('-inf')
        for action in gameState.getLegalActions(0):  # Pacman's legal moves
            successor = gameState.generateSuccessor(0, action)
            score = minimax(1, 0, successor)
            if score > bestScore:
                bestScore = score
                bestAction = action

        return bestAction

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        """

        Initial Call:
        Set the best action to None
        Initialize alpha to negative infinity and beta to positive infinity
        Set the best score to negative infinity
        For each legal action Pacman can take from the current state:
            Simulate the game state after taking the action
            Run alphabeta for the first ghost starting at depth 0
            If the returned score is better than the best score seen so far:
            Update the best score
            Set this action as the best action
            Update alpha to be the maximum of itself and the current score
        Return the best action Pacman should take



        Define alphabeta(agentIndex, depth, state, alpha, beta):
        
        If the state is a win, a loss, or weve reached the maximum search depth:
            Return the evaluation of the state
        
        Set the total number of agents in the game
        
        If the agent is Pacman (maximizing player):
            Set the current best value to negative infinity
        
        For each legal action Pacman can take:
            Simulate the game state after that action
            Recursively call alphabeta for the first ghost
            Update the best value to be the maximum between the current value and the result of the recursive call
        
        If this best value is greater than beta:
            Return the value immediately (beta cutoff)
        
        Update alpha to be the maximum of itself and the current value
        
        Return the best value found
        
        Else (if the agent is a ghost - minimizing player):
            Determine who the next agent is
        
        If this ghost is the last agent:
            Set the next agent to Pacman and increase the search depth
        
        Set the current best value to positive infinity
        
        For each legal action the ghost can take:
            Simulate the game state after that action
            Recursively call alphabeta for the next agent
            Update the best value to be the minimum between the current value and the result of the recursive call
            If this best value is less than alpha:
                Return the value immediately (alpha cutoff)
                Update beta to be the minimum of itself and the current value
        Return the best value found


        """



        def alphabeta(agentIndex, depth, state, alpha, beta):
            # Terminal state check
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            numAgents = state.getNumAgents()

            if agentIndex == 0:  # Pacman (Max)
                value = float('-inf')
                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)
                    value = max(value, alphabeta(1, depth, successor, alpha, beta))
                    if value > beta:
                        return value  # Beta cutoff
                    alpha = max(alpha, value)
                return value

            else:  # Ghosts (Min)
                nextAgent = agentIndex + 1
                nextDepth = depth
                if nextAgent == numAgents:
                    nextAgent = 0
                    nextDepth += 1

                value = float('inf')
                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)
                    value = min(value, alphabeta(nextAgent, nextDepth, successor, alpha, beta))
                    if value < alpha:
                        return value  # Alpha cutoff
                    beta = min(beta, value)
                return value

        # Initial call: Pacman chooses the best move
        bestAction = None
        alpha = float('-inf')
        beta = float('inf')
        bestScore = float('-inf')

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            score = alphabeta(1, 0, successor, alpha, beta)
            if score > bestScore:
                bestScore = score
                bestAction = action
            alpha = max(alpha, score)

        return bestAction


        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
