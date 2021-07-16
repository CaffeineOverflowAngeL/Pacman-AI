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

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
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

    def evaluationFunction(self, currentGameState, action):
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
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #
        numberOfGhosts = gameState.getNumAgents() - 1
        #print(self.depth)
        def miniMax(gameState, depth, agentIndex):
            # pacmans turn 
            if agentIndex == 0 : 
                #Every time its pacmans turn -> increase depth ( full cycle of moves has occured )
                currDepth = depth + 1
                #if current game state is a terminating state 
                #or if we reached max depth , then terminate
                if gameState.isWin() or gameState.isLose() or currDepth==self.depth:   
                  return self.evaluationFunction(gameState)
                #initiate max value to - infinite (here we use a really small number considering the values returned from pacman)
                maxvalue = -1e10
                #get all legal actions associated to the current game state
                actions = gameState.getLegalActions(0)
                for action in actions:
                    #get successor
                  successor= gameState.generateSuccessor(0,action)
                  #caclulate max number between current max and the value 
                  #that occurs from successors state
                  eval = miniMax(successor,currDepth,1)
                  maxvalue = max (maxvalue,eval)
                return maxvalue
            #agents turns 
            else: 
                minvalue = 1e10
                if gameState.isWin() or gameState.isLose():   
                  return self.evaluationFunction(gameState)
                actions = gameState.getLegalActions(agentIndex)
                for action in actions:
                  successor= gameState.generateSuccessor(agentIndex,action)
                  if agentIndex == (gameState.getNumAgents() - 1):
                    eval = miniMax(successor,depth,0)
                    minvalue = min (minvalue,eval)
                  else:
                    eval = miniMax(successor,depth,agentIndex+1)
                    minvalue = min(minvalue,eval)
                return minvalue


        
        #Root level action.
        #get pacmans iniate legal actions
        actions = gameState.getLegalActions(0)
        #iniate score to minimum 
        currentScore = -1e10
        #iniate solution action to null 
        returnAction = ''
        for action in actions:
            nextState = gameState.generateSuccessor(0,action)
            # Since we started with pacman first , now we have to call 
            # miniMax for the agents in the current depth 
            score = miniMax(nextState,0,1)
            # Choosing the action which is Maximum of the successors.
            if score > currentScore:
                returnAction = action
                currentScore = score
        return returnAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        numberOfGhosts = gameState.getNumAgents() - 1
        #print(self.depth)
        def miniMax(gameState, depth, alpha , beta, agentIndex):
            # pacmans turn 
            if agentIndex == 0 : 
                #Every time its pacmans turn -> increase depth ( full cycle of moves has occured )
                currDepth = depth + 1
                #if current game state is a terminating state 
                #or if we reached max depth , then terminate
                if gameState.isWin() or gameState.isLose() or currDepth==self.depth:   
                  return self.evaluationFunction(gameState)
                #initiate max value to - infinite (here we use a really small number considering the values returned from pacman)
                maxvalue = -1e10
                #get all legal actions associated to the current game state
                actions = gameState.getLegalActions(0)
                alpha1 = alpha
                for action in actions:
                    #get successor
                  successor= gameState.generateSuccessor(0,action)
                  #caclulate max number between current max and the value 
                  #that occurs from successors state
                  eval = miniMax(successor,currDepth, alpha,beta,1)
                  maxvalue = max (maxvalue,eval)
                  alpha = max(alpha,eval)
                  if beta < alpha: 
                      break
                return maxvalue
            #agents turns 
            else: 
                minvalue = 1e10
                if gameState.isWin() or gameState.isLose():   
                  return self.evaluationFunction(gameState)
                actions = gameState.getLegalActions(agentIndex)
                for action in actions:
                  successor= gameState.generateSuccessor(agentIndex,action)
                  if agentIndex == (gameState.getNumAgents() - 1):
                    eval = miniMax(successor,depth, alpha, beta,0)
                    minvalue = min (minvalue,eval)
                    beta = min(beta,eval)
                    if beta < alpha:
                        break
                  else:
                    eval = miniMax(successor,depth, alpha , beta,agentIndex+1)
                    minvalue = min(minvalue,eval)
                    beta = min(beta,eval)
                    if beta < alpha:
                        break
                return minvalue


        
        #Root level action.
        #get pacmans iniate legal actions
        actions = gameState.getLegalActions(0)
        #iniate score to minimum 
        currentScore = -1e10
        #iniate solution action to null 
        returnAction = ''
        #initiate alpha and beta 
        alpha = -1e10 
        beta = 1e10
        for action in actions:
            nextState = gameState.generateSuccessor(0,action)
            # Since we started with pacman first , now we have to call 
            # miniMax for the agents in the current depth 
            score = miniMax(nextState,0,alpha,beta,1)
            # Choosing the action which is Maximum of the successors.
            if score > currentScore:
                returnAction = action
                currentScore = score
            if score > beta: 
                return returnAction
            alpha = max(alpha,score)
        return returnAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        numberOfGhosts = gameState.getNumAgents() - 1
        #print(self.depth)
        def expectiMax(gameState, depth, agentIndex):
            # if next agent is MAX : return max-value(state)
            if agentIndex == 0 : 
                #Every time its pacmans turn -> increase depth ( full cycle of moves has occured )
                currDepth = depth + 1
                #if current game state is a terminating state 
                #or if we reached max depth , then terminate
                if gameState.isWin() or gameState.isLose() or currDepth==self.depth:   
                  return self.evaluationFunction(gameState)
                #initiate max value to - infinite (here we use a really small number considering the values returned from pacman)
                maxvalue = -1e10
                #get all legal actions associated to the current game state
                actions = gameState.getLegalActions(0)
                for action in actions:
                    #get successor
                  successor= gameState.generateSuccessor(0,action)
                  #caclulate max number between current max and the value 
                  #that occurs from successors state
                  eval = expectiMax(successor,currDepth,1)
                  maxvalue = max (maxvalue,eval)
                return maxvalue
            #if next agent is EXP : return exp-value(state) 
            else: 
                expvalue = 0
                if gameState.isWin() or gameState.isLose():   
                  return self.evaluationFunction(gameState)
                actions = gameState.getLegalActions(agentIndex)
                numberOfactions = len(actions)
                for action in actions:
                  successor= gameState.generateSuccessor(agentIndex,action)
                  p = 1/numberOfactions
                  if agentIndex == (gameState.getNumAgents() - 1):
                    eval = expectiMax(successor,depth,0)
                    expvalue += p*eval 
                  else:
                    eval = expectiMax(successor,depth,agentIndex+1)
                    expvalue += p*eval
                return expvalue


        
        #Root level action.
        #get pacmans iniate legal actions
        actions = gameState.getLegalActions(0)
        #iniate score to minimum 
        currentScore = -1e10
        #iniate solution action to null 
        returnAction = ''
        for action in actions:
            nextState = gameState.generateSuccessor(0,action)
            # Since we started with pacman first , now we have to call 
            # miniMax for the agents in the current depth 
            score = expectiMax(nextState,0,1)
            # Choosing the action which is Maximum of the successors.
            if score > currentScore:
                returnAction = action
                currentScore = score
        return returnAction

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    #score based on pacmans distances from ghots 
    def _scoreDistanceGhost(gameState):
      score = 0
      #calculate pacmans distance from each ghost in the game state
      for ghost in gameState.getGhostStates():
        ghostDinstance = manhattanDistance(gameState.getPacmanPosition(), ghost.getPosition())
        #if ghost is scared 
        if ghost.scaredTimer > 0: 
          #score is occurs base on the remaining scared timer and the distance between the scared ghost and pacman
          score += max(9-ghostDinstance,0)*ghost.scaredTimer
        else:
          #if ghost is not scared , the closer the ghost is to pacman the more negative the score that occurs is
          #we use the exponential function to simulate that 

          score -= pow(2.71828,(max(5-ghostDinstance,2)))

      return score



    def _scoreDistanceFood(gameState):
      foodDistance = []
      dotDistance = []

      #If there are no more food dots left -> return 0
      foodDots = gameState.getFood().asList()
      if len(foodDots) == 0:
        return 0

      #Find the dot which is closer to current pacmans position
      for dot in foodDots: 
        distance = util.manhattanDistance(gameState.getPacmanPosition(),dot)  
        foodDistance.append((distance,dot))
    
      #Get the smallest value item in the list
      minDist , minDot = min(foodDistance)

      for dot_dot in foodDots: 
        dot_distance = manhattanDistance(minDot,dot_dot)
        dotDistance.append(dot_distance)

      dotDot = max(dotDistance, default=0)
      #print(minDist)

      if (minDist == 0):
        #print("minDist equals 0 !")
        minDist = 0.1
      if (dotDot == 0):
        #print("dotDot equals 0 !")
        return (1.0/minDist)
      return (1.0/minDist) + (1.0/dotDot)  #min(foodDistance)
      #1.0/(minDist + dotDot)


    def _scoreFromBigDots(gameState):

      score = []
      bigFoodDots = gameState.getCapsules()

      #terminate 
      if len(bigFoodDots) == 0:
        return 0

      #for every capsule in game state 
      for Cap in gameState.getCapsules():
        #my strategy higly evaluates capsules and considers them a huge win condition 
        #thats why the score that is corresponded to them has max ceiling 200 in contrast to normal food dots which has 1.0 
        #Capsule value = 200*foodDot value
        score.append(200.0/manhattanDistance(gameState.getPacmanPosition(), Cap))
      return max(score)


    #calculate each score for current game state
    score = currentGameState.getScore()
    scoreGhosts = _scoreDistanceGhost(currentGameState)
    scoreFood = _scoreDistanceFood(currentGameState)
    scoreCapsules = _scoreFromBigDots(currentGameState)
    #print('Score: %f, ghosts: %f , food: %f , cap: %f ',score, scoreGhosts,scoreFood,scoreCapsules)
    #aggregate all scores for current game state
    return  score + scoreGhosts + scoreFood + scoreCapsules

# Abbreviation
better = betterEvaluationFunction

#1257.3
#1308.9