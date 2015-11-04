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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        #Get the current score and use this as and use it as an evaluation for each potential reflex.
        #pacman is awarded or penalized points for each "decision" made.  Higher values are more encouraging.
        #We add the distance to the ghost to encourage pacman to stay away from the ghost
        score = successorGameState.getScore() + manhattanDistance(currentGameState.getGhostPosition(1), newPos)
        #make a list of all of the food
        food = newFood.asList()
        #set the closest food to a high number to check it against a distance heuristic to find the closest food
        closestFood = 100

        #Then, we calculate the distance to each piece of food that's remaining
        for foodLocation in food:
            #if we find a closer distance than the initial one, overwrite it
            distance = manhattanDistance(foodLocation, newPos)
            if (distance < closestFood):
                closestFood = distance
        #if we ate a piece of food, increment the score
        #I looked in pacman.py and found that killing ghosts awarded 200 points, so 100 is for eating food
        if (currentGameState.getNumFood() > successorGameState.getNumFood()):
            score += 92
        #If pacman has to stop at any point, he loses 5 points.  This will discourage stopping, somewhat
        if action == 'STOP':
            score -= 3
        #lose points for any step taking where food is not eaten.  This enourages more optimal path choices
        score -= 5 * closestFood
        #Pacman gets a bonus to his score for eating capsules that allow him to kill ghosts
        if successorGameState.getPacmanPosition() in currentGameState.getCapsules():
            score += 127
        #return the current resulting score based on the "decision" made
        return score

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

    def getAction(self, gameState):
        return self.maximize(gameState, 0, 1)

    def minimize(self, gameState, agentIndex, depth):
        value = 0
        bestValue = float('inf')
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)

        if agentIndex == 0:
            legalMoves = [action for action in gameState.getLegalActions(agentIndex) if action!='Stop']
        else:
            legalMoves = gameState.getLegalActions(agentIndex)

        for action in legalMoves:
            if agentIndex == gameState.getNumAgents() - 1:
                if depth == self.depth:
                    value = self.evaluationFunction(gameState.generateSuccessor(agentIndex, action))
                else:
                    value = self.maximize(gameState.generateSuccessor(agentIndex, action), 0, depth+1)
            else:
                value = self.minimize(gameState.generateSuccessor(agentIndex, action), agentIndex+1,depth)

            if value < bestValue:
                bestValue = value
        return value

    def maximize(self, gameState, agentIndex, depth):
        value = 0
        bestValue = float('-inf')
        bestMove = ""
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)

        #Remove the 'STOP' action from pacman.
        if agentIndex == 0:
            legalMoves = [action for action in gameState.getLegalActions(agentIndex) if action!='Stop']
        else:
            legalMoves = gameState.getLegalActions(agentIndex)

        for action in legalMoves:
            value = self.minimize(gameState.generateSuccessor(0, action), 1, depth)
            if value > bestValue:
                bestMove = action
                bestValue = value
        if depth == 1:
            return bestMove
        else:
            return bestValue


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

