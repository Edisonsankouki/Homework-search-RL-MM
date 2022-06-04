from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


def minmaxinterface(instance, gameState, depth, agentnum):
    maxvalues = []
    comparearray = []
    if gameState.isWin() or gameState.isLose():
        return instance.evaluationFunction(gameState)
    if depth > 0:
        if depth % agentnum == 0:
            NumberofAgent = 0
        else:
            NumberofAgent = agentnum - (depth % agentnum)

        legalactions = gameState.getLegalActions(NumberofAgent)
        for action in legalactions:
            successors = gameState.generateSuccessor(NumberofAgent, action)
            if NumberofAgent == 0:
                maxvalues.append((minmaxinterface(instance, successors, depth - 1, agentnum), action))
                maxvalue = max(maxvalues)
                instance.value_max = maxvalue[0]
                instance.action = maxvalue[1]
            else:
                if isinstance(instance, MinimaxAgent):
                    comparearray.append((minmaxinterface(instance, successors, depth - 1, agentnum), action))
                    minvalue = min(comparearray)
                    instance.value_min = minvalue[0]

                if isinstance(instance, ExpectimaxAgent):
                    comparearray.append((minmaxinterface(instance, successors, depth - 1, agentnum), action))
                    avg = float(0)
                    for x in comparearray:
                        avg += comparearray[comparearray.index(x)][0]
                    avg /= len(comparearray)
                    instance.value_avg = avg
        if NumberofAgent == 0:
            return instance.value_max
        else:
            if isinstance(instance, MinimaxAgent):
                return instance.value_min
            else:
                return instance.value_avg

    else:
        return instance.evaluationFunction(gameState)


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
        if "Stop" in legalMoves:
            legalMoves.remove("Stop")

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)

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


        score = successorGameState.getScore()

        return self.Scorecounter(newPos,newFood,newGhostStates,score)



    def Scorecounter(self, newPos, newFood,newGhostStates,score):
        #calculate avg food fistance
        fd_distances = []
        for x, row in enumerate(newFood):
            for y, column in enumerate(newFood[x]):
                if newFood[x][y]:
                    fd_distances.append(manhattanDistance(newPos, (x,y)))
        avgDistance = sum(fd_distances)/float(len(fd_distances)) if (fd_distances and sum(fd_distances) != 0) else 1
        #calculate sum of surrounding food
        count = 0
        for x in range(newPos[0]-2, newPos[0]+3):
            for y in range(newPos[1]-2, newPos[1]+3):
                if (x>=0 and x < len(list(newFood))) and (y >= 0 and y < len(list(newFood[1]))) and newFood[x][y]:
                    count += 1
        #calculate manhatan distance for each ghost and select the min
        gh_distances = []
        for ghoststate in newGhostStates:
            ghost_coordinate = ghoststate.getPosition()
            gh_distances.append(manhattanDistance(newPos, ghost_coordinate))
        if gh_distances and min(gh_distances) != 0:
            mindis =  min(gh_distances)
        else:
            mindis = 1

        return 2.0 / mindis + score + count + 10.0 / avgDistance

def manhattanDistance(xy1, xy2):
    "Returns the Manhattan distance between points xy1 and xy2"
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.action = Directions.STOP
        self.value_max = -100000
        self.value_min = 100000
        self.value_avg = 100000


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
        """
        "*** YOUR CODE HERE ***"
        num_of_agents = gameState.getNumAgents()
        depth1 = self.depth * num_of_agents

        minmaxinterface(self,gameState, depth1, num_of_agents)
        return self.action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        num_of_agents = gameState.getNumAgents()
        value, action = self.alpha(gameState, float('-inf'), float('inf'), 0, self.depth)
        return action


    def alpha(self,state,a,b,agentNumber,depth):
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state),'none'
        value = float('-inf')
        Actions = state.getLegalActions(agentNumber)
        nextmove = Actions[0]

        for x in Actions:
            i = value
            successor = state.generateSuccessor(agentNumber, x)
            if depth == 0 or successor.isWin() or successor.isLose():
                value = max(value,self.evaluationFunction(successor))
            else:
                value = max(value,self.beta(successor,a,b,agentNumber+1,depth))
            if value > b:
                return value,x
            a = max(a,value)
            if value != i:
                nextmove = x
        return value,nextmove


    def beta(self,state,a,b,agentNumber,depth):
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state), 'none'
        value = float('inf')
        actions = state.getLegalActions(agentNumber)
        flag = False
        for action in actions:

            successor = state.generateSuccessor(agentNumber, action)
            if depth == 0 or successor.isWin() or successor.isLose():

                value = min(value, self.evaluationFunction(successor))
            elif agentNumber == (state.getNumAgents() - 1):
                if flag == False:
                    depth -=  1
                    flag = True
                if depth == 0:
                    value = min(value, self.evaluationFunction(successor))
                else:
                    value = min(value, self.alpha(successor, a, b, 0, depth)[0])

            else:
                value = min(value, self.beta(successor, a, b, agentNumber + 1, depth))
            if value < a:
                return value
            b = min(b, value)

        return value




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
        num_of_agents = gameState.getNumAgents()
        depth1 = self.depth * num_of_agents

        minmaxinterface(self,gameState, depth1, num_of_agents)
        return self.action



def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
      DESCRIPTION: <write something here so we know what you did>
    """
    position = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates()
    result = currentGameState.getScore()
    foods = currentGameState.getFood().asList()

    mindistance = -float("inf")
    for food in foods:
        if mindistance > manhattanDistance(food, position):
            mindistance = manhattanDistance(food, position)

    if mindistance == -float("inf"):
        mindistance = 0
    result += -mindistance

    for x in ghostStates:
        if x.scaredTimer == 0:
            result += -5 * manhattanDistance(x.getPosition(), position)
        elif x.scaredTimer > 0:
            result += -manhattanDistance(x.getPosition(), position)

    return result


# Abbreviation
better = betterEvaluationFunction