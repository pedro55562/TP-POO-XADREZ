from .Piece import *
from .constantes import *

class Pawn(Piece):
    def __init__(self, Position, color) -> None:
        super().__init__(Position, color, PAWN)
        
    def IsValidMove(self, to, toColor):
        drow = to.getRow() - self.position.getRow() 
        dcol = to.getCol() - self.position.getCol()
        
        if dcol == 0 and toColor == EMPTY:
            
            if self.getColor() == BLACKn:
                if self.position.getRow() == 1:
                    return drow == 1 or drow == 2
                elif self.position.getRow() != 1:
                    return drow == 1
            
            if self.getColor() == WHITEn:
                if self.position.getRow() == 6:
                    return drow == -1 or drow == -2
                elif self.position.getRow() != 6:
                    return drow == -1
        
        if toColor != EMPTY and abs(dcol) == 1:
            if self.getColor() == BLACKn and toColor == WHITEn:
                return abs(dcol) == 1 and drow == 1
                
            if self.getColor() == WHITEn and toColor == BLACKn:
                return abs(dcol) == 1 and drow == -1