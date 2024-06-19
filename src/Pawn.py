from .Piece import *
from .constantes import *

class Pawn(Piece):
    '''
    :param Position: Posição da peça
    :param color : a cor da peça
    :return: Se o movimento eh valido
    '''
    def __init__(self, Position : Position, color : int) -> None:
        super().__init__(Position, color, PAWN)
        
    '''
    :param to: casa de destino do moviento 
    :param toColor: cor da peça presente no destino
    :return: Se o movimento eh valido
    '''        
    def IsValidMove(self, to : Position, toColor : int)-> bool:
        drow = to.getRow() - self.getPosition().getRow() 
        dcol = to.getCol() - self.getPosition().getCol()
        
        if dcol == 0 and toColor == EMPTY:
            
            if self.getColor() == BLACKn:
                if self.getPosition().getRow() == 1:
                    return drow == 1 or drow == 2
                elif self.getPosition().getRow() != 1:
                    return drow == 1
            
            if self.getColor() == WHITEn:
                if self.getPosition().getRow() == 6:
                    return drow == -1 or drow == -2
                elif self.getPosition().getRow() != 6:
                    return drow == -1
        
        if toColor != EMPTY and abs(dcol) == 1:
            if self.getColor() == BLACKn and toColor == WHITEn:
                return abs(dcol) == 1 and drow == 1
                
            if self.getColor() == WHITEn and toColor == BLACKn:
                return abs(dcol) == 1 and drow == -1