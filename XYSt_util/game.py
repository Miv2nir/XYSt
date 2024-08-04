from XYSt_util.names import Names,Space
class Grid:
    def __init__(self,x=15,y=15):
        self._x=x
        self._y=y
        self._grid = [[0 for col in range(x)] for row in range(y)]

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
