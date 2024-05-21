from .Piece import *
from .constantes import *

class Knight(Piece):
    def __init__(self, Position, color) -> None:
        super().__init__(Position, color, KNIGHT)
        
    def IsValidMove(self, to):
        drow = abs(to.getRow() - self.position.getRow()) 
        dcol = abs(to.getCol() - self.position.getCol())
        return ((drow == 1)and(dcol == 2)) or ((drow == 2)and(dcol == 1))