from XYSt_util import game,names

def main():
    g=game.Grid()
    g.put(5,5,names.Space.WHITE)
    g.put(6,5,names.Space.WHITE)
    g.put(7,5,names.Space.WHITE)
    g.put(8,5,names.Space.WHITE)
    g.put(9,5,names.Space.WHITE)
    g.print_grid()
    g.evaluate()

if __name__ == '__main__':
    main()