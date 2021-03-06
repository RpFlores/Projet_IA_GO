import numpy as np
import Goban
from collections import defaultdict
from abc import ABC, abstractmethod
import sys
import time
import copy


class MonteCarloTreeSearchNode(ABC):

    def __init__(self, state1, color, parent=None):
        
        self.state = state1
        self.parent = parent
        self.children = [] #list of child nodes
#======================CHANGED====================================================#
        self.move = None
        self.color = color
        
#=================================================================================#

    @property
    @abstractmethod
    def untried_actions(self):
        """

        Returns
        -------
        list of legal moves

        """
        pass

    @property
    @abstractmethod
    def q(self):
        pass

    @property
    @abstractmethod
    def n(self):
        pass

    @abstractmethod
    def expand(self):
        pass

    @abstractmethod
    def is_terminal_node(self):
        pass

    @abstractmethod
    def rollout(self):
        pass

    @abstractmethod
    def backpropagate(self, reward):
        pass

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, c_param=1.4):
        choices_weights = [
            (c.q / c.n) + c_param * np.sqrt((2 * np.log(self.n) / c.n))
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):        
        return possible_moves[np.random.randint(len(possible_moves))]
    
    def getColor(self):
        return self.color


class nodeMCTS(MonteCarloTreeSearchNode):

    def __init__(self, state, color, parent=None):
        super().__init__(state, color, parent)
        self._number_of_visits = 0.
        self._results = defaultdict(int)
        self._untried_actions = None

    @property
    def untried_actions(self):
        if self._untried_actions is None:
#======================CHANGED====================================================#
            self._untried_actions = self.state.legal_moves()
#=================================================================================#
        return self._untried_actions

    @property
    def q(self):
#======================CHANGED====================================================#
        wins = self._results[self.getColor()]
        loses = self._results[Goban.Board.flip(self.getColor())]
#=================================================================================#
        return wins - loses

    @property
    def n(self):
        return self._number_of_visits

    def expand(self):
        if(len(self.untried_actions) <= 1):
            action = self.untried_actions.pop()
        else:
            action = self.untried_actions.pop()
            action = self.untried_actions.pop()
        self.state.push(action)

#======================CHANGED====================================================#
        #creates new node with a copy of the board with the new random move and returns it
        child_node = nodeMCTS(
        copy.deepcopy(self.state), self.color, parent=self)
        child_node.correspondingMove(action)
        self.children.append(child_node)
        self.state.pop()
#=================================================================================#

        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    def rollout(self):
        current_rollout_state = self.state
#======================CHANGED====================================================#
        count = 0
        while ( not current_rollout_state.is_game_over() ):
            possible_moves = current_rollout_state.legal_moves()
            action = self.rollout_policy(possible_moves)
            current_rollout_state.push(action)

            count += 1
        result = current_rollout_state.result() # result is a string with the score
        while(count > 0): #we pop the moves  we pushed
            count = count-1
            current_rollout_state.pop()
        return self.resultToInt(result) #we return the winner (0 1 2) depending on the score.
#=================================================================================#


    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

#============= CHANGED ================================#
    #put the corresponding move to the node in move
    def correspondingMove(self, move): 
        self.move = move

    #returns the move corresponding to the node
    def getCorrespondingMove(self): 
        return self.move
    

    #transforms the score "1-0" to 1 (white wins)
    #transforms the score "0-1" to -1 (black wins)
    #transforms the score "1/2-1/2" to 0 (draw)
    def resultToInt(self, result): 
        result_to_return = 0
        if result == "1-0":
            result_to_return = 1
        elif result == "0-1":
            result_to_return = 2
        else:
            result_to_return = 0
        
        return result_to_return
        


    
    

#======================================================#   

        

    
