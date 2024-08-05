from XYSt_util.names import Names,Space
class Grid:
    def __init__(self,x=15,y=15,win_white=5,win_black=5):
        self._x=x
        self._y=y
        self._grid = [[0 for col in range(x)] for row in range(y)]
        
        self.win_white=win_white
        self.win_black=win_black

    def print_grid(self):
        for i in self._grid:
            print(i)
        return None
    
    def get_piece(self,x,y):
        '''Returns a piece on an (x,y) coordinate'''
        piece = self._grid[y-1][x-1]
        if piece == Space.WHITE.value:
            return Space.WHITE
        if piece == Space.BLACK.value:
            return Space.BLACK
        else:
            return Space.EMPTY

    def get_grid(self):
        '''Returns the grid'''
        return self._grid

    def put(self,x,y,piece:Space):
        '''Puts a piece on the board that is of the respective color'''
        if self._grid[y-1][x-1] == Space.EMPTY.value: 
            self._grid[y-1][x-1]=piece.value
        else:
            raise RuntimeWarning('(%s,%s) is already occupied!'%(str(x),str(y)))
        return self

    def _check(self,x,y,value,dir_x,dir_y,length=1):
        '''Recursive check from a certain game position'''
        #dir values are for checking which way to look towards next time
        #add out of bounds checks here
        print(x,y,self._grid[y-1][x-1])
        print(length>=self.win_white,value,Space.WHITE.value)
        if x>self._x or y>self._y or x<1 or y<1:
            #out of bounds
            return False
        elif length>=self.win_black and value==Space.BLACK.value:
            return True #black won
        elif length>=self.win_white and value==Space.WHITE.value:
            return True #white won
        elif self._grid[y-1][x-1]!=value:
            return False #not a victory sequence
        else:
            return self._check(x+dir_x,y+dir_y,value,dir_x,dir_y,length+1)

    def evaluate(self):
        '''
        Check the condition of the field to see if anybody won
        '''
        white_wins=False
        black_wins=False
        for i in range(self._x):
            for j in range(self._y):
                if self._grid[j][i]!=0:
                    #check 8 possible directions for a possible win
                    # x increase means moving to the right
                    # y increase means moving down
                    x=i+1
                    y=j+1
                    value=self._grid[j][i]
                    # x+1 y = right
                    r=self._check(x+1,y,value,1,0)
                    # x+1 y+1 = down right
                    dr=self._check(x+1,y+1,value,1,1)
                    # x y+1 = down
                    d=self._check(x,y+1,value,0,1)
                    # x-1 y+1 = down left
                    dl=self._check(x-1,y+1,value,-1,1)
                    # x-1 y = left
                    l=self._check(x-1,y,value,-1,0)
                    # x-1 y-1 = up left
                    ul=self._check(x-1,y-1,value,-1,-1)
                    # x y-1 = up
                    u=self._check(x,y-1,value,0,-1)
                    # x+1 y-1 = up right
                    ur=self._check(x+1,y-1,value,1,-1)
                    #if any of those are victorious, return true
                    condition=(r or dr or d or dl or l or ul or u or ur)
                    if condition:
                        if value == Space.WHITE.value:
                            print('White wins!')
                            return Space.WHITE.name
                        elif value == Space.BLACK.value:
                            print('Black wins!')
                            return Space.BLACK.name
        #nobody won
        print('nobody won')
        return False
