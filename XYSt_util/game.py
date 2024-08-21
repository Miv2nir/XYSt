from XYSt_util.names import Names,Space
class Grid:
    def __init__(self,x=15,y=15,win_white=5,win_black=5,alpha=1,a=10,b=10,rush_value=1):
        self._x=x
        self._y=y
        self._grid = [[0 for col in range(x)] for row in range(y)]
        
        self.win_white=win_white
        self.win_black=win_black
        #algorithm stuff
        self.alpha=alpha
        self.a=a
        self.b=b
        self.rush_value=rush_value
        self.log_dict=dict()

    def log(self,color:Names,x:int,y:int):
        '''Logs a move to be then printed out'''
        keynum=str((len(self.log_dict)+2)//2)
        while len(keynum)<3:
            keynum='0'+keynum
        keyletter=color.name[0].lower()
        self.log_dict[keyletter+keynum]=str((x,y))

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

    def set_grid(self,m):
        '''
        m is assumed to be a list of lists
        '''
        self._grid=m
        self._x=len(m[0])
        self._y=len(m)
    def put(self,x,y,piece:Space):
        '''Puts a piece on the board that is of the respective color'''
        if self._grid[y-1][x-1] == Space.EMPTY.value: 
            self._grid[y-1][x-1]=piece.value
        else:
            raise RuntimeWarning('(%s,%s) is already occupied!'%(str(x),str(y)))
        return self

    def get_value(self,x,y):
        '''Returns a value on an (x,y) coordinate'''
        return self._grid[y-1][x-1]
        
    def _check(self,x,y,value,dir_x,dir_y,length=1):
        '''Recursive check from a certain game position'''
        #dir values are for checking which way to look towards next time
        #add out of bounds checks here
        #print(x,y,self._grid[y-1][x-1])
        #print(length>=self.win_white,value,Space.WHITE.value)
        if length>=self.win_black or length>=self.win_white:
            return True
        elif x>self._x or y>self._y or x<1 or y<1:
            #out of bounds
            return False
        elif self._grid[y-1][x-1]!=value:
            return False #not a victory sequence
        else:
            return self._check(x+dir_x,y+dir_y,value,dir_x,dir_y,length+1)

    def evaluate(self,verbal=False):
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
                            if verbal:
                                print('White wins!')
                            return Space.WHITE.name
                        elif value == Space.BLACK.value:
                            if verbal:
                                print('Black wins!')
                            return Space.BLACK.name
        #nobody won
        if verbal:
            print('nobody won')
        return False
    def is_out_of_bounds(self,x,y):
        if x>self._x or y>self._y or x<1 or y<1:
            return True
        return False
    def _check_heuristics(self,x,y,value,dir_x,dir_y,tracker_length=1,length=1):
        '''Calculates distance to victory from a certain position in a defined direction'''
        #dir values are for checking which way to look towards next time
        #add out of bounds checks here
        #print(x,y,self._grid[y-1][x-1])
        #print(tracker_length>=self.win_white,value,Space.WHITE.value)
        if tracker_length>=self.win_black:
            return length
        elif tracker_length>=self.win_white:
            return length
        elif x>self._x or y>self._y or x<1 or y<1:
            #out of bounds
            return 0
        elif self._grid[y-1][x-1]==0:
            return self._check_heuristics(x+dir_x,y+dir_y,value,dir_x,dir_y,tracker_length+1,length) #not a victory sequence but possible to win
        elif self._grid[y-1][x-1]!=value:
            #blocked direction
            return 0
        else: #value on a spot == value parsed to function
                return self._check_heuristics(x+dir_x,y+dir_y,value,dir_x,dir_y,tracker_length+1,length+1)

    def evaluate_heuristics(self):
        '''
        Calculate the level of benefit of a particular position for blacks (heuristics stuff)
        '''
        white_score=-1
        black_score=0
        for i in range(self._x):
            for j in range(self._y):
                x=i+1
                y=j+1
                peg=self._grid[j][i]
                if self._grid[j][i]!=0:
                    value=self._grid[j][i]
                    # x+1 y = right
                    r=self._check_heuristics(x+1,y,value,1,0)
                    # x+1 y+1 = down right
                    dr=self._check_heuristics(x+1,y+1,value,1,1)
                    # x y+1 = down
                    d=self._check_heuristics(x,y+1,value,0,1)
                    # x-1 y+1 = down left
                    dl=self._check_heuristics(x-1,y+1,value,-1,1)
                    # x-1 y = left
                    l=self._check_heuristics(x-1,y,value,-1,0)
                    # x-1 y-1 = up left
                    ul=self._check_heuristics(x-1,y-1,value,-1,-1)
                    # x y-1 = up
                    u=self._check_heuristics(x,y-1,value,0,-1)
                    # x+1 y-1 = up right
                    ur=self._check_heuristics(x+1,y-1,value,1,-1)
                    #score time
                    if value>0:
                        #black
                        black_score=max(black_score,r,dr,d,dl,l,ul,u,ur) #>0
                    elif value<0:
                        #white
                        white_score=min(white_score,-r,-dr,-d,-dl,-l,-ul,-u,-ur) #<0
        #got our scores and everything
        debug=(black_score+white_score)/self.win_black
        return (black_score+white_score)/self.win_black
    