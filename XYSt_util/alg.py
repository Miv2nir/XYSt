from XYSt_util import game
from XYSt_util.names import Names,Space

import random,copy
from math import inf
import threading,multiprocessing,time
import numpy as np

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
                if beta<=alpha:
                    break_flag=True
                    break
            if break_flag:
                break
        return minEval

def availability_check(game_obj:game.Grid,x,y):
    if game_obj.get_piece(x,y)==Space.EMPTY and x>0 and x<=game_obj._x and y>0 and y<=game_obj._y:
        return True
    return False

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
            print(d)
    
    if max(d.values())==min(d.values()):
        substitute=(0,0)
        #the algorithm in this case doesnt care as to where to set a peg so let's set it near a player's one
        for i in range(game_obj._x):
            break_flag=False
            for j in range(game_obj._y):
                x=i+1
                y=j+1
                if game_obj.get_piece(x,y)==Space.WHITE: #found it
                    if availability_check(game_obj,x-1,y): #left
                        substitute=(x-1,y)
                        break_flag=True
                        break
                    elif availability_check(game_obj,x,y-1): #up
                        substitute=(x,y-1)
                        break_flag=True
                        break
                    elif availability_check(game_obj,x+1,y): #right
                        substitute=(x+1,y)
                        break_flag=True
                        break
                    elif availability_check(game_obj,x,y+1): #down
                        substitute=(x,y+1)
                        break_flag=True
                        break
                    elif availability_check(game_obj,x-1,y-1): #left up
                        substitute=(x-1,y-1)
                        break_flag=True
                        break
                    elif availability_check(game_obj,x-1,y+1): #left down
                        substitute=(x-1,y+1)
                        break_flag=True
                        break
                    elif availability_check(game_obj,x+1,y-1): #right up
                        substitute=(x+1,y-1)
                        break_flag=True
                        break
                    elif availability_check(game_obj,x+1,y+1): #right down
                        substitute=(x+1,y+1)
                        break_flag=True
                        break
            if break_flag:
                break
        if substitute!=(0,0):
            return substitute
                        
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

def check_completion(game_obj:game.Grid,x,y,value,dir_x,dir_y,target_moves):
    '''Rewrite of game_obj._check_heuristics() to work with improved_evaluation.
    Checks whether the line can be completed in a given direction (returns 0 or 1 integer)'''
    #x,y - starter coordinates
    #check if a spot is already occupied or not
    if game_obj.is_out_of_bounds(x,y):
        return 0
    if game_obj.get_piece(x,y).value!=0: #double check
        return 0
    length=1
    zero_count=1
    while length<game_obj.win_white:
        x+=dir_x
        y+=dir_y
        if game_obj.is_out_of_bounds(x,y):
            return 0
        if game_obj.get_piece(x,y).value!=value and game_obj.get_piece(x,y)!=0:
            return 0
        length+=1
        if game_obj.get_piece(x,y)==0:
            zero_count+=1
    if zero_count>target_moves:
        return 0
    return 1

def check_completion_all_directions(game_obj,x,y,value,win_length):
    # x+1 y = right
    r=check_completion(game_obj,x,y,value=value,dir_x=1,dir_y=0,target_moves=win_length)
    # x+1 y+1 = down right
    dr=check_completion(game_obj,x,y,value=value,dir_x=1,dir_y=1,target_moves=win_length)
    # x y+1 = down
    d=check_completion(game_obj,x,y,value=value,dir_x=0,dir_y=1,target_moves=win_length)
    # x-1 y+1 = down left
    dl=check_completion(game_obj,x,y,value=value,dir_x=-1,dir_y=1,target_moves=win_length)
    # x-1 y = left
    l=check_completion(game_obj,x,y,value=value,dir_x=-1,dir_y=0,target_moves=win_length)
    # x-1 y-1 = up left
    ul=check_completion(game_obj,x,y,value=value,dir_x=-1,dir_y=-1,target_moves=win_length)
    # x y-1 = up
    u=check_completion(game_obj,x,y,value=value,dir_x=0,dir_y=-1,target_moves=win_length)
    # x+1 y-1 = up right
    ur=check_completion(game_obj,x,y,value=value,dir_x=1,dir_y=-1,target_moves=win_length)
    #score time
    return sum([r,dr,d,dl,l,ul,u,ur])

def improved_eval(game_obj:game.Grid,win_length:int,value=Space.BLACK.value):
    #rough algo description:
    eval_grid=[[0 for col in range(game_obj._x)] for row in range(game_obj._y)]
    #For every point:
    calc_length=game_obj.win_white-win_length
    for i in range(game_obj._x):
        for j in range(game_obj._y):
            #if point is zero:
            if game_obj._grid[j][i]==0:
                x=i+1
                y=j+1
                #calculate how many ways are there to reach a victory in x moves
                #similar to game_obj.evaluate_heuristics():
                eval_grid[j][i]=check_completion_all_directions(game_obj,x,y,value,win_length)

            #how did the coefficients change after one's move in P.
            #calculated coefficients to be added up, multiplied by k^(-1) where k=10
            #check in 3 stages, P has a white peg, a black peg or is empty
            #pick a point with the largest difference
    return eval_grid

def alg_improved(game_obj:game.Grid,value,k=10):
    '''New version of a linear evaluation function algorithm previously used as part of a minimax process'''
    score_matrix=[[0 for col in range(game_obj._x)] for row in range(game_obj._y)]
    for a in range(1,game_obj.win_black+1):
        intermediate_score_matrix=improved_eval(game_obj,a,value)
        for i in range(game_obj._x):
            for j in range(game_obj._y):
                intermediate_score_matrix[j][i]*=(k**(game_obj.win_black-a))
                score_matrix[j][i]+=intermediate_score_matrix[j][i]
        g_bruh=game.Grid()
        g_bruh.set_grid(score_matrix)
        g_bruh.print_grid()
        print()
    #calc the highest diff
    return score_matrix

def double_sum(grid):
    return np.sum(grid)

def alg_improved_comparison(game_obj:game.Grid,alpha=1,a=10,b=10):
    '''Wrapper for alg_improved that runs it for blacks and whites and then compares both'''
    scores_black=alg_improved(game_obj,value=Space.BLACK.value)
    scores_white=alg_improved(game_obj,value=Space.WHITE.value)
    #og_score=double_sum(scores_black)*alpha - double_sum(scores_white)
    #iterate through the entire grid, test for the next placement
    d=dict()
    #scores_final=[[0 for col in range(game_obj._x)] for row in range(game_obj._y)]
    for i in range(game_obj._x):
        for j in range(game_obj._y):
            x=i+1
            y=j+1
            if game_obj.get_value(x,y)!=Space.EMPTY.value:
                continue
            score_black=scores_black[j][i]
            score_white=scores_white[j][i]
            #remove comparison to the old move
            d[(x,y)]=(score_black)*alpha+(score_white)
            #print(d)
    #picking the best option available
    max_val=-inf
    final_x=0
    final_y=0
    for i in d.keys():
        if d[i]>max_val:
            max_val=d[i]
            final_x,final_y=i
    for i in d.keys():
        if d[i]==max_val:
            print(i,end=' ')
    print()
    return (final_x,final_y)

def alg_improved_sum(game_obj:game.Grid,alpha=0.8,a=8,b=10):
    '''Wrapper for alg_improved that runs it for blacks and whites and then compares both'''
    #score_black=double_sum(alg_improved(game_obj,value=Space.BLACK.value))
    #score_white=double_sum(alg_improved(game_obj,value=Space.WHITE.value))
    #og_score=double_sum(scores_black)*alpha - double_sum(scores_white)
    #iterate through the entire grid, test for the next placement
    d=dict()

    #scores_final=[[0 for col in range(game_obj._x)] for row in range(game_obj._y)]
    for i in range(game_obj._x):
        for j in range(game_obj._y):
            x=i+1
            y=j+1
            if game_obj.get_value(x,y)!=Space.EMPTY.value:
                continue
            future_game_obj=copy.deepcopy(game_obj)
            future_game_obj.put(x,y,Space.BLACK)
            score_black=double_sum(alg_improved(future_game_obj,value=Space.BLACK.value,k=a))
            score_white=double_sum(alg_improved(future_game_obj,value=Space.WHITE.value,k=b))
            #remove comparison to the old move
            d[(x,y)]=(score_black)*alpha+(score_white)
            #print(d)
    #picking the best option available
    max_val=-inf
    final_x=0
    final_y=0
    for i in d.keys():
        if d[i]>max_val:
            max_val=d[i]
            final_x,final_y=i
    for i in d.keys():
        if d[i]==max_val:
            print(i,end=' ')
    print()
    
    return (final_x,final_y)



    