from .Piece import *
from .constantes import *

class Queen(Piece):
    '''
    :param Position: Posição da peça
    :param color : a cor da peça
    '''
    def __init__(self, Position : Position, color : int) -> None:
        super().__init__(Position, color, QUEEN)

    '''
    :param to: casa de destino do moviento 
    :return: Se o movimento eh valido
    '''        
    def IsValidMove(self, to : Position ) -> bool:
        drow = abs(to.getRow() - self.getPosition().getRow()) 
        dcol = abs(to.getCol() - self.getPosition().getCol())
        return (drow == dcol)or((drow != 0) and (dcol == 0))or((drow == 0) and (dcol != 0))