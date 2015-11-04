################################################
##############Stephen Blanchard   ##############
##############swb4062             ##############
##############CMPS 420 - Fall 2015##############
##############Homework - 2        ##############
################################################

#Import util for Stack, Queue, PriorityQueue
import util
#Import searchTestClasses for its graph building and comparisons
import searchTestClasses
import math
#A graph_text is what the SearchGraph function uses to build a graph in searchTestClasses
#It's formatted as a text string that gives a start state, a goal and then each line after that is
#broken up by <current state> <action> <resulting state> <cost>.  When this is passed to GraphSearch,
#It's read line by line and then split by spaces to grab each field.
graph_text = """start_state: 0,0
goal_states: 125,5
0,0 H->a 15,-10 20
0,0 H->c 45,5 50
0,0 H->b 55,-5 70
15,-10 a->b 55,-5 40
15,-10 a->d 80,-5 80
55,-5 b->c 45,5 15
55,-5 b->d 80,-5 30
45,5 c->e 90,0 55
45,5 c->h 115,10 110
80,-5 d->e 90,0 10
80,-5 d->f 105,-3 40
90,0 e->f 105,-3 20
90,0 e->g 105,-5 25
90,0 e->h 115,10 30
105,-3 f->g 105,-5 10
105,-3 f->L 125,5 70
105,-5 g->h 115,10 20
105,-5 g->L 125,5 50
115,10 h->L 125,5 20"""

#This search item is an object of the GraphSearch class.  It will allow me to pass that graph above so that
#I can do comparisons and traversals on the nodes and edges.
search = searchTestClasses.GraphSearch(graph_text)

#the manhattan distance function determined by |xi-xk|+|yi-yk|
def Manhattan(currentState, goalState):
    #I had to do some conversions and splitting of the graph text due to the way it was being presented.
    current = str(currentState)
    currentSplit = current.split(',')
    xi = int(currentSplit[0])
    yi = int(currentSplit[1])
    goal = tuple(goalState)
    goalSplit = goal[0].split(',')
    xk = int(goalSplit[0])
    yk = int(goalSplit[1])

    distance = abs(xi - xk) + abs(yi - yk)
    return distance

#the biolab distance function calculated by max(xi-xk, yi-yk)
def BioLab (currentState,goalState):
    current = str(currentState)
    currentSplit = current.split(',')
    xi = int(currentSplit[0])
    yi = int(currentSplit[1])
    goal = tuple(goalState)
    goalSplit = goal[0].split(',')
    xk = int(goalSplit[0])
    yk = int(goalSplit[1])

    distance = max(xi-xk, yi-yk)
    return distance

#greedy algorithm does not care about the cost of its current state, only the estimate to the goal
def greedy(search, estimate):
    visited = []
    startState = search.getStartState()
    goal = search.goals
    #much like the blind searches, we track the current state and the solution, but also add in the heuristic estimate
    fringe = util.PriorityQueue()
    fringe.push((startState, []), estimate(startState, goal))

    while fringe.isEmpty() == False:
        currentNode, solution = fringe.pop()
        #and here, if we reach the goal, we return the solution but also the cost of that solution
        if search.isGoalState(currentNode):
            return solution, search.getCostOfActions(solution)

        visited.append(currentNode)
        successors = search.getSuccessors(currentNode)

        for location, direction, cost in successors:
            if location not in visited:
                newSolution = solution + [direction]
                #This is where the main difference is compared to aStar. f(n) = h(n)
                #The distance only concerns the heuristic or the estimate due to g(n) = 0
                distance = estimate(location, goal)
                fringe.push( (location, newSolution), distance)

#With aStar, we use essentially the same algorithm except this time we take into account
#The cost of getting to our current position to better estimate the distance to the goal
def aStar(search, estimate):
    visited = []
    startState = search.getStartState()
    goal = search.goals

    fringe = util.PriorityQueue()
    fringe.push((startState, []), estimate(startState, goal))

    while fringe.isEmpty() == False:
        currentNode, solution = fringe.pop()

        if search.isGoalState(currentNode):
            return solution, search.getCostOfActions(solution)

        visited.append(currentNode)
        successors = search.getSuccessors(currentNode)
        #aStar is essentially the same as the greedy algorithm, except for how we track the distance or cost
        for location, direction, cost in successors:
            if location not in visited:
                newSolution = solution + [direction]
                #So here with aStar we consider f(n) = g(n) + h(n)
                distance = search.getCostOfActions(newSolution) + estimate(location, goal)
                fringe.push( (location, newSolution), distance)


print"Using the greedy algorithm with Manhattan distance, we get a path of: ",greedy(search, Manhattan)
print"Using the greedy algorithm with BioLab distance, we get a path of: ",greedy(search, BioLab)
print"Using the A* algorithm with Manhattan distance, we get a path of: ",aStar(search, Manhattan)
print"Using the A* algorithm with BioLab distance, we get a path of: ",aStar(search, BioLab)
