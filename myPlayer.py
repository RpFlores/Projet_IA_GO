# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''

import time
import Goban
from random import choice
from playerInterface import *
from mctsClass import *
from MCTSsearch import *


class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and 
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None

    def currentColor(self):
        return self._mycolor

    def getPlayerName(self):
        return "Random Player"

    def intersection(self,lst1, lst2): 
        lst3 = [value for value in lst1 if value in lst2] 
        return lst3 

    def ouverture(self,legal_moves):
        ouvertures = ['C9', 'C8', 'B7',  'A7', 'G9', 'G8', 'H7', 'J7',
        'A3', 'B3', 'C2', 'C1', 'G1', 'G2', 'H3', 'J3']
        moves= []
        for m in ouvertures:
            moves.append(self._board.name_to_flat(m))
        return self.intersection(moves, legal_moves)

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS" 
        moves = self._board.legal_moves() # Dont use weak_legal_moves() here!

        ouvertures = self.ouverture(moves)
        if len(ouvertures)>=1:
            print("ouvertures possibles :")
            print(ouvertures)
            move = ouvertures.pop()
        else :  
        

            # alpha beta
            move = chooseMove(self, self._mycolor, 2)

            #Décommenter pour faire tourner monte carlo:

            #root = nodeMCTS(self._board, self._mycolor)
            #mcts = MonteCarloTreeSearch(root)
            #move =  mcts.best_action(100)

        self._board.push(move)

        # New here: allows to consider internal representations of moves
        print("I am playing ", self._board.move_to_str(move))
        print("My current board :")
        self._board.prettyPrint()
        # move is an internal representation. To communicate with the interface I need to change if to a string
        return Goban.Board.flat_to_name(move) 
    
    def heuristic2(self, move, move_color):
        
        cpt = 0
        if(move_color != self._mycolor):
            return cpt
        
        nbEmpty = 0
        nbSameColor = 0
        i = self._board._neighborsEntries[move]
        while self._board._neighbors[i] != -1:
            n = self._board._neighbors[i]
            if  n == Goban.Board._EMPTY:
                nbEmpty += 1
            elif n == self._mycolor:
                nbSameColor += 1
            i += 1
        
        
        if(nbEmpty == i):
                cpt = -2
        elif(nbSameColor == i):
                cpt = -1
        elif(nbSameColor != 0):
                cpt += 1
        return cpt*2


    def heuristic(self):
        score = 0 
        (black, white) = (self._board._nbBLACK, self._board._nbWHITE)
        if(self._mycolor == Goban.Board._WHITE):
            score = white - black
            return score
        else:
            score = black - white
            return score
        return score

    def MinMax(self, depth, player):
        b = self._board
        if(b.is_game_over() or depth == 0):
            return self.heuristic()  
        to_ret = 0
        if(player):
            to_ret = -10000
        else:
            to_ret = +10000
        for m in b.legal_moves():
            b.push(m)
            res = self.MinMax(depth-1, Goban.Board.flip(player))
            b.pop()
            if(player and res > to_ret):
                to_ret = res
            elif(Goban.Board.flip(player) and res < to_ret):
                to_ret = res
        return to_ret

    def playOpponentMove(self, move):
        print("Opponent played ", move) # New here
        # the board needs an internal represetation to push the move.  Not a string
        self._board.push(Goban.Board.name_to_flat(move)) 

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")

    def ABminimax(self, player, depth, alpha, beta, move):
        if (depth == 0 or self._board.is_game_over()):
            return self.heuristic2(move, self._mycolor) + self.heuristic()

        if(player == self._mycolor):
            best = -10000
            moves = self._board.legal_moves()
            for move in moves:
                self._board.push(move)
                player = self._opponent;
                val = self.ABminimax(Goban.Board.flip(player), depth-1, alpha, beta, move)
                self._board.pop()
                best = max(best, val)
                alpha = max(alpha, best)

                if(beta <= alpha):
                    break
            return best
        elif(player == self._opponent):
            best = 10000
            moves = self._board.legal_moves()
            for move in moves:
                self._board.push(move)
                val = self.ABminimax(Goban.Board.flip(player), depth-1, alpha, beta, move)
                self._board.pop()
                best = min(best, val)
                beta = min(alpha, best)

                if(beta <= alpha):
                    break
            return best
        return 0

def chooseMove(self, player, depth): #chooses the best first move by getting the min max value of each tree generated after the first move
    #player = self._myColor
    print("choose move")
    if(self._board.is_game_over()):
        return Goban.Board.name_to_flat('PASS')
    to_ret_val = -10000
    to_ret = []
    moves = self._board.legal_moves()
    if (len(moves) == 1):
        return -1
    for move in moves:
        self._board.push(move)
        res = self.ABminimax(Goban.Board.flip(player), depth, -10000, 10000, move)
        self._board.pop()
        if(res > to_ret_val):
            to_ret_val = res
            to_ret.clear
            if(move != -1):
                to_ret.append(move)
        elif(res == to_ret_val and move != -1):
            to_ret.append(move)
    return choice(to_ret)

    

