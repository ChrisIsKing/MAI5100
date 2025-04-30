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
        newFood = successorGameState.getFood().asList()
        oldFood = currentGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        score = 0
        
        if newFood:
            closestFoodDist = min([manhattanDistance(newPos, food) for food in newFood])
            score += (100 / (closestFoodDist + 1))
            
        if len(newFood) < len(oldFood):
            score += 50

        for ghost in newGhostStates:
            ghostPos = ghost.getPosition()
            distance = manhattanDistance(newPos, ghostPos)
            if distance < 2 and ghost.scaredTimer == 0:
                score -= 200 
            elif ghost.scaredTimer > 0:
                score += (50 / (distance + 1))  
       
        if action == Directions.STOP:
            score -= 100
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
        legal_actions = gameState.getLegalActions(0)
        best_score = float('-inf')
        best_action = None

        if not legal_actions:
            return Directions.STOP
        
        for action in legal_actions:
            successor = gameState.generateSuccessor(0, action)
            score = self.min_agent(successor, self.depth, 1)
            
            if score > best_score:
                best_score = score
                best_action = action
                
        return best_action
    
    def max_agent(self, gameState, depth):

        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)

        legal_actions = gameState.getLegalActions(0)
        max_score = float('-inf')

        for action in legal_actions:
            successor = gameState.generateSuccessor(0, action)
            score = self.min_agent(successor, depth, 1)
            max_score = max(max_score, score)
    
        return max_score
    
    def min_agent(self, gameState, depth, ghost_index):

        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
        
        min_score = float('inf')
        legal_actions = gameState.getLegalActions(ghost_index)

        for action in legal_actions:
            successor = gameState.generateSuccessor(ghost_index, action)
            if ghost_index == gameState.getNumAgents() - 1:
                score = self.max_agent(successor, depth - 1)
            else:
                score = self.min_agent(successor, depth, ghost_index + 1)
                
            min_score = min(min_score, score)
                    
        return min_score


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        legal_actions = gameState.getLegalActions(0)
        best_score = float('-inf')
        best_action = None
        alpha = float('-inf')
        beta = float('inf')

        if not legal_actions:
            return Directions.STOP
        
        for action in legal_actions:
            successor = gameState.generateSuccessor(0, action)
            score = self.min_agent(successor, self.depth, 1, alpha, beta)
            
            if score > best_score:
                best_score = score
                best_action = action
            
            alpha = max(alpha, best_score)
                
        return best_action
    
    def max_agent(self, gameState, depth, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)

        legal_actions = gameState.getLegalActions(0)
        max_score = float('-inf')

        for action in legal_actions:
            successor = gameState.generateSuccessor(0, action)
            score = self.min_agent(successor, depth, 1, alpha, beta)
            max_score = max(max_score, score)
            
            if max_score > beta:
                return max_score
        
            alpha = max(alpha, max_score)

        return max_score
    
    def min_agent(self, gameState, depth, ghost_index, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
        
        min_score = float('inf')
        legal_actions = gameState.getLegalActions(ghost_index)

        for action in legal_actions:
            successor = gameState.generateSuccessor(ghost_index, action)

            if ghost_index == gameState.getNumAgents() - 1:
                score = self.max_agent(successor, depth - 1, alpha, beta)
            else:
                score = self.min_agent(successor, depth, ghost_index + 1, alpha, beta)
                
            min_score = min(min_score, score)

            if min_score < alpha:
                return min_score
            
            beta = min(beta, min_score)
            
        return min_score

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
        legal_actions = gameState.getLegalActions(0)
        best_score = float('-inf')
        best_action = None

        if not legal_actions:
            return Directions.STOP
        
        for action in legal_actions:
            successor = gameState.generateSuccessor(0, action)
            score = self.exp_agent(successor, self.depth, 1)
            
            if score > best_score:
                best_score = score
                best_action = action
                
        return best_action
    
    def max_agent(self, gameState, depth):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)

        legal_actions = gameState.getLegalActions(0)
        max_score = float('-inf')

        for action in legal_actions:
            successor = gameState.generateSuccessor(0, action)
            score = self.exp_agent(successor, depth, 1)
            max_score = max(max_score, score)
    
        return max_score
    
    def exp_agent(self, gameState, depth, ghost_index):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
        
        legal_actions = gameState.getLegalActions(ghost_index)
        total_score = 0
        num_actions = len(legal_actions)

        for action in legal_actions:
            successor = gameState.generateSuccessor(ghost_index, action)
            if ghost_index == gameState.getNumAgents() - 1:
                score = self.max_agent(successor, depth - 1)
            else:
                score = self.exp_agent(successor, depth, ghost_index + 1)
            total_score += score / num_actions

        return total_score

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isWin(): 
        return float("inf")

    if currentGameState.isLose(): 
        return float("-inf")
    
    pacman_position = currentGameState.getPacmanPosition()
    food_list = currentGameState.getFood().asList()
    ghosts = currentGameState.getGhostStates()
    power_capsules = currentGameState.getCapsules()
    score = currentGameState.getScore()

    if food_list:
        closest_food = min(manhattanDistance(pacman_position, food) for food in food_list)
        score += 10.0 / (closest_food + 1)
    
    if power_capsules:
        closest_capsule = min(manhattanDistance(pacman_position, capsule) for capsule in power_capsules)
        score += 20.0 / (closest_capsule + 1)
    
    for ghost in ghosts:
        ghost_distance = manhattanDistance(pacman_position, ghost.getPosition())
        if ghost.scaredTimer > 0:
            score += 100.0 / (ghost_distance + 1)
        else:
            if ghost_distance < 3:
                score -= 200.0 / (ghost_distance + 1)
    return score

# Abbreviation
better = betterEvaluationFunction
