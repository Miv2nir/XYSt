from XYSt_util import game,players,archive
from XYSt_util.names import Names, Space
import random
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

def runtime(white,black,presets,presets_win_lengths,decision_max_seconds,win_black,win_white,alpha,a,b,rush_value,k):
    '''runtime for the CLI play'''
    print('Select an option:')
    print('1. Load a field preset')
    print('2. Define and randomly generate the game field')
    option1=option_picker_int({1,2})

    g=game.Grid()
    g.win_black=win_black
    g.win_white=win_white
    #insert algorithm parameters
    g.rush_value=rush_value
    if k==0:
        g.alpha=alpha
        g.a=a
        g.b=b 
        g.k=0
    else:
        k=k/100
        g.alpha=random.uniform(alpha-k,alpha+k)
        g.a=random.uniform(a-k,a+k)
        g.b=random.uniform(b-k,b+k)
        g.k=k
    
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
        selection=option_picker_str(presets.keys())
        g.set_grid(presets[selection])
        g.win_black=presets_win_lengths[selection][0]
        g.win_white=presets_win_lengths[selection][1]
        print('Selected preset:',selection+',win lenghts for white & black:(%s,%s)'%(g.win_white,g.win_black))
    elif option1==2: #generating a map
        x,y=map(int,input("Enter desired dimensions of a grid: ").split())
        print('Generating a grid of %s by %s...'%(x,y))
        g=game.Grid(x,y)
        g.win_white,g.win_black=map(int,input("Enter win condition lenghts for white & black respectively: ").split())
    g.print_grid()
    print("Who's playing the game?")
    print("1. Player vs bot")
    print("2. Bot vs bot")
    play_mode=option_picker_int({1,2})
    if play_mode==2:
        #bot vs bot
        game_over=False
        while not game_over:
            #first move
            try:
                game_over=black.analyze(g,decision_max_seconds,move=True,verbal=True)
            except (RuntimeWarning, ValueError) as e:
                #the game is over with a draw
                game_over=True
                print('Draw!')
            black_win=g.evaluate(verbal=True)
            if black_win==Space.BLACK.name:
                print(str(g.log_dict).replace('\'','"'))
                exit(0) #the game is over
            #the move is done, flip the game field and proceed
            g.reverse()
            try:
                game_over=black.analyze(g,decision_max_seconds,move=True,verbal=True,printer=False,white_label=True)
                g.reverse()
                g.print_grid()
            except (RuntimeWarning, ValueError) as e:
                #the game is over with a draw
                game_over=True
                g.print_grid()
                print('Draw!')
        #if white wins the loop should exit gracefully
    else:  
        #regular player vs bot time      
        print('Who is making the first move? (player, bot)')
        first_move=option_picker_str({'player','bot'})
        #gaming time
        game_over=False
        if first_move=='bot':
            game_over=black.analyze(g,decision_max_seconds,move=True,verbal=True)
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
            g.log(Names.WHITE,white_x,white_y)
            g.print_grid()
            white_win=g.evaluate(verbal=True)
            if white_win==Space.WHITE.name:
                print(str(g.log_dict).replace('\'','"'))
                exit(0) #the game is over
            try:
                game_over=black.analyze(g,decision_max_seconds,move=True,verbal=True)
            except RuntimeWarning:
                #the game is over with a draw
                game_over=True
                print('Draw!')
    print(str(g.log_dict).replace('\'','"'))


def main():
    #settings
    decision_max_seconds=10 #does not work with the current algorithm in place
    win_black=5
    win_white=5
    #algorithm parameters
    alpha=1 #agression 
    a=10 #evaluation factor for the white player
    b=10 #evaluation factor for the black player
    rush_value=1 #in how many moves until one's victory the alg_rush() shall trigger
    k=5 #percentage of the constants (alpha,a,b) deviating from the set values as well as position selection
    presets={
        'default':[[0 for col in range(15)] for row in range(15)],
        'small':[[0 for col in range(5)] for row in range(5)],
        'tictactoe':[[0 for col in range(3)] for row in range(3)],
        'smallest':[[0 for col in range(2)] for row in range(2)]
    }
    presets_win_lengths={
        'default':(5,5),
        'small':(4,4),
        'tictactoe':(3,3),
        'smallest':(2,2)
    }
    #init players
    white=players.Player(Names.WHITE)
    black=players.Player(Names.BLACK)
    
    runtime(white,black,presets,presets_win_lengths,decision_max_seconds,win_black,win_white,alpha,a,b,rush_value,k)
    #archive.test6()
    #archive.test10()

if __name__ == '__main__':
    main()