from .Piece import *
from .constantes import *

class Rook(Piece):
    def __init__(self, Position, color) -> None:
        super().__init__(Position, color, ROOK)
        
    def IsValidMove(self, to):
        drow = abs(to.getRow() - self.getPosition().getRow()) 
        dcol = abs(to.getCol() - self.getPosition().getCol())
        return ((drow != 0) and (dcol == 0)) or ((drow == 0) and (dcol != 0))