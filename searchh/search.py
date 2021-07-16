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


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
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
    from util import Stack

    successors = []
    visited = []


    tree=util.Stack() #Initializing the desicion tree with a stack (Stack is a better fit for dfs). A LIFO queue allows us to search in depth because we can visit the last node that was inserted to our queue. In this case we first examine the furthest nodes connected to our initiale node , back to the closest ones. There are no weights on the edges of the graph so we can use this technique.


    #Problems iniate state is added to the stack 
    
    tree.push(((problem.getStartState()),[])) #variable type of (coordinates , path)


    while(not tree.isEmpty()):

        (currentState, path)=tree.pop()

        if currentState not in visited:

            #mark current node as visited
            visited.append(currentState)

            if(problem.isGoalState(currentState)):
                #breaks while and returns path 
                break

            successors = problem.getSuccessors(currentState)

            for node in successors:
                #if already on the queue -> DO NOT ADD IT AGAIN
                if(node[0] not in visited):
                    tree.push((node[0], path + [node[1]]))


    return path

    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    successors = []
    visited = []
    #counter = 0 DEBUGGING 


    tree=util.Queue() #We make use of a FIFO Queue, because in order to search in breadth we have to visit all neighbour nodes first 

    #Problems iniate state is added to the stack 
    tree.push(((problem.getStartState()),[])) 
    #visited.append(problem.getStartState())


    while(not tree.isEmpty()):
        (currentState, path)=tree.pop()
        #counter=counter+1  #Debugging message to check how many time while loop was excecuted -> how many items where inserted into the queue

        if currentState not in visited:

            visited.append(currentState)

            if(problem.isGoalState(currentState)):
                break

            #get current nodes neighbors 
            successors = problem.getSuccessors(currentState)

            for node in successors:
                #if already on the queue -> DO NOT ADD IT AGAIN
                if(node[0] not in visited):
                    tree.push((node[0], path + [node[1]]))

    #print(counter) #debug msg -> how many items where inserted into the queue
    return path

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    successors = []
    visited = {}
    #counter = 0 DEBUGGING 


    tree=util.PriorityQueue()

    tree.push((problem.getStartState(), [] , 0), 0) #variable type : coords , path , cost 

    while(not tree.isEmpty()):
        
        currentState, path, cost=tree.pop()

        #check if current state has never been visited 
        #or if it has been visited and its cost is higher than the current one
        if(currentState not in visited) or (cost < visited[currentState]):
            #update the minimum cost of the current state
            visited[currentState] = cost 

            #if the current node is the goal state then exit while and return path
            if(problem.isGoalState(currentState)):
                break

            #get successor nodes
            successors = problem.getSuccessors(currentState)
            
            #iniate each successor node and push him into Priority Queue
            for node in successors: 
                tree.update((node[0], path + [node[1]], cost + node[2]), cost + node[2])

    return path

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    visited = []
    #counter = 0 DEBUGGING 
    tree=util.PriorityQueue()

    tree.push((problem.getStartState(), [] , 0), 0) #variable type : (coords , path , actual cost), heuristic cost 

    while (not tree.isEmpty()):

        #priority Queue pops every time the object with the smallest cost
        currentState, path, cost=tree.pop()

        #print("cost",cost)
        #print(tree.heap)


        if not currentState in visited:
            visited.append(currentState)
            
            if(problem.isGoalState(currentState)):
                #if we find the goal state , problem is solved and path is returned
                return path

            for node in problem.getSuccessors(currentState):
                if not node[0] in visited:
                    #calculating heuristic function : h = actual cost to the current node + predicted cost to the goal node
                    # actual cost = cost of the current node + cost of the edge connecting him to the examined successor node
                    #predicted cost = heuristic function result
                    h = cost + node[2] + heuristic(node[0], problem)
                    tree.push((node[0], path + [node[1]], cost + node[2]), h)
                    #print("next", node[0], cost + node[2], h , heuristic(node[0], problem)) debugging 

    #If tree is empty , that means that there was no goal state found 
    #during the iteration 
    return False
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
