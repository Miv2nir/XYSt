from XYSt_util import game
from XYSt_util.names import Names,Space

import random,copy
from math import inf
import threading,multiprocessing,time

def if_terminal(game_obj:game.Grid):
    thought=game_obj.evaluate()
    if thought==Names.WHITE.name or thought==Names.BLACK.name or thought==True:
        return True
    return False

def terminal_calc(game_obj:game.Grid):
    thought=game_obj.evaluate()
    if thought==Names.WHITE.name:
        return -1
    elif thought==Names.BLACK.name:
        return 1
    else:
        return 0

def cut_off_evaluation(game_obj:game.Grid):
    return game_obj.evaluate_heuristics()

def minimax(game_obj:game.Grid,x,y,alpha=-inf,beta=inf,depth=inf,black=True):
    #here we go again
    if if_terminal(game_obj):
        return terminal_calc(game_obj)

    #depth check
    if depth<=0:
        return cut_off_evaluation(game_obj)
    #the algorithm itself
    #black is always the maximizing player 
    if black:
        maxEval= -inf
        for i in range(game_obj._x):
            break_flag=False
            for j in range(game_obj._y):
                if game_obj.get_value(i+1,j+1)!=0: #if it happens like that then there is a piece on this position already
                    continue
                #copy the game field
                future_game_obj=copy.deepcopy(game_obj)
                future_game_obj.decrease(i+1,j+1)
                #recursion time
                eval=minimax(future_game_obj,i+1,j+1,alpha,beta,depth-1,False)
                maxEval=max(eval,maxEval)
                alpha=max(alpha,eval)
                if beta <= alpha:
                    break_flag=True
                    break
            if break_flag:
                break
        return maxEval
    else: #evaluating the player
        minEval=inf
        for i in range(game_obj._x):
            break_flag=False
            for j in range(game_obj._y):
                if game_obj.get_value(i+1,j+1)!=0: #if it happens like that then there is a piece on this position already
                    continue
                #copy the game field
                future_game_obj=copy.deepcopy(game_obj)
                future_game_obj.decrease(i+1,j+1)
                #more recursion!!!!!!
                eval=minimax(future_game_obj,i+1,j+1,alpha,beta,depth-1,True)
                minEval=min(eval,minEval)
                beta=min(beta,eval)
                beta=min(beta,eval)
                if beta<=alpha:
                    break_flag=True
                    break
            if break_flag:
                break
        return minEval


def alg_minimax(game_obj:game.Grid,depth=inf):
    raise NotImplemented

def alg_minimax_process(game_obj:game.Grid,best_coords:list):
    raise NotImplemented

def alg_minimax_timed(game_obj:game.Grid,decision_max_seconds):
    raise NotImplemented