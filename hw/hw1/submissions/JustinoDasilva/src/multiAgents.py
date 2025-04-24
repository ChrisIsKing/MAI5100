
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
        #return legalMoves[0]

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
        #print(newGhostStates[0],newGhostStates[1])
        #
        #calculate nuber of steps ghosts requirs to reac pacman, the  the farter the  more valuabel the moce

        #newGhostStates[0].getDirection() gets possible direction fo ghostType
        #print(newFood[newPos[0]][newPos[1]]) determine is the new postition to move to has  food.
        #gx,gy=newGhostStates[0]['Ghost']
        """"
        1.calculate the numeber of steps requrire to reac pacman. for each step one  to score
        2. if packman direcion is  not the same as opppostte of pacman reduce by
        """
        '*** get distance  of pacman from ghost ***'
        '*** if pacman is coming in your direction but ther is a awall'
        ##check if ther is food in the chosen Directions
        distance=1
        height=newFood.height
        width=newFood.width
        hasfood={'North':0,'South':0,'East':0,'West':0}
        x,y=currentGameState.getPacmanPosition();


        'searching for food'
        #print('x :',x,'y :',y)
        if action =='North':
            for newY in range(y,height,1):
                if newFood[x][newY]==True:
                    hasfood[action]=hasfood[action]+1
            distance=distance+hasfood[action]
        elif action=='South':
            for newY in range(y,0,-1):
                if newFood[x][newY]==True:
                    hasfood[action]=hasfood[action]+1
            distance=distance+hasfood[action]
        elif action=='East':
            for newX in range(x,width,1):
                if newFood[newX][y]==True:
                    hasfood[action]=hasfood[action]+1
            distance=distance+hasfood[action]
        elif action=='West':
            for newX in range(x,0,-1):
                if newFood[newX][y]==True:
                    hasfood[action]=hasfood[action]+1
            distance=distance+hasfood[action]



        '''searching for food'''


        ghostDirection=newGhostStates[0].getDirection()
        scared=max(newScaredTimes)
        gx,gy=newGhostStates[0].getPosition()
        px,py=newPos


        if action==ghostDirection:

            '''pacman is in the same row or column as ghost'''
            if action in ['West','East']:
               if px==gx:
                   distance=distance+1
                   if scared>0:
                       distance=distance+3

               else:
                   distance=distance+2


            elif action in ['North','South']:
                if py==gy:
                    distance=distance+1
                    if scared>0:
                        distance=distance+3
                else:
                    distance=distance+2


        '''pacman is going west'''
        if action=='West':

            if ghostDirection=='East':
                if (abs(px-gx)+abs(py-gy))<(abs(px-(gx+1))+abs(py-gy)):
                    distance=distance+distance+2
                    if scared>0:
                        distance=distance+3
                        if px==gx:
                            distance=distance+3
                        else:
                            distance=distance+2
                    else:
                        distance=distance-1
                else:
                    distance=distance+distance/2


            elif ghostDirection=='South':
                if(abs(px-gx)+abs(py-gy))<(abs(px-gx)+abs(py-(gy-1))):
                    distance=distance+distance+2
                else:
                    distance=distance+distance/2


            else:
                if(abs(px-gx)+abs(py-gy))<(abs(px-gx)+abs(py-(gy+1))):
                    distance=distance+distance+2
                else:
                    distance=distance+distance/2


        '''packman is going north'''
        if action=='North':
            if ghostDirection=='South':
                if(abs(px-gx)+abs(py-gy))<(abs(px-gx)+abs(py-(gy-1))):
                    distance=distance+distance+2
                    if scared>0:
                        distance=distance+3
                        if gy==py:
                            distance=distance+3
                        else:
                            distance=distance+2
                    else:
                        distance=distance-1
                else:
                    distance=distance+distance/2


            elif ghostDirection=='East':
                if(abs(px-gx)+abs(py-gy))<(abs(px-(gx+1))+abs(py-gy)):
                    distance=distance+distance+2
                else:
                    distance=distance+distance/2
                if px==(gx+1):
                    distance=distance-(distance/2)

            else:
                if(abs(px-gx)+abs(py-gy))<(abs(px-(gx-1))+abs(py-gy)):
                    distance=distance+distance+2
                else:
                    distance=distance+distance/2


        '''packman is ogitn south'''
        if action=='South':
            if ghostDirection=='North':
                if(abs(px-gx)+abs(py-gy))<(abs(px-gx)+abs(py-(gy+1))):
                    distance=distance+distance+2
                    if scared>0:
                        distance=distance+3
                        if py==gy:
                            distance=distance+3
                        else:
                            distance=distance+2
                    else:
                        distance=distance-1
                else:
                    distance=distance+distance/2


            elif ghostDirection=='East':
                if(abs(px-gx)+abs(py-gy))<(abs(px-(gx+1))+abs(py-gy)):
                    distance=distance+distance+2
                else:
                    distance=distance+distance/2

            else:
                if(abs(px-gx)+abs(py-gy))<(abs(px-(gx-1))+abs(py-gy)):
                    distance=distance+distance+2
                else:
                    distance=distance+distance/2

        ''' pacman is going East'''
        if action=='East':
            if ghostDirection=='West':
                if(abs(px-gx)+abs(py-gy))<(abs(px-(gx-1))+abs(py-gy)):
                    distance=distance+distance+2
                    if scared>0:
                        distance=distance+3
                        if px==gx:
                            distance=distance+3
                        else:
                            distance=distance+2
                    else:
                        distance=distance-1
                else:
                    distance=distance+distance/2


            elif ghostDirection=='North':
                if(abs(px-gx)+abs(py-gy))<(abs(px-gx)+abs(py-(gy+1))):
                    distance=distance+distance+2
                else:
                    distance=distance+distance/2


            else:
                if(abs(px-gx)+abs(py-gy))<(abs(px-gx)+abs(py-(gy-1))):
                    distance=distance+distance+2
                else:
                    distance=distance+distance/2






        if scared==0:
            distance=distance/2
        else:
            distance=distance*scared+len(newScaredTimes)





        '''*** compare direction of pacman and'''
        #if newFood[px][py]==True:
        #    distance=distance+1

        #if newFood[newPos[0]][newPos[1]]==False:
        #    addededvalue=addededvalue+1
        #gx,gy=newGhostStates.getPosition()

        #print(action,newGhostStates[0].getDirection())



        return successorGameState.getScore()+distance

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
    '''minmax tree  contains wight and action'''



    #def getAction(self, gameState: GameState):
    ''''successorGameState = currentGameState.generatePacmanSuccessor(action)

    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]'''
    def getAction(self, gameState):

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
        """
        "*** YOUR CODE HERE ***"

        # Format of result = [score, action]
        ''' call call to max '''

        # Return the action from result
        return self.maxValue(gameState,0,0)[1]

    #pacman is moving
    def maxValue(self,gameState,agent,depth):
            if  len(gameState.getLegalActions(agent))==0 or depth==self.depth:
               #print("calling Score: NumberOfLegalMoves: ",NumberOfActions,"depth: ",depth,"function Depth: ",self.depth)
               #exit(str(depth)+"hhhhhhhhhh")
               return self.evaluationFunction(gameState),None
            #get all legal moves of pacmane
            legalMoves=gameState.getLegalActions(0)
            #set the best move to lowest possible
            bestMove=float('-inf')
            bestAction=None
            for actions in legalMoves:
                GhostToMove=gameState.generateSuccessor(0,actions)
                nextDepth=depth
                newAgentToMove=agent+1
                CostToMove=self.minValue(GhostToMove,newAgentToMove,nextDepth)[0]
                #if we find a better move that the current move update it
                if CostToMove>bestMove:

                    bestMove=CostToMove
                    bestAction=actions
            #return the maxkim move for pacman on this leaf in case of multi layer
            return bestMove,bestAction

    #ghost is moving
    def minValue(self,gameState,agent,depth):
            if  len(gameState.getLegalActions(agent))==0 or depth==self.depth:
               #print("calling Score: NumberOfLegalMoves: ",NumberOfActions,"depth: ",depth,"function Depth: ",self.depth)
               #exit(str(depth)+"hhhhhhhhhh")
               return self.evaluationFunction(gameState),None

            NumberOfAgents=gameState.getNumAgents()
            legalMoves=gameState.getLegalActions(agent)
            worstMove=float('inf')
            worstAction=None
            #newAgentToMove=None

            for actions in legalMoves:
                newGameState=gameState.generateSuccessor(agent,actions)
                if agent<NumberOfAgents-1:
                    #all the ghost haven't moved new ghost to move
                    newAgentToMove=agent+1
                    nextDepth=depth
                    CostToMove=self.minValue(newGameState,newAgentToMove,nextDepth)[0]
                else:
                    # one level is complete it's pacman turn to move again
                    #move to the next level by increasing depth
                    newAgentToMove=0
                    nextDepth=depth+1
                    CostToMove=self.maxValue(newGameState,newAgentToMove,nextDepth)[0]

                #minimuze both pacman and otherchosts moves
                if worstMove>CostToMove:
                    worstMove=CostToMove
                    worstAction=actions

            return worstMove,worstAction
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):

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
        """
        "*** YOUR CODE HERE ***"

        # Format of result = [score, action]
        ''' call call to max '''
        agent=0
        currentDept=0
        alpha=float('-inf')
        beta=float('inf')
        # Return the action from result
        return self.maxValueAB(gameState,agent,currentDept,alpha,beta)[1]

    #pacman is moving
    def maxValueAB(self,gameState,agent,depth,alpha,beta):
            if  len(gameState.getLegalActions(agent))==0 or depth==self.depth or gameState.isLose():
                return self.evaluationFunction(gameState),None
            #get all legal moves of pacmane
            legalMoves=gameState.getLegalActions(0)
            #set the best move to lowest possible
            bestMove=float('-inf')
            bestAction=None
            for actions in legalMoves:
                GhostToMove=gameState.generateSuccessor(0,actions)
                nextDepth=depth
                newAgentToMove=agent+1
                CostToMove=self.minValueAB(GhostToMove,newAgentToMove,nextDepth,alpha,beta)[0]
                #if we find a better move that the current move update it


                if CostToMove>bestMove:
                    bestMove=CostToMove
                    bestAction=actions

                #we update alpha if best move is better
                alpha=max(alpha,bestMove)
                # if best move so far is better than beta we return it
                if bestMove>beta:
                    return bestMove,bestAction
            return bestMove,bestAction

    #ghost is moving
    def minValueAB(self,gameState,agent,depth,alpha,beta):
            if  len(gameState.getLegalActions(agent))==0 or depth==self.depth or gameState.isLose():
               #print("calling Score: NumberOfLegalMoves: ",NumberOfActions,"depth: ",depth,"function Depth: ",self.depth)
               #exit(str(depth)+"hhhhhhhhhh")
               #print("Value i gotttttttttttttttttttt:",self.evaluationFunction(gameState))
               return self.evaluationFunction(gameState),None

            NumberOfAgents=gameState.getNumAgents()
            legalMoves=gameState.getLegalActions(agent)
            worstMove=float('inf')
            worstAction=None
            #newAgentToMove=None

            for actions in legalMoves:
                newGameState=gameState.generateSuccessor(agent,actions)
                if agent<NumberOfAgents-1:
                    #all the ghost haven't moved new ghost to move
                    newAgentToMove=agent+1
                    nextDepth=depth
                    CostToMove=self.minValueAB(newGameState,newAgentToMove,nextDepth,alpha,beta)[0]
                else:
                    # one level is complete it's pacman turn to move again
                    #move to the next level by increasing depth
                    newAgentToMove=0
                    nextDepth=depth+1
                    CostToMove=self.maxValueAB(newGameState,newAgentToMove,nextDepth,alpha,beta)[0]

                #minimuze both pacman and otherchosts moves
                #print('Minnnnnnnnnnnnnnnnn',CostToMove,worstMove)

                if worstMove>CostToMove:
                    worstAction=actions
                    worstMove=CostToMove
                    #beta=worstMove
                beta=min(beta,worstMove)
                # we are mininmizain sor if we find a move that is es
                if CostToMove <alpha:
                    return worstMove,worstAction
                #if worstMove>CostToMove:

                    #worstMove=CostToMove
                    #worstAction=actions

            return worstMove,worstAction
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
        agent=0
        currentDept=0
        # Return the action from result
        return self.maxOfAverage(gameState,agent,currentDept)[1]

    #pacman is moving
    def maxOfAverage(self,gameState,agent,depth):
            if  len(gameState.getLegalActions(agent))==0 or depth==self.depth or gameState.isLose():
                return self.evaluationFunction(gameState),None
            #get all legal moves of pacmane
            legalMoves=gameState.getLegalActions(0)
            #set the best move to lowest possible
            bestMove=float('-inf')
            bestAction=None
            MovesCostArray=[]
            for actions in legalMoves:
                GhostToMove=gameState.generateSuccessor(0,actions)
                nextDepth=depth
                newAgentToMove=agent+1
                CostToMove=self.averageValue(GhostToMove,newAgentToMove,nextDepth)[0]

                if CostToMove> bestMove:
                    bestMove=CostToMove
                    bestAction=actions
            return bestMove,bestAction




    #ghost is moving
    def averageValue(self,gameState,agent,depth):
            #if you are in a losing state still return the value as it is use to calaulate the averade.
            if  len(gameState.getLegalActions(agent))==0 or depth==self.depth or gameState.isLose():
               return self.evaluationFunction(gameState),None
            NumberOfAgents=gameState.getNumAgents()
            #get all legal moves for ghosts
            legalMoves=gameState.getLegalActions(agent)
            total=0
            for actions in legalMoves:
                newGameState=gameState.generateSuccessor(agent,actions)
                if agent<NumberOfAgents-1:
                    #all the ghost haven't moved new ghost to move
                    newAgentToMove=agent+1
                    #depth remains the same as  ther are still more ghosts to move
                    nextDepth=depth
                    CostToMove=self.averageValue(newGameState,newAgentToMove,nextDepth)[0]
                else:
                    # one level is complete it's pacman turn to move again
                    #move to the next level by increasing depth
                    newAgentToMove=0
                    nextDepth=depth+1
                    CostToMove=self.maxOfAverage(newGameState,newAgentToMove,nextDepth)[0]
                #sum all movecost  to find the averade of all, whic is wht MAX needd
                total=total+CostToMove

            # return the average value of legal moves, None of the nodes have this value so we don't return an action
            return total/len(legalMoves),None



def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).


    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    value=0
    ppos=currentGameState.getPacmanPosition()
    gpos=currentGameState.getGhostStates()
    #print("fffffffffffffffffffffffffffffffffffffprinting ghostpositions",gpos[0])

    px,py=ppos
    gx,gy=gpos[0].getPosition()
    Gpostion=gpos[0].getPosition()
    scared=gpos[0].scaredTimer
    pacmanDirection=currentGameState.getPacmanState().getDirection()
    foods=currentGameState.getFood()
    bigfood=currentGameState.data.capsules

    if ppos==gpos:
        return -10
    else:
        value=value+abs(px-gx)+abs(py-gy)

    '''if pacmanDirection=='North':
        for y in range(py,foods.height,1):
            if foods[px][y]==True:
                value=value+10
    elif pacmanDirection=='South':
        for y in range(py,foods.height,-1):
            if foods[px][y]==True:
                value=value+10
            else:
                value=value-1

    elif pacmanDirection=='East':
        for x in range(px,foods.width,1):
            if foods[x][py]==True:
                value=value+10
            else:
                value=value-1

    elif pacmanDirection=='West':
        for x in range(px,foods.width,-1):
            if foods[x][py]==True:
                value=value+10
            else:
                 value=value-1
    else:
        value=value-10'''










    #hasfood={'North':0,'South':0,'East':0,'West':0}


    for point in bigfood:
        if ppos==point:
            value=value+20


    if foods[px][py]==True:
        vlaue=value+10
    else:
        value=value+1
    if scared>0:
        value=value+scared
    else:
        value=value-1





    return value

    #util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
