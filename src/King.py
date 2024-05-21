from Piece import *
from constantes import *

class King(Piece):
    def __init__(self, Position, color) -> None:
        super().__init__(Position, color, KING)
        
    def IsValidMove(self, to):
        drow = abs(to.getRow() - self.position.getRow()) 
        dcol = abs(to.getCol() - self.position.getCol())
        return (drow == 1) or (dcol == 1)