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
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # Initialize score
        score = successorGameState.getScore()
        
        # Food evaluation
        foodList = newFood.asList()
        if foodList:
            foodDistances = [manhattanDistance(newPos, food) for food in foodList]
            closestFoodDist = min(foodDistances)
            score += 1.0 / (closestFoodDist + 1)  # Reward being close to food
            
            # Consider clustering of food - reward states that lead to areas with multiple food pellets
            if len(foodList) > 1:
                # Calculate average distance to all food pellets
                avgFoodDist = sum(foodDistances) / len(foodDistances)
                score += 2.0 / (avgFoodDist + 1)
        
        # Bonus for eating food
        if currentGameState.getNumFood() > successorGameState.getNumFood():
            score += 10
        
        # Ghost evaluation
        for index, ghostState in enumerate(newGhostStates):
            ghostPos = ghostState.getPosition()
            ghostDist = manhattanDistance(newPos, ghostPos)
            
            # Handle ghost based on scared timer
            if ghostState.scaredTimer > 0:
                # Chase scared ghosts - more reward for closer ghosts
                score += 200 / (ghostDist + 1)
            else:
                # Avoid regular ghosts - severely penalize being too close
                if ghostDist < 2:
                    score -= 500  # Strong penalty for being in immediate danger
                elif ghostDist < 4:
                    score -= 100 / ghostDist  # Moderate penalty for being close
        
        # Avoid STOP action as it wastes time
        if action == Directions.STOP:
            score -= 5
        
        # Consider capsules (power pellets)
        capsules = successorGameState.getCapsules()
        if capsules:
            capsuleDistances = [manhattanDistance(newPos, capsule) for capsule in capsules]
            closestCapsuleDist = min(capsuleDistances)
            score += 5.0 / (closestCapsuleDist + 1)  # Reward being close to capsules
        
        # Bonus for eating a capsule
        if len(currentGameState.getCapsules()) > len(successorGameState.getCapsules()):
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

        def minimax_value(state, agent_index, depth):
            # Check if we're at a terminal state (win, lose, or depth limit)
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            
            # Get legal actions for the current agent
            legal_actions = state.getLegalActions(agent_index)
            
            # Max agent (Pacman) is agent 0
            if agent_index == 0:  # Pacman's turn (Max)
                value = float("-inf")
                for action in legal_actions:
                    successor = state.generateSuccessor(agent_index, action)
                    # The next agent will be the first ghost (agent 1)
                    value = max(value, minimax_value(successor, 1, depth))
                return value
            else:  # Ghost's turn (Min)
                value = float("inf")
                for action in legal_actions:
                    successor = state.generateSuccessor(agent_index, action)
                    
                    # Check if this is the last ghost
                    next_agent = agent_index + 1
                    
                    # If this was the last ghost, the next agent is Pacman (agent 0)
                    # and we decrease depth by 1 since a full ply is complete
                    if next_agent == state.getNumAgents():
                        next_agent = 0
                        next_depth = depth - 1
                    else:
                        next_depth = depth
                        
                    value = min(value, minimax_value(successor, next_agent, next_depth))
                return value
        
        # Main function to find the best action for Pacman
        actions = gameState.getLegalActions(0)
        best_action = Directions.STOP
        best_score = float("-inf")
        
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            score = minimax_value(successor, 1, self.depth)
            
            if score > best_score:
                best_score = score
                best_action = action
                
        return best_action

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        with alpha-beta pruning
        """
        def alpha_beta_value(state, agent_index, depth, alpha, beta):
            # Terminal state or depth limit
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)

            legal_actions = state.getLegalActions(agent_index)

            if agent_index == 0:  # Pacman (Max)
                value = float("-inf")
                for action in legal_actions:
                    successor = state.generateSuccessor(agent_index, action)
                    value = max(value, alpha_beta_value(successor, 1, depth, alpha, beta))
                    if value > beta:
                        return value  # Beta cutoff
                    alpha = max(alpha, value)
                return value
            else:  # Ghosts (Min)
                value = float("inf")
                for action in legal_actions:
                    successor = state.generateSuccessor(agent_index, action)
                    next_agent = agent_index + 1
                    next_depth = depth

                    if next_agent == state.getNumAgents():
                        next_agent = 0
                        next_depth -= 1

                    value = min(value, alpha_beta_value(successor, next_agent, next_depth, alpha, beta))
                    if value < alpha:
                        return value  # Alpha cutoff
                    beta = min(beta, value)
                return value

        # Initial call from Pacman
        best_score = float("-inf")
        best_action = Directions.STOP
        alpha = float("-inf")
        beta = float("inf")

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            score = alpha_beta_value(successor, 1, self.depth, alpha, beta)

            if score > best_score:
                best_score = score
                best_action = action

            alpha = max(alpha, best_score)

        return best_action

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
        def expectimax_value(state, agent_index, depth):
            # Check if we're at a terminal state (win, lose, or depth limit)
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            
            # Get legal actions for the current agent
            legal_actions = state.getLegalActions(agent_index)
            
            # Max agent (Pacman) is agent 0
            if agent_index == 0:  # Pacman's turn (Max)
                value = float("-inf")
                for action in legal_actions:
                    successor = state.generateSuccessor(agent_index, action)
                    # The next agent will be the first ghost (agent 1)
                    value = max(value, expectimax_value(successor, 1, depth))
                return value
            else:  # Ghost's turn (Chance/Expected value)
                value = 0
                # Calculate expected value assuming uniform probability distribution
                # over all possible ghost actions
                probability = 1.0 / len(legal_actions)
                
                for action in legal_actions:
                    successor = state.generateSuccessor(agent_index, action)
                    
                    # Check if this is the last ghost
                    next_agent = agent_index + 1
                    
                    # If this was the last ghost, the next agent is Pacman (agent 0)
                    # and we decrease depth by 1 since a full ply is complete
                    if next_agent == state.getNumAgents():
                        next_agent = 0
                        next_depth = depth - 1
                    else:
                        next_depth = depth
                    
                    # Sum the expected values (probability × value)
                    value += probability * expectimax_value(successor, next_agent, next_depth)
                
                return value
        
        # Main function to find the best action for Pacman
        actions = gameState.getLegalActions(0)
        best_action = Directions.STOP
        best_score = float("-inf")
        
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            score = expectimax_value(successor, 1, self.depth)
            
            if score > best_score:
                best_score = score
                best_action = action
                
        return best_action

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: This evaluation function considers several features:
    1. Current score - base component
    2. Distance to closest food - incentivize collecting food efficiently
    3. Food count - fewer remaining food items is better
    4. Capsule count - fewer remaining capsules is better
    5. Distance to closest capsule - incentivize getting capsules
    6. Ghost distances - avoid normal ghosts, chase scared ghosts
    7. Remaining scared timer - prioritize taking advantage of scared ghosts
    """
    # Current position and game state info
    pacmanPosition = currentGameState.getPacmanPosition()
    foodGrid = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()
    
    # Base score from the game
    score = currentGameState.getScore()
    
    # Food evaluation
    foodList = foodGrid.asList()
    
    # Distance to closest food
    if foodList:
        foodDistances = [manhattanDistance(pacmanPosition, food) for food in foodList]
        closestFoodDist = min(foodDistances)
        # Incentivize getting closer to food
        score += 5.0 / (closestFoodDist + 1)
        
        # The fewer food items remaining, the better
        score -= 4 * len(foodList)
        
        # Consider food clustering - if food is clustered, that's good
        if len(foodList) > 1:
            avgFoodDist = sum(foodDistances) / len(foodDistances)
            score += 1.0 / (avgFoodDist + 1)
    
    # Capsule evaluation
    if capsules:
        capsuleDistances = [manhattanDistance(pacmanPosition, capsule) for capsule in capsules]
        closestCapsuleDist = min(capsuleDistances)
        # Incentivize getting capsules
        score += 8.0 / (closestCapsuleDist + 1)
    
    # Fewer capsules is better (it means Pacman has eaten them)
    score -= 20 * len(capsules)
    
    # Ghost evaluation
    for ghostState in ghostStates:
        ghostPos = ghostState.getPosition()
        ghostDist = manhattanDistance(pacmanPosition, ghostPos)
        
        # If ghost is scared, chase it
        if ghostState.scaredTimer > 0:
            # The closer to a scared ghost, the better
            score += 200 / (ghostDist + 1)
            
            # The more remaining scared time, the better position we're in
            score += ghostState.scaredTimer * 5
        else:
            # Stay away from active ghosts
            if ghostDist < 2:
                # Strong penalty for being in immediate danger
                score -= 500
            elif ghostDist < 5:
                # Moderate penalty for being relatively close
                score -= 100 / ghostDist
    
    # Small additional reward for being in an open area (more escape options)
    walls = currentGameState.getWalls()
    numWallsAround = 0
    x, y = pacmanPosition
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        if walls[x + dx][y + dy]:
            numWallsAround += 1
    
    # Fewer walls around is better (more escape routes)
    score -= 5 * numWallsAround
    
    return score

# Abbreviation
better = betterEvaluationFunction
