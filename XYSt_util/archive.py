from XYSt_util import game,players,names,alg
from XYSt_util.names import Space

import copy
def test1():
    g=game.Grid()
    g.win_black=5
    g.win_white=5
    g.put(5,5,names.Space.BLACK)
    g.put(6,6,names.Space.BLACK)
    g.put(7,7,names.Space.BLACK)
    g.put(8,8,names.Space.BLACK)
    g.put(9,9,names.Space.BLACK)
    g.print_grid()
    g.evaluate(verbal=True)
def test2():
    g=game.Grid()
    g.set_grid([[0 for col in range(2)] for row in range(2)])
    g.win_black=2
    g.win_white=2
    g.put(1,1,names.Space.WHITE)
    g.put(1,2,names.Space.BLACK)
    g.put(2,1,names.Space.WHITE)
    g.print_grid()
    g.evaluate(verbal=True)
def test3():
    g=game.Grid()
    g.set_grid([[0 for col in range(3)] for row in range(3)])
    g.win_black=3
    g.win_white=3
    g.put(2,1,names.Space.WHITE)
    g.put(1,1,names.Space.BLACK)
    g.put(2,2,names.Space.WHITE)
    g.put(1,2,names.Space.BLACK)
    g.put(1,3,names.Space.WHITE)
    
    #g.put(3,1,names.Space.BLACK)
    g.put(2,3,names.Space.BLACK)
    g.print_grid()
    print(g.evaluate_heuristics())
def test4():
    g=game.Grid()
    g.win_black=5
    g.win_white=5
    g.put(2,2,names.Space.WHITE)
    g.put(3,2,names.Space.BLACK)
    g.put(4,4,names.Space.WHITE)
    #g.put(2,2,names.Space.BLACK)
    #g.put(2,2,names.Space.BLACK)
    #g.put(5,7,names.Space.WHITE)
    g.print_grid()
    print(g.evaluate_heuristics())

def test5():
    g=game.Grid()
    #g.put(5,5,names.Space.BLACK)
    g.put(6,6,names.Space.BLACK)
    g.put(7,7,names.Space.BLACK)
    g.put(8,8,names.Space.BLACK)
    g.put(9,9,names.Space.BLACK)
    #g.put(9,9,names.Space.WHITE)
    g.print_grid()
    print(alg.alg_rush(g,max_moves=1))
    
    #g_bruh=game.Grid()
    #g_bruh.set_grid(alg.alg_improved(g,names.Space.BLACK.value))
    #g_bruh.print_grid()
    #for i in range(1,6):
    #    print(i)
    #    g_bruh.set_grid(alg.improved_eval(g,i))
    #    g_bruh.print_grid()
    #print(g_bruh.get_value(4,4))
    #print(alg.double_sum(g_bruh.get_grid()))

def test5_1():
    g=game.Grid()
    for i in range(2,4):
        g.put(i,1,names.Space.BLACK)


    g.print_grid()
    print()
    print(alg.check_completion(g,1,1,Space.BLACK.value,1,0,3))

def test5_2():
    g=game.Grid()
    g.put(8,8,names.Space.BLACK)
    g.print_grid()
    print()
    g_bruh=game.Grid()
    print(alg.check_completion_all_directions(g,7,8,Space.BLACK.value,5))

def test6():
    g=game.Grid()
    #g.put(5,5,names.Space.BLACK)
    #g.put(6,6,names.Space.WHITE)
    #g.put(5,6,names.Space.BLACK)
    #g.put(7,7,names.Space.WHITE)
    #g.put(5,7,names.Space.BLACK)
    #g.put(5,4,names.Space.WHITE)
    #g.put(5,9,names.Space.BLACK)
    #g.put(5,8,names.Space.WHITE)
    #g_bruh=copy.deepcopy(g)
    g.print_grid()
    print()
    g_bruh=game.Grid()
    #g_bruh.set_grid(alg.improved_eval(g,win_length=4,value=Space.WHITE.value))
    g_bruh.set_grid(alg.alg_improved(g,value=Space.BLACK.value))
    #g_bruh.set_grid(alg.alg_improved(g,value=Space.WHITE.value))
    
    g_bruh.print_grid()
    #print(g_bruh.get_value(8,8))
    #print(g_bruh.get_value(10,10))
    #aaa=4
    #print(alg.check_completion_all_directions(g,9,9,-1,aaa))
    #print(alg.check_completion_all_directions(g,10,10,-1,aaa))
    #print(alg.find_root_all_directions(g,5,6,-1,aaa))
    #print(alg.find_root_all_directions(g,10,10,-1,aaa))