from XYSt_util import game,alg
from XYSt_util.names import Names,Space

class Player:
    def __init__(self,name:Names):
        self.name=name
    
    def move(self,game_obj:game.Grid,x,y,verbal=False,white_label=False):
        if white_label:
            print(Names.WHITE.name,'sets a piece on (%s,%s)'%(x,y))
        else:
            print(self.name.name,'sets a piece on (%s,%s)'%(x,y))
        if self.name==Names.WHITE:
            game_obj.put(x,y,Space.WHITE)
        else:
            game_obj.put(x,y,Space.BLACK)
        return game_obj.evaluate(verbal)
    
    def analyze(self,game_obj:game.Grid,decision_max_seconds,move=True,verbal=False,white_label=False,printer=True):
        '''
        Suggests the next most beneficial move to the player.
        According to the design this function should only be called when the player is Black AKA a bot. (To be fixed)
        '''
        #algo goes here, continue on from here later
        #guess_x,guess_y = alg.alg_minimax_timed(game_obj,decision_max_seconds)
        #guess_x,guess_y = alg.alg_minimax(game_obj,depth=0)
        guess_x,guess_y = alg.alg_improved_comparison(game_obj)
        #to rewrite as alg_linear which's alg_minimax with depth 0 and then edit the formula
        if move:
            thought=self.move(game_obj,guess_x,guess_y,verbal,white_label)
            if white_label:
                game_obj.log(Names.WHITE,guess_x,guess_y)
            else:
                game_obj.log(Names.BLACK,guess_x,guess_y)
        else:
            thought=False
        if printer:
            game_obj.print_grid()
        return thought