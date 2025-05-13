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

        "*** YOUR CODE HERE ***"
        """
        The paramaters that are important for relexive behavior includes 
        distance from food, distance from ghost, and if food or ghost has eaten
        The latter 2 are already implemented, so let's implement the first 2
        
        1) Let's get closest food pellet [Manhattan Distance] (if tie randomly choose one)
           If we are getting closer, let's reward it
        2) Let's avoid ghosts in a radius from them by penalizing the action's score
           
        """
        
        # First let's get the base score of the game
        score = successorGameState.getScore()
        
        # 1) Find the closest Food Pellet
        # Reward closer food
        
        foodList = newFood.asList()
        if len(foodList) > 0:
            foodValues = (manhattanDistance(newPos,food)for food in foodList)
            minFoodDist = min(foodValues)
            score = score + (30/ minFoodDist) #10 is food eat score

        # Penalize being too close to ghosts
        for ghost in newGhostStates:
            ghostDist = manhattanDistance(newPos, ghost.getPosition())
            
            # attempt to use weighted distance
            # score = score - (100/ghostDist)
            
            #if the ghost is scared and its timer is greater than or equall to its distance,
            # we can ignore it
            
            #if ghost is scared
            if ghost.scaredTimer > 0:
                
                #only approach it if scared timer >= distance
                if ghostDist <= ghost.scaredTimer :
                    score += (10/ghostDist)+1
                else:
                    # avoid it as usual
                    if ghostDist < 3:
                        score += -200  # very risky
            else:
            # if ghost is not scared, avoid it
                
                if ghostDist < 3:
                    score += -200  # very risky

        # Reward eating food
        if successorGameState.getNumFood() < currentGameState.getNumFood():
            score += 50
            
        if action == Directions.STOP:
                    score += -20
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
        # util.raiseNotDefined()
        """
                STEPS to solve this problem
                Get Array of players
                set level depth = 1
                Function minmax tree (Players,depth,count)
                    if Player = Us, run max agent
                        Then minmax(players,depth,count+1)
                    if player is enemy Run min agent
                        Then minmax(players,depth,count+1)

                then return the best one

        """
        
        # Collect legal moves and successor states
        numAgents = gameState.getNumAgents()
        myActions = gameState.getLegalActions(0)
        newGameState = gameState.generateSuccessor(0, myActions[0])
        isWin = gameState.isWin()
        isLose = gameState.isLose()
        
        bestAction,_ = self.minimax(gameState,0,1)
        return bestAction
    
    def minimax(self, gameState, agentIndex, turn):
        # Terminal condition: if max turns reached or game over
        if turn > self.depth or gameState.isWin() or gameState.isLose():
            return None, self.evaluationFunction(gameState)

        # Determine next agent and possibly increment turn
        nextAgent = agentIndex + 1
        if nextAgent == gameState.getNumAgents():
            nextAgent = 0
            turn += 1

        legalActions = gameState.getLegalActions(agentIndex)
        if not legalActions:
            return None, self.evaluationFunction(gameState)

        # Store actions and their minimax values
        actionScores = {}

        for action in legalActions:
            successor = gameState.generateSuccessor(agentIndex, action)
            _, score = self.minimax(successor, nextAgent, turn)
            actionScores[action] = score

        # Pacman (MAX)
        if agentIndex == 0:
            bestAction = max(actionScores, key=actionScores.get)
            return (bestAction, actionScores[bestAction]) if turn == 1 else (None, actionScores[bestAction])

        # Ghosts (MIN)
        else:
            worstScore = min(actionScores.values())
            return None, worstScore
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        action,finalScore = self.minimaxAB(gameState,0,1,float('-inf'),float('inf'))
        return action
    def minimaxAB(self,gameState, playerIndex, turnIndex, alpha, beta):
        # Terminal condition: if max turns reached or game over
        if turnIndex > self.depth or gameState.isWin() or gameState.isLose():
            return None, self.evaluationFunction(gameState)

        # Increment turn and player counter
        nextPlayerIndex = playerIndex + 1
        nextTurnIndex = turnIndex
        if nextPlayerIndex == gameState.getNumAgents():
            nextPlayerIndex = 0
            nextTurnIndex += 1

        SuccessorScores = {}

        # Pacman (Maximizer)
        # if playerIndex == 0 and turnIndex == 1:
        if playerIndex == 0:
            bestScore = float('-inf')
            
            legalActions = gameState.getLegalActions(playerIndex)
            if not legalActions:
                return None, self.evaluationFunction(gameState)
        
            for action in legalActions:
                newGameState = gameState.generateSuccessor(playerIndex, action)
                _, newScore = self.minimaxAB(newGameState, nextPlayerIndex, nextTurnIndex, alpha, beta)
                SuccessorScores[action] = newScore

                if newScore >= bestScore:
                    bestScore = newScore
                if bestScore > alpha:
                    alpha = bestScore
                if  beta < alpha:
                    return None, bestScore


        # Enemy/Ghost (Minimizer)
        else:
            bestScore = float('inf')
            
            legalActions = gameState.getLegalActions(playerIndex)
            if not legalActions:
                return None, self.evaluationFunction(gameState)
            
            for action in legalActions:
                newGameState = gameState.generateSuccessor(playerIndex, action)
                _, newScore = self.minimaxAB(newGameState, nextPlayerIndex, nextTurnIndex, alpha, beta)
                SuccessorScores[action] = newScore

                if newScore <= bestScore:
                    bestScore = newScore
                if bestScore < beta:
                    beta = bestScore
                if beta < alpha:
                    return None,bestScore  # Prune

        # Return action and score for root Pacman, or just score otherwise
        if playerIndex == 0:
            if turnIndex == 1:
                bestAction = max(SuccessorScores, key=SuccessorScores.get)
                return (bestAction, SuccessorScores[bestAction])
            return None,max(SuccessorScores.values())
        else:
            return None, min(SuccessorScores.values())


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
        bestAction,_ = self.expectiMax(gameState,0,1)
        return bestAction
        
    def expectiMax(self, gameState, agentIndex, turn):
        # Terminal condition: if max turns reached or game over
        if turn > self.depth or gameState.isWin() or gameState.isLose():
            return None, self.evaluationFunction(gameState)

        # Determine next agent and possibly increment turn
        nextAgent = agentIndex + 1
        if nextAgent == gameState.getNumAgents():
            nextAgent = 0
            turn += 1

        legalActions = gameState.getLegalActions(agentIndex)
        if not legalActions:
            return None, self.evaluationFunction(gameState)

        # Store actions and their minimax values
        actionScores = {}

        for action in legalActions:
            successor = gameState.generateSuccessor(agentIndex, action)
            _, score = self.expectiMax(successor, nextAgent, turn)
            actionScores[action] = score

        # Pacman (MAX)
        if agentIndex == 0:
            bestAction = max(actionScores, key=actionScores.get)
            return (bestAction, actionScores[bestAction]) if turn == 1 else (None, actionScores[bestAction])

        # Ghosts (MIN)
        else:
            avgScore = sum(actionScores.values())/len(actionScores)
            return None, avgScore

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION:
    To evaluate a score thats more than just the food-Eaten score
    Other parameters to consider:
        Distance to Food, Number of Food pellets
        Distance from Ghosts
        Are Ghosts Scared?
        Capsule Distances? and Quantity?
        Future States
    """
    "*** YOUR CODE HERE ***"
    #Grab all variables\
     # Useful information you can extract from a GameState (pacman.py)
    
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    capsules = currentGameState.getCapsules()
    # First let's get the base score of the game
    score = currentGameState.getScore()
    
    # 1) Find the closest Food Pellet
    # Reward closer food
    
    foodList = food.asList()
    if len(foodList) > 0:
        # Reward our current state based on food closeness
        foodValues = (manhattanDistance(pos,food)for food in foodList)
        minFoodDist = min(foodValues)
        score = score + (10/ minFoodDist) #10 is food eat score

        # Reward our current state based on num of food pellets
        score += 100/len(foodList)
    else:
        #if the food array is empty, we win!
        score += 1000

    if len(capsules) >0:
        capsuleValues = (manhattanDistance(pos,cap) for cap in capsules)
        shortestCapDist = min(capsuleValues)
        score = score + (10/shortestCapDist)
        
        # score = 200/len(capsules)
    else:
        # if we ate all capsules we are doing better
        score += 400
    # Penalize being too close to ghosts
    for ghost in ghostStates:
        ghostDist = manhattanDistance(pos, ghost.getPosition())
        
        # attempt to use weighted distance
        # score = score - (100/ghostDist)
        
        #if the ghost is scared and its timer is greater than or equall to its distance,
        # we can ignore it
        
        #if ghost is scared
        if ghost.scaredTimer > 0:
            
            #only approach it if scared timer >= distance
            if ghostDist <= ghost.scaredTimer :
                score += (100/ghostDist)+1
            else:
                # avoid it as usual
                if ghostDist < 3:
                    score += -200  # very risky
        else:
        # if ghost is not scared, avoid it
            
            if ghostDist < 3:
                score += -200  # very risky

    return score


# Abbreviation
better = betterEvaluationFunction
