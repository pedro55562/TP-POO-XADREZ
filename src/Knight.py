from .Piece import *
from .constantes import *

class Knight(Piece):
    '''
    :param Position: Posição da peça
    :param color : a cor da peça
    :return: Se o movimento eh valido
    '''
    def __init__(self, Position : Position , color : int ) -> None:
        super().__init__(Position, color, KNIGHT)

    '''
    :param to: casa de destino do moviento 
    :return: Se o movimento eh valido
    '''
    def IsValidMove(self, to : Position):
        drow = abs(to.getRow() - self.getPosition().getRow()) 
        dcol = abs(to.getCol() - self.getPosition().getCol())
        return ((drow == 1)and(dcol == 2)) or ((drow == 2)and(dcol == 1))