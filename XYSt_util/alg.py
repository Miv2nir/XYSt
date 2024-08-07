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
    raise NotImplemented

def minimax(game_obj:game.Grid,x,y,alpha=-inf,beta=inf,depth=inf,black=True):
    raise NotImplemented

def alg_minimax(game_obj:game.Grid,depth=inf):
    raise NotImplemented

def alg_minimax_process(game_obj:game.Grid,best_coords:list):
    raise NotImplemented

def alg_minimax_timed(game_obj:game.Grid,decision_max_seconds):
    raise NotImplemented