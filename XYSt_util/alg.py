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
    global heuristics_called
    heuristics_called=True
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
                future_game_obj.put(i+1,j+1,Space.BLACK)
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
                future_game_obj.put(i+1,j+1,Space.WHITE)
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
    '''minimax function wrapper for further integration into the code + iterative deepening work'''
    d=dict()
    #iterate through the entire game field, calculate minimax values for each position, return the highest one possible
    for i in range(game_obj._x):
        for j in range(game_obj._y):
            if game_obj.get_value(i+1,j+1)!=0:
                continue
            future_game_obj=copy.deepcopy(game_obj)
            future_game_obj.put(i+1,j+1,Space.BLACK)
            d[(i+1,j+1)]=minimax(future_game_obj,i+1,j+1,depth=depth,black=False)
    #pick the highest value coordinate
    max_val=-inf
    final_x=0
    final_y=0
    for i in d.keys():
        if d[i]>max_val:
            max_val=d[i]
            final_x,final_y=i
    return (final_x,final_y)

def alg_minimax_process(game_obj:game.Grid,best_coords:list):
    '''An iterative deepening thread that should be able to terminate whenever needed'''
    depth=0
    while True:
        copied_game_obj=copy.deepcopy(game_obj)
        global heuristics_called
        heuristics_called=False
        best_x,best_y=alg_minimax(copied_game_obj,depth)
        best_coords[0]=best_x
        best_coords[1]=best_y
        depth+=1
        if not heuristics_called:
            return None

def alg_minimax_timed(game_obj:game.Grid,decision_max_seconds):
    '''Wrapper of a wrapper of a minimax algorithm for the purposes of iterative deepening'''
    seconds=decision_max_seconds

    t_end=time.time()+seconds
    depth=0
    best_x=0
    best_y=0
    global heuristics_called
    heuristics_called=False
    best_x,best_y=alg_minimax(game_obj,depth)
    depth+=1
    manager=multiprocessing.Manager()
    best_coords=manager.list([best_x,best_y])
    t=multiprocessing.Process(target=alg_minimax_process,args=(game_obj,best_coords))
    t.start()
    t.join(seconds)
    if t.is_alive():
        t.terminate()
    best_x=best_coords[0]
    best_y=best_coords[1]
    return best_x,best_y