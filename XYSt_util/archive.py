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
    g.put(5,5,names.Space.BLACK)
    g.put(6,6,names.Space.WHITE)
    g.put(5,6,names.Space.BLACK)
    g.put(7,7,names.Space.WHITE)
    g.put(5,7,names.Space.BLACK)
    g.put(5,4,names.Space.WHITE)
    g.put(5,9,names.Space.BLACK)
    g.put(5,8,names.Space.WHITE)
    #g_bruh=copy.deepcopy(g)
    print()
    g.print_grid()
    print()
    g_bruh1=game.Grid()
    g_bruh2=game.Grid()
    #g_bruh.set_grid(alg.improved_eval(g,win_length=4,value=Space.WHITE.value))
    #g_bruh1.set_grid(alg.alg_improved(g,value=Space.BLACK.value))
    #for i in range(g._x):
    #    for j in range(g._y):
    #        x=i+1
    #        y=j+1

    g_bruh1.set_grid(alg.improved_eval(g,5,value=Space.BLACK.value))
    #g_bruh2.set_grid(alg.improved_eval(g,5,value=Space.WHITE.value))
    g_bruh2.set_grid(alg.alg_improved(g,value=Space.BLACK.value))
    
    g_bruh1.print_grid()
    g_bruh2.print_grid()
    print(g_bruh1.get_value(6,5))
    print(g_bruh1.get_value(9,9))
    print(g_bruh2.get_value(6,5))
    print(g_bruh2.get_value(9,9))
    #print(alg.find_root_all_directions(g,4,6,Space.BLACK.value,4))
    #g_bruh2.print_grid()
    #print(g_bruh1.get_value(7,9))
    #print(g_bruh2.get_value(7,9))
    #print(g_bruh2.get_value(8,8))
    #aaa=4
    #print(alg.check_completion_all_directions(g,8,8,-1,aaa))
    #print(alg.check_completion_all_directions(g,9,9,-1,aaa))
    #print(alg.find_root_all_directions(g,8,8,-1,aaa))
    #print(alg.find_root_all_directions(g,9,9,-1,aaa))

def test7():
    g=game.Grid()
    #g.put(9,5,names.Space.WHITE)
    #print(alg.calc_line(g,5,5,Space.BLACK.value,1,0,5))
    g.put(6,5,Space.BLACK)
    g.put(7,5,Space.BLACK)
    g.put(8,5,Space.BLACK)
    g.put(9,5,Space.BLACK)
    print(alg.calc_ways(g,5,5,Space.BLACK.value,1))

def test8():
    g=game.Grid()
    g.put(5,5,names.Space.BLACK)
    g.put(6,6,names.Space.WHITE)
    g.put(5,6,names.Space.BLACK)
    g.put(7,7,names.Space.WHITE)
    g.put(5,7,names.Space.BLACK)
    g.put(5,4,names.Space.WHITE)
    g.put(5,9,names.Space.BLACK)
    g.put(5,8,names.Space.WHITE)
    g.put(9,9,names.Space.BLACK)
    g.print_grid()
    print(alg.calc_ways(g,7,9,Space.WHITE.value,3))
def test9():
    g=game.Grid()
    g.put(5, 5,names.Space.BLACK)
    g.put(6, 6,names.Space.WHITE)
    g.put(5, 6,names.Space.BLACK)
    g.put(7, 7,names.Space.WHITE)
    g.put(5, 7,names.Space.BLACK)
    g.put(5, 4,names.Space.WHITE)
    g.put(5, 9,names.Space.BLACK)
    g.put(5, 8,names.Space.WHITE)
    g.put(6, 5,names.Space.BLACK)
    g.put(8, 8,names.Space.WHITE)
    g.put(9, 9,names.Space.BLACK)
    g.put(7, 8,names.Space.WHITE)
    g.put(6, 8,names.Space.BLACK)
    g.put(7, 9,names.Space.WHITE)
    g.put(7, 6,names.Space.BLACK)
    g.put(6, 10,names.Space.WHITE)
    g.put(9, 7,names.Space.BLACK)
    g.put(5, 11,names.Space.WHITE)
    g.put(4, 12,names.Space.BLACK)
    g.put(7, 10,names.Space.WHITE)
    g.put(7, 11,names.Space.BLACK)
    g.put(5, 10,names.Space.WHITE)
    g.put(8, 10,names.Space.BLACK)
    g.put(4, 10,names.Space.WHITE)
    g.put(3, 10,names.Space.BLACK)
    g.put(6, 12,names.Space.WHITE)
    g.put(3, 9,names.Space.BLACK)
    g.put(7, 13,names.Space.WHITE)
    g.put(8, 14,names.Space.BLACK)
    g.put(6, 11,names.Space.WHITE)
    g.put(6, 13,names.Space.BLACK)
    g.put(5, 12,names.Space.WHITE)
    g.put(8, 9,names.Space.BLACK)
    g.put(5, 13,names.Space.WHITE)
    g.put(5, 14,names.Space.BLACK)
    g.put(4, 13,names.Space.WHITE)
    g.put(3, 14,names.Space.BLACK)
    g.put(2, 13,names.Space.WHITE)
    g.put(10, 8,names.Space.BLACK)
    g.put(3, 13,names.Space.WHITE)
    #g.put(1, 13,names.Space.BLACK)
    #g.put(3, 11,names.Space.WHITE)
    #g.put(11, 7,names.Space.BLACK)
    #g.put(11,7,names.Space.BLACK)
    g.print_grid()
    print(alg.check_completion_rush_all(g,7,11,Space.BLACK.value,1))
    print(alg.check_completion_rush_all(g,5,13,Space.WHITE.value,1))
    print(alg.alg_rush(g,1))
    print(g.evaluate())

def test10():
    g=game.Grid(2,7,4,3)
    g.put(1,1,Space.BLACK)
    g.put(1,2,Space.BLACK)
    g.put(1,3,Space.BLACK)
    #g.put(1,4,Space.WHITE)
    g.print_grid()
    print(g.evaluate())
