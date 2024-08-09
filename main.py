from XYSt_util import game,players,archive
from XYSt_util.names import Names, Space
def option_picker_str(options:set):
    while True: #option selector
        option=str(input("Type an option: "))
        if option in options:
            return option
        print('Incorrect option specified.')

def option_picker_int(options:set):
    while True: #option selector
        option=int(input("Pick an option: "))
        if option in options:
            return option
        print('Incorrect option number specified.')

def runtime(white,black,presets,decision_max_seconds,win_black,win_white):
    '''runtime for the CLI play'''
    print('Select an option:')
    print('1. Load a field preset')
    print('2. Define and randomly generate the game field')
    option1=option_picker_int({1,2})

    g=game.Grid()
    g.win_black=win_black
    g.win_white=win_white
    global decision_max_time
    decision_max_time=decision_max_seconds

    if option1==1: #picking a preset map
        print('Type the name of a desired preset.')
        print('Available presets are:')
        for i in presets:
            print("%s:"% i)
            g_temp=game.Grid()
            g_temp.set_grid(presets[i])
            g_temp.print_grid()
        g.set_grid(presets[option_picker_str(presets.keys())])
    elif option1==2: #generating a map
        x,y=map(int,input("Enter desired dimensions of a grid: ").split())
        print('Generating a grid of %s by %s...'%(x,y))
        g=game.Grid(x,y)
    g.print_grid()

    #gaming time
    game_over=False
    while not game_over:
        white_x,white_y=map(int,input('Select a space to place a peg in: ').split())
        #out of bounds check
        if (white_x>g._x) or (white_y>g._y) or (0>white_x) or (0>white_y):
            print(g._x,g._y)
            print('Selection is Out of Bounds!')
            continue
        #check for not selecting an empty space
        if g.get_value(white_x,white_y)!=0:
            print('This space is occupied!')
            continue
        #continuing on
        white.move(g,white_x,white_y,verbal=True)
        g.print_grid()
        game_over=black.analyze(g,decision_max_seconds,move=True,verbal=True)


def main():
    decision_max_seconds=10
    win_black=3
    win_white=3
    presets={
        'default':[[0 for col in range(15)] for row in range(15)],
        'small':[[0 for col in range(5)] for row in range(5)],
        'smallest':[[0 for col in range(3)] for row in range(3)],
        'smallestest':[[0 for col in range(2)] for row in range(2)]
    }
    #init players
    white=players.Player(Names.WHITE)
    black=players.Player(Names.BLACK)
    
    #runtime(white,black,presets,decision_max_seconds,win_black,win_white)
    archive.test4()

if __name__ == '__main__':
    main()