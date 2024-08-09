from XYSt_util import game,players,names
from XYSt_util.names import Space
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