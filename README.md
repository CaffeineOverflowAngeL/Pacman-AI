# <b> Pacman Artificial Intelligence Python project for UC Berkeley CS188 Intro to AI <b>
  [Pac-Man Projects UC Berkeley](http://ai.berkeley.edu/project_overview.html)

  ## Project 1: Search:
  [Search](http://ai.berkeley.edu/search.html)

* Depth-First Search (DFS): Graph search that avoids expanding already visited states. Fringe implemented via stack.
  
* Breadth-First Search (BFS): Graph search that avoids expanding already visited states. Fringe implemented via queue.
  
* Uniform Cost Search (UCS): Graph search that avoids expanding already visited states. Fringe implemented via Priority Queue.
  
* A* Search: uses Manhattan distance heuristic to find optimal solution
  
* CornersProblem: Search problem and heuristic for pacman to reach all active corner dots on board.
  
* FoodSearchProblem: Search problem and heuristic for pacman to eat all active dots on board.
  

## Project 2: Multiagents:
[Multiagents](http://ai.berkeley.edu/multiagent.html)

* ReflexAgent: A reflex agent uses an evaluation function (aka heuristic function) to estimate the value of an action using the current * game state. The Reflex Agent considered 
  
* food locations and ghost locations, using reciprocals of distances as features.
  
* MinimaxAgent: A minimax agent is implemented using a minimax tree with multiple min layers (one for each ghost) for every max layer. The agent uses an evaluation function that evaluates states, and can sometimes choose to kill itself when believed this is the best choice.
  
* AlphaBetaAgent: An alpha beta agent uses alpha-beta pruning to explore the minimax tree.
  
* Expectimax: The expectimax pacman makes decisions using the expected value
