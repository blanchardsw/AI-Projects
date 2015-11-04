################################################
##############Stephen Blanchard   ##############
##############swb4062             ##############
##############CMPS 420 - Fall 2015##############
##############Homework - 1        ##############
################################################

#Import util for Stack, Queue, PriorityQueue
import util
#Import searchTestClasses for its graph building and comparisons
import searchTestClasses

#A graph_text is what the SearchGraph function uses to build a graph in searchTestClasses
#It's formatted as a text string that gives a start state, a goal and then each line after that is
#broken up by <current state> <action> <resulting state> <cost>.  When this is passed to GraphSearch,
#It's read line by line and then split by spaces to grab each field.
graph_text = """start_state: S
goal_states: Z
S S->a a 20
S S->c c 50
S S->b b 70
a a->b b 40
a a->d d 80
b b->c c 15
b b->d d 30
c c->e e 55
c c->h h 110
d d->e e 10
d d->f f 40
e e->f f 20
e e->g g 25
e e->h h 30
f f->g g 10
f f->Z Z 70
g g->h h 20
g g->Z Z 50
h h->Z Z 20"""

#This search item is an object of the GraphSearch class.  It will allow me to pass that graph above so that
#I can do comparisons and traversals on the nodes and edges.
search = searchTestClasses.GraphSearch(graph_text)

#Then here, I do a depth first search on the graph above.
def DFS (search):
	#The fringe will be a stack, as we discussed in class
	fringe=util.Stack()
	#The fringe has to know the current state, the actions taken so far and the nodes we've visited.
	#Of course, the current state is the start for now and we haven't taken any actions or visited any nodes, so those are empty.
	fringe.push( (search.getStartState(), [],[]) )

	#Then we try each path until the graph is exhausted
	while fringe.isEmpty() == False:
    
		#Pop the stack to grab the current node, the solution thus far and all visited nodes
		currentNode, solution, visited = fringe.pop()
	
		#Then, we grab the successors of the current node
		successors = search.getSuccessors(currentNode)
		
		#We look at those successors for their location, their direction and the cost of each move
		for location, direction, cost in successors:
			#If the current location has not been visited
			if location not in visited:
				#Check to see if it's the goal
				if search.isGoalState(location):
					#If it is, we break out of the loop and add the location to the solution thus far
					solution = solution + [direction]
					break
				#But if not, we put it on the stack so that we can update the solution and the list of visited nodes and continue checking
				fringe.push((location, solution + [direction], visited + [currentNode]))


	print("For depth first search, the path taken is as follows:\n")
	print(solution)
	print("With a total path cost of: ", search.getCostOfActions(solution))
	print("\n")

def BFS (search):
	#This time, the fringe will be a queue, as we discussed in class
    fringe = util.Queue()
	#The fringe has to know the current state, the actions taken so far and the nodes we've visited.
	#Of course, the current state is the start for now and we haven't taken any actions or visited any nodes, so those are empty.
    fringe.push( (search.getStartState(), []) )

    visited = []
	#once again, we go until there's nowhere else to go or a goal is reached.
    while fringe.isEmpty() == False:
		#pop the queue to get the current node and the solution thus far
        currentNode, solution = fringe.pop()
		#Get the successors of the current node
        successors = search.getSuccessors(currentNode)
		#check the location, the direction and cost of the successors
        for location, direction, cost in successors:
			#If we haven't visited the current location
            if location not in visited:
				#Check to see if we're at the goal
                if search.isGoalState(location):
					#If so, update the solution and break out of the loop
                    solution = solution + [direction]
                    break
				#Otherwise, update the solution and the visited nodes thus far
                fringe.push((location, solution + [direction]))
                visited.append(location)
				
    print("For breadth first search, the path taken is as follows:\n")
    print(solution)
    print("With a total path cost of: ", search.getCostOfActions(solution))
    print("\n")
	
def UCS(problem):
	#for uniform cost search, we discussed using a priority queue in class so that each action can have a cost to it and is sorted in the queue
	#This should cause the function to choose the cheapest path
    fringe = util.PriorityQueue()
	#So we start the queue off with just the start state, blank solution, blank visited and no cost
    fringe.push( (problem.getStartState(), []), 0)
    visited = []

	#traverse until there's nothing left or we reach a goal
    while fringe.isEmpty() == False:
		#Grab the current node and the solution from the queue
        currentNode, solution = fringe.pop()
		#check and see if we're at the goal
        if problem.isGoalState(currentNode):
			#if so, break out
            break
		#if not, add it to our visited list
        visited.append(currentNode)
		
		#then we grab the successors of the current node
        successors = search.getSuccessors(currentNode)
		#look at the location, direction, cost as before
        for location, direction, cost in successors:
			#if the current location has not been visited
            if location not in visited:
				#then we create a new solution
                newSolution = solution + [direction]
				#and push it onto the queue along with the cost of the solution so far.  The cost of this solution will be weighed against other solutions
				#and prioritized in the queue
                fringe.push((location, newSolution), problem.getCostOfActions(newSolution))

    print("For breadth first search, the path taken is as follows:\n")
    print(solution)
    print("With a total path cost of: ", search.getCostOfActions(solution))
    print("\n")
	
#call each function for the search algorithms
print("\n")
DFS(search)
print("\n")
BFS(search)
print("\n")
UCS(search)