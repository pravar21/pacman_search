# pacmanAgents.py
# ---------------
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

from pacman import Directions
from game import Agent
from heuristics import scoreEvaluation
import random

class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0,len(actions)-1)]

class GreedyAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        # get all the successor state for these actions
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(scoreEvaluation(state), action) for state, action in successors]
        # get best choice
        bestScore = max(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random action from the list of the best actions
        return random.choice(bestActions)

class BFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):

        frontier = []
        stateMetadata = {}

        legal = state.getLegalPacmanActions()
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal]
        for successor in successors:
            stateMetadata[successor[0]] = successor[1]
            frontier.append((successor[0],scoreEvaluation(successor[0])))

        while frontier:
            node = frontier[0][0]
            frontier = frontier[1:] #frontier acts as FIFO structure

            if node.isWin():
                return stateMetadata[node]

            elif node.isLose():
                continue

            legal = node.getLegalPacmanActions()
            successors = [node.generatePacmanSuccessor(action) for action in legal]

            for successor in successors:
                if successor is None:
                    for frontierNode in frontier:
                        if frontierNode[0].isWin():
                            return stateMetadata[frontierNode]
                        elif frontierNode[0].isLose():
                            frontier.remove(frontierNode)
                    return stateMetadata[max(frontier,key=lambda x : x[1])[0]]
                stateMetadata[successor] = stateMetadata[node]
                frontier.append((successor,scoreEvaluation(successor)))
        return Directions.STOP

class DFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        frontier = []
        stateMetadata = {}

        legal = state.getLegalPacmanActions()
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal]
        for successor in successors:
            stateMetadata[successor[0]] = successor[1]
            frontier.append((successor[0], scoreEvaluation(successor[0])))

        while frontier:
            node = frontier[0][0]
            frontier = frontier[:len(frontier)-1] #frontier acts as LIFO

            if node.isWin():
                return stateMetadata[node]

            elif node.isLose():
                continue

            legal = node.getLegalPacmanActions()
            successors = [node.generatePacmanSuccessor(action) for action in legal]

            for successor in successors:
                if successor is None:
                    for frontierNode in frontier:
                        if frontierNode[0].isWin():
                            return stateMetadata[frontierNode]
                        elif frontierNode[0].isLose():
                            frontier.remove(frontierNode)
                    return stateMetadata[max(frontier, key=lambda x : x[1])[0]]
                stateMetadata[successor] = stateMetadata[node]
                frontier.append((successor, scoreEvaluation(successor)))
        return Directions.STOP

class AStarAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # Computes f(x) = g(x) + h(x)
    def fOfXEvaluation(self,state,stateMetadata,root):
        return int(stateMetadata[state][1]) -(scoreEvaluation(state) - scoreEvaluation(root));

    # GetAction Function: Called with every frame
    def getAction(self, state):
        frontier = []
        stateMetadata = {}
        depth = 0
        legal = state.getLegalPacmanActions()
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal]
        for successor in successors:
            stateMetadata[successor[0]] = (successor[1],depth) #key = state , value = (initialAction,depthOfNode)
            frontier.append((successor[0], self.fOfXEvaluation(successor[0], stateMetadata, state)))

        while frontier:
            tuple = min(frontier,key= lambda x : x[1])
            node = tuple[0]
            frontier.remove(tuple)

            if node.isWin():
                return stateMetadata[node][0]

            elif node.isLose():
                continue

            legal = node.getLegalPacmanActions()
            successors = [node.generatePacmanSuccessor(action) for action in legal]

            for successor in successors:
                if successor is None:
                    for frontierNode in frontier:
                        if frontierNode[0].isWin():
                            return stateMetadata[frontierNode][0]
                        elif frontierNode[0].isLose():
                            frontier.remove(frontierNode)
                    return stateMetadata[min(frontier,key= lambda x : x[1])[0]][0]
                stateMetadata[successor] = (stateMetadata[node][0],stateMetadata[node][1] + 1)
                frontier.append((successor, self.fOfXEvaluation(successor, stateMetadata, state)))
        return Directions.STOP
