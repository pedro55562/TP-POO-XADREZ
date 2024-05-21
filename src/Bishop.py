from Piece import *
from constantes import *
from Position import *

class Bishop(Piece):
    def __init__(self, Position, color) -> None:
        super().__init__(Position, color, BISHOP)
        
    def IsValidMove(self, to):
        drow = abs(to.getRow() - self.position.getRow()) 
        dcol = abs(to.getCol() - self.position.getCol())
        return drow == dcol