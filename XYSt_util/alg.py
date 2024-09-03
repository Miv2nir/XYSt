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
            #print(d)
    
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

def check_completion_old(game_obj:game.Grid,x,y,value,dir_x,dir_y,target_moves):
    '''Rewrite of game_obj._check_heuristics() to work with improved_evaluation.
    Checks whether the line can be completed in a given direction (returns 0 or 1 integer)'''
    #x,y - starter coordinates
    #check if a spot is already occupied or not
    if game_obj.is_out_of_bounds(x,y):
        return 0
    if game_obj.get_piece(x,y).value!=0: 
        #0 is good
        return 0
    length=1
    zero_count=1
    if value==Space.WHITE.value:
        win_length=game_obj.win_white
    else:
        win_length=game_obj.win_black
    while length<win_length:
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

def check_completion(game_obj:game.Grid,x,y,value,dir_x,dir_y,target_moves):
    '''Rewrite of game_obj._check_heuristics() to work with improved_evaluation.
    Checks whether the line can be completed in a given direction (returns 0 or 1 integer)'''
    #x,y - starter coordinates
    #check if a spot is already occupied or not
    if game_obj.is_out_of_bounds(x,y):
        return 0
    if not (game_obj.get_piece(x,y).value==0 or game_obj.get_piece(x,y).value==value): 
        #0 and value are good
        return 0
    length=1
    if game_obj.get_piece(x,y).value==0:
        zero_count=1
    else:
        zero_count=0
    if value==Space.WHITE.value:
        win_length=game_obj.win_white
    else:
        win_length=game_obj.win_black
    while length<win_length:
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


def find_root(game_obj,x,y,value,dir_x,dir_y,target_moves):
    #target moves is specifically how many moves can be taken
    if game_obj.is_out_of_bounds(x,y):
        return 0
    if game_obj.get_piece(x,y).value!=0: #double check on the starting pos
        return 0
    length=1
    zero_count=1
    if value==Space.WHITE.value:
        win_length=game_obj.win_white
    else:
        win_length=game_obj.win_black
    while length<win_length:
        x+=dir_x
        y+=dir_y
        if game_obj.is_out_of_bounds(x,y):
            #back track 1 move
            return 0
        if game_obj.get_piece(x,y).value!=value and game_obj.get_piece(x,y)!=0:
            #back track 1 move
            x-=dir_x
            y-=dir_y
            return check_completion(game_obj,x,y,value,dir_x*(-1),dir_y*(-1),target_moves)
        length+=1
        if game_obj.get_piece(x,y)==0:
            zero_count+=1
        if zero_count>target_moves:
            return 0
    return check_completion(game_obj,x,y,value,dir_x*(-1),dir_y*(-1),target_moves)

def check_completion_all_directions(game_obj,x,y,value,win_length):
    #idea: go into all possible directions, record where a victory line can start
    #afterwards call check_completion in an opposite direction
    # x+1 y = right
    r=check_completion_old(game_obj,x,y,value=value,dir_x=1,dir_y=0,target_moves=win_length)
    # x+1 y+1 = down right
    dr=check_completion_old(game_obj,x,y,value=value,dir_x=1,dir_y=1,target_moves=win_length)
    # x y+1 = down
    d=check_completion_old(game_obj,x,y,value=value,dir_x=0,dir_y=1,target_moves=win_length)
    # x-1 y+1 = down left
    dl=check_completion_old(game_obj,x,y,value=value,dir_x=-1,dir_y=1,target_moves=win_length)
    # x-1 y = left
    l=check_completion_old(game_obj,x,y,value=value,dir_x=-1,dir_y=0,target_moves=win_length)
    # x-1 y-1 = up left
    ul=check_completion_old(game_obj,x,y,value=value,dir_x=-1,dir_y=-1,target_moves=win_length)
    # x y-1 = up
    u=check_completion_old(game_obj,x,y,value=value,dir_x=0,dir_y=-1,target_moves=win_length)
    # x+1 y-1 = up right
    ur=check_completion_old(game_obj,x,y,value=value,dir_x=1,dir_y=-1,target_moves=win_length)
    #score time
    return sum([r,dr,d,dl,l,ul,u,ur])

def find_root_all_directions(game_obj,x,y,value,win_length):
    #idea: go into all possible directions, record where a victory line can start
    #afterwards call find_root in an opposite direction
    # x+1 y = right
    r=find_root(game_obj,x,y,value=value,dir_x=1,dir_y=0,target_moves=win_length)
    # x+1 y+1 = down right
    dr=find_root(game_obj,x,y,value=value,dir_x=1,dir_y=1,target_moves=win_length)
    # x y+1 = down
    d=find_root(game_obj,x,y,value=value,dir_x=0,dir_y=1,target_moves=win_length)
    # x-1 y+1 = down left
    dl=find_root(game_obj,x,y,value=value,dir_x=-1,dir_y=1,target_moves=win_length)
    # x-1 y = left
    l=find_root(game_obj,x,y,value=value,dir_x=-1,dir_y=0,target_moves=win_length)
    # x-1 y-1 = up left
    ul=find_root(game_obj,x,y,value=value,dir_x=-1,dir_y=-1,target_moves=win_length)
    # x y-1 = up
    u=find_root(game_obj,x,y,value=value,dir_x=0,dir_y=-1,target_moves=win_length)
    # x+1 y-1 = up right
    ur=find_root(game_obj,x,y,value=value,dir_x=1,dir_y=-1,target_moves=win_length)
    #score time
    final_old=[r,dr,d,dl,l,ul,u,ur]
    final_new=[max(r,l),max(dr,ul),max(dl,ur),max(u,d)]
    return sum(final_old)

def calc_line(game_obj:game.Grid,x,y,value,dir_x,dir_y,max_moves):
    #given a direction, offset by win_length-1 moves
    #begin a loop, going through the line for win_length times
    #if out of bounds or otherwise the line cannot be completed, continue
    #if the line can be completed within target moves, +1
    #return the counted number
    if value==Space.WHITE.value:
        win_length=game_obj.win_white
    if value==Space.BLACK.value:
        win_length=game_obj.win_black
    x-=(dir_x)*(win_length-1)
    y-=(dir_y)*(win_length-1)
    #coords are now in the beginning of the track
    count_ways=0
    for _ in range(win_length):
        if game_obj.is_out_of_bounds(x,y): #skipping ahead
            x+=dir_x
            y+=dir_y
            continue
        zero_count=0
        possible_to_finish=True
        for i in range(win_length):
            temp_x=x+(i*dir_x)
            temp_y=y+(i*dir_y)
            if game_obj.is_out_of_bounds(temp_x,temp_y):
                possible_to_finish=False
                break 
            elif game_obj.get_piece(temp_x,temp_y).value==0:
                zero_count+=1
            elif game_obj.get_piece(temp_x,temp_y).value==value:
                pass
            else:
                possible_to_finish=False
                break
        if possible_to_finish and zero_count<=max_moves:
            count_ways+=1
        x+=dir_x
        y+=dir_y
    return count_ways
        


def calc_ways(game_obj,x,y,value,win_length):
    '''Yet another calc function that should count all the ways to fill in lines passing through a point and stuff'''
    #4 directions
    #left-right (treat as right)
    r=calc_line(game_obj,x,y,value,1,0,win_length)
    #up-down (treat as down)
    d=calc_line(game_obj,x,y,value,0,1,win_length)
    #upleft-downright (treat as downright)
    dr=calc_line(game_obj,x,y,value,1,1,win_length)
    #upright-downleft (treat as downleft)
    dl=calc_line(game_obj,x,y,value,-1,1,win_length)
    return sum([r,d,dr,dl])

def improved_eval(game_obj:game.Grid,win_length:int,value=Space.BLACK.value):
    #rough algo description:
    eval_grid=[[0 for col in range(game_obj._x)] for row in range(game_obj._y)]
    #For every point:
    #calc_length=game_obj.win_white-win_length
    for i in range(game_obj._x):
        for j in range(game_obj._y):
            #if point is zero:
            if game_obj._grid[j][i]==0:
                x=i+1
                y=j+1
                #calculate how many ways are there to reach a victory in x moves
                #similar to game_obj.evaluate_heuristics():
                #eval_grid[j][i]=find_root_all_directions(game_obj,x,y,value,win_length)
                eval_grid[j][i]=calc_ways(game_obj,x,y,value,win_length)

            #how did the coefficients change after one's move in P.
            #calculated coefficients to be added up, multiplied by k^(-1) where k=10
            #check in 3 stages, P has a white peg, a black peg or is empty
            #pick a point with the largest difference
    return eval_grid

def alg_improved(game_obj:game.Grid,value,k=10):
    '''New version of a linear evaluation function algorithm previously used as part of a minimax process'''
    score_matrix=[[0 for col in range(game_obj._x)] for row in range(game_obj._y)]

    win_length=game_obj.win_black
    if value==Space.WHITE:
        win_length=game_obj.win_white

    for a in range(1,win_length+1):
        intermediate_score_matrix=improved_eval(game_obj,a,value)
        for i in range(game_obj._x):
            for j in range(game_obj._y):
                intermediate_score_matrix[j][i]*=(k**(win_length-a))
                score_matrix[j][i]+=intermediate_score_matrix[j][i]
        #g_bruh=game.Grid()
        #g_bruh.set_grid(score_matrix)
        #g_bruh.print_grid()
        #print()
    #calc the highest diff
    return score_matrix

def double_sum(grid):
    return np.sum(grid)

def check_completion_rush(game_obj:game.Grid,x,y,value,dir_x,dir_y,target_moves):
    '''Rewrite of game_obj._check_heuristics() to work with improved_evaluation.
    Checks whether the line can be completed in a given direction specifically for the rush algorithm
    Checks only from the filled in points, returns in how many moves the line can be completed.
    Returns coordinates that shall be filled in to win.'''
    #x,y - starter coordinates
    #check if a spot is already occupied or not
    if game_obj.is_out_of_bounds(x,y):
        return set()
    if game_obj.get_piece(x,y).value==0: #double check
        return set()
    length=1
    zero_coords=set()
    if value==Space.WHITE.value:    
        win_length=game_obj.win_white
    else:
        win_length=game_obj.win_black
    while length<win_length:
        x+=dir_x
        y+=dir_y
        if game_obj.is_out_of_bounds(x,y):
            return set()
        if game_obj.get_piece(x,y).value!=value and game_obj.get_piece(x,y)!=Space.EMPTY:
            return set()
        length+=1
        if game_obj.get_piece(x,y)==Space.EMPTY:
            zero_coords.add((x,y))
    if len(zero_coords)>target_moves:
        return set()
    return zero_coords

def check_completion_rush_all(game_obj,x,y,value,max_moves):
    r=check_completion_rush(game_obj,x,y,value=value,dir_x=1,dir_y=0,target_moves=max_moves)
    # x+1 y+1 = down right
    dr=check_completion_rush(game_obj,x,y,value=value,dir_x=1,dir_y=1,target_moves=max_moves)
    # x y+1 = down
    d=check_completion_rush(game_obj,x,y,value=value,dir_x=0,dir_y=1,target_moves=max_moves)
    # x-1 y+1 = down left
    dl=check_completion_rush(game_obj,x,y,value=value,dir_x=-1,dir_y=1,target_moves=max_moves)
    # x-1 y = left
    l=check_completion_rush(game_obj,x,y,value=value,dir_x=-1,dir_y=0,target_moves=max_moves)
    # x-1 y-1 = up left
    ul=check_completion_rush(game_obj,x,y,value=value,dir_x=-1,dir_y=-1,target_moves=max_moves)
    # x y-1 = up
    u=check_completion_rush(game_obj,x,y,value=value,dir_x=0,dir_y=-1,target_moves=max_moves)
    # x+1 y-1 = up right
    ur=check_completion_rush(game_obj,x,y,value=value,dir_x=1,dir_y=-1,target_moves=max_moves)
    #score time
    min_moves=inf
    final=set()
    for i in [r,dr,d,dl,l,ul,u,ur]:
        if len(i)<min_moves and i!=set():
            min_moves=len(i)
            final=i
        else:
            final=final.union(i)
    return (min_moves,final)    

def alg_rush(game_obj:game.Grid,max_moves=1):
    '''Helper algorithm that attempts to rush a win'''
    moves_white=set()
    moves_black=set()
    distance_to_win_white=game_obj.win_white
    distance_to_win_black=game_obj.win_black
    for i in range(game_obj._x):
        for j in range(game_obj._y):
            x=i+1
            y=j+1
            if game_obj.get_piece(x,y)==Space.EMPTY:
                continue
            if game_obj.get_piece(x,y)==Space.WHITE:
                thought=check_completion_rush_all(game_obj,x,y,Space.WHITE.value,max_moves)
                if thought[1]==set(): #no actual way to proceed
                    pass
                elif thought[0]<distance_to_win_white:
                    distance_to_win_white=thought[0]
                    moves_white=thought[1]
                else:
                    moves_white=moves_white.union(thought[1])
            
            if game_obj.get_piece(x,y)==Space.BLACK:
                thought=check_completion_rush_all(game_obj,x,y,Space.BLACK.value,max_moves)
                if thought[1]==set(): #no actual way to proceed
                    pass
                elif thought[0]<distance_to_win_black:
                    distance_to_win_black=thought[0]
                    moves_black=thought[1]
                else:
                    moves_black=moves_black.union(thought[1])
    #check if empty
    if moves_white==set() and moves_black==set():
        return False
    else:
        if distance_to_win_black<=distance_to_win_white:
            i=random.randrange(0,len(moves_black))
            return list(moves_black)[i]
        else:
            i=random.randrange(0,len(moves_white))
            return list(moves_white)[i]
            

def alg_improved_comparison(game_obj:game.Grid):
    '''Wrapper for alg_improved that runs it for blacks and whites and then compares both'''
    #first of all check if a rushed win is possible
    alpha=game_obj.alpha
    a=game_obj.a
    b=game_obj.b
    rush_value=game_obj.rush_value
    thought=alg_rush(game_obj,max_moves=rush_value)
    if thought!=False:
        return thought
    #regular algorithm because the alg_rush did not find any possible to finish immediately positions
    scores_black=alg_improved(game_obj,value=Space.BLACK.value,k=b)
    scores_white=alg_improved(game_obj,value=Space.WHITE.value,k=a)
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
    final_x=[]
    final_y=[]
    if game_obj.k==0:
        for i in d.keys():
            if d[i]>max_val:
                max_val=d[i]
                final_x=[i[0]]
                final_y=[i[1]]
                #final_x,final_y=i
            elif d[i]==max_val:
                final_x.append(i[0])
                final_y.append(i[1])
    else:
        for i in d.keys():
            if (d[i] >= max_val-max_val*game_obj.k) and (d[i] <= max_val+max_val*game_obj.k):
                #print(max_val*game_obj.k,max_val-max_val*game_obj.k,max_val+max_val*game_obj.k)
                final_x.append(i[0])
                final_y.append(i[1])
            elif d[i]>max_val:
                max_val=d[i]
                final_x=[i[0]]
                final_y=[i[1]]
                #final_x,final_y=i

    #for i in d.keys():
    #    if d[i]==max_val:
            #print(i,end=' ')
    #print()
    i=random.randrange(0,len(final_x))
    return (final_x[i],final_y[i])

def alg_improved_sum(game_obj:game.Grid,alpha=0.8,a=8,b=10):
    '''Wrapper for alg_improved that runs it for blacks and whites and then compares both (works badly)'''
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
    #for i in d.keys():
    #    if d[i]==max_val:
            #print(i,end=' ')
    #print()
    
    return (final_x,final_y)



    