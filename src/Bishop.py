from .Piece import *
from .constantes import *
from .Position import *

class Bishop(Piece):
    '''
    :param Position: Posição da peça
    :param color : a cor da peça
    :return: Se o movimento eh valido
    '''    
    def __init__(self, Position : Position , color : int ) -> None:
        super().__init__(Position, color, BISHOP)
    
    '''
    :param to: casa de destino do moviento 
    :return: Se o movimento eh valido
    '''
    def IsValidMove(self, to : Position) -> bool:
        drow = abs(to.getRow() - self.getPosition().getRow()) 
        dcol = abs(to.getCol() - self.getPosition().getCol())
        return drow == dcol