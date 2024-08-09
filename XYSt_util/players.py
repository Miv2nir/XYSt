from XYSt_util import game,alg
from XYSt_util.names import Names,Space

class Player:
    def __init__(self,name:Names):
        self.name=name
    
    def move(self,game_obj:game.Grid,x,y,verbal=False):
        print(self.name.name,'sets a piece on (%s,%s)'%(x,y))
        if self.name==Names.WHITE:
            game_obj.put(x,y,Space.WHITE)
        else:
            game_obj.put(x,y,Space.BLACK)
        return game_obj.evaluate(verbal)
    
    def analyze(self,game_obj:game.Grid,decision_max_seconds,move=True,verbal=False):
        '''
        Suggests the next most beneficial move to the player.
        According to the design this function should only be called when the player is Black AKA a bot.
        '''
        #algo goes here, continue on from here later
        #guess_x,guess_y = alg.alg_minimax_timed(game_obj,decision_max_seconds)
        guess_x,guess_y = alg.alg_minimax(game_obj)
        if move:
            thought=self.move(game_obj,guess_x,guess_y,verbal)
        else:
            thought=False
        game_obj.print_grid()
        return thought