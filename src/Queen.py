from .Piece import *
from .constantes import *

class Queen(Piece):
    def __init__(self, Position, color) -> None:
        super().__init__(Position, color, QUEEN)
        
    def IsValidMove(self, to):
        drow = abs(to.getRow() - self.getPosition().getRow()) 
        dcol = abs(to.getCol() - self.getPosition().getCol())
        return (drow == dcol)or((drow != 0) and (dcol == 0))or((drow == 0) and (dcol != 0))