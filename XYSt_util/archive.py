def test1():
    g=game.Grid()
    g.put(5,5,names.Space.BLACK)
    g.put(6,6,names.Space.BLACK)
    g.put(7,7,names.Space.BLACK)
    g.put(8,8,names.Space.BLACK)
    g.put(9,9,names.Space.BLACK)
    g.print_grid()
    g.evaluate()