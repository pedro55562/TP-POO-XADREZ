from .Piece import *
from .constantes import *

class King(Piece):
    '''
    :param Position: Posição da peça
    :param color : a cor da peça
    :return: Se o movimento eh valido
    '''    
    def __init__(self, Position : Position , color : int) -> None:
        super().__init__(Position, color, KING)
        
    '''
    :param to: casa de destino do moviento 
    :return: Se o movimento eh valido
    '''
    def IsValidMove(self, to : Position) -> bool:
        drow = abs(to.getRow() - self.getPosition().getRow()) 
        dcol = abs(to.getCol() - self.getPosition().getCol())
        return (drow == 1) or (dcol == 1)