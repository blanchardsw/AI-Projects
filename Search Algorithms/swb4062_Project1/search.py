#! /usr/bin/env python2
################################################
##############Stephen Blanchard   ##############
##############swb4062             ##############
##############CMPS 420 - Fall 2015##############
##############Project 1           ##############
################################################

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
    #The fringe will be a stack, as we discussed in class
	fringe=util.Stack()
	#The fringe has to know the current state, the actions taken so far and the nodes we've visited.
	#Of course, the current state is the start for now and we haven't taken any actions or visited any nodes, so those are empty.
	fringe.push( (problem.getStartState(), [],[]) )

	#Then we try each path until the graph is exhausted
	while fringe.isEmpty() == False:

		#Pop the stack to grab the current node, the solution thus far and all visited nodes
		currentNode, solution, visited = fringe.pop()

		#Then, we grab the successors of the current node
		successors = problem.getSuccessors(currentNode)

		#We look at those successors for their location, their direction and the cost of each move
		for location, direction, cost in successors:
			#If the current location has not been visited
			if location not in visited:
				#Check to see if it's the goal
				if problem.isGoalState(location):
					#If it is, we update the solution and return it
					solution = solution + [direction]
					return solution
				#But if not, we put it on the stack so that we can update the solution and the list of visited nodes and continue checking
				fringe.push((location, solution + [direction], visited + [currentNode]))

def breadthFirstSearch(problem):
    #This time, the fringe will be a queue, as we discussed in class
    fringe = util.Queue()
	#The fringe has to know the current state, the actions taken so far and the nodes we've visited.
	#Of course, the current state is the start for now and we haven't taken any actions or visited any nodes, so those are empty.
    fringe.push( (problem.getStartState(), []) )

    visited = []
	#once again, we go until there's nowhere else to go or a goal is reached.
    while fringe.isEmpty() == False:
		#pop the queue to get the current node and the solution thus far
        currentNode, solution = fringe.pop()
		#Get the successors of the current node
        successors = problem.getSuccessors(currentNode)
		#check the location, the direction and cost of the successors
        for location, direction, cost in successors:
			#If we haven't visited the current location
            if location not in visited:
				#Check to see if we're at the goal
                if problem.isGoalState(location):
					#If so, update the solution and return it
                    solution = solution + [direction]
                    return solution
				#Otherwise, update the solution and the visited nodes thus far
                fringe.push((location, solution + [direction]))
                visited.append(location)

def uniformCostSearch(problem):
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
			#if so, return the solution
            return solution
		#if not, add it to our visited list
        visited.append(currentNode)

		#then we grab the successors of the current node
        successors = problem.getSuccessors(currentNode)
		#look at the location, direction, cost as before
        for location, direction, cost in successors:
			#if the current location has not been visited
            if location not in visited:
				#then we create a new solution
                newSolution = solution + [direction]
				#and push it onto the queue along with the cost of the solution so far.  The cost of this solution will be weighed against other solutions
				#and prioritized in the queue
                fringe.push((location, newSolution), problem.getCostOfActions(newSolution))

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

#aStar is just like it was in our homework except we can use a return function instead of printing out the path
def aStarSearch(problem, heuristic=nullHeuristic):
    #again we store the visited nodes separately
    visited = []
    #grab the start state and make a reference variable for the problem labeled as goal just to easily
    #recognize when it's being used by the heuristic in a different way from the rest of the function.
    startState = problem.getStartState()
    goal = problem

    #As discussed in class, fringe is a PriorityQueue
    fringe = util.PriorityQueue()
    #Put the start state, solution, and backwards cost (g(n)) in the queue along with the estimated cost to the goal
    fringe.push((startState, [], 0), heuristic(startState, goal))

    #Pop the fringe until there's nothing left
    while fringe.isEmpty() == False:
        #grab the current node, solution and the cost thus far
        currentNode, solution, currentCost = fringe.pop()
        #If we're at the goal, stop
        if problem.isGoalState(currentNode):
            return solution
        #Otherwise, we mark the node as visited
        visited.append(currentNode)
        successors = problem.getSuccessors(currentNode)
        #We then calculate a new solution based on what we know about our current point
        #as well as what it will take us to reach the goal from where we are.
        for location, direction, cost in successors:
            if location not in visited:
                #find our g(n) and h(n)
                gn = currentCost + cost
                hn = heuristic(location, goal)
                newSolution = solution + [direction]
                #aStar is not greedy so g(n) is used.  Here, our distance, f(n),  is g(n)+h(n)
                distance = gn + hn
                #Then we record that new solution plus the distance
                fringe.push( (location, newSolution, gn), distance)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
