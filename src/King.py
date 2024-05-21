from Piece import *
from constantes import *

class King(Piece):
    def __init__(self, Position, color) -> None:
        super().__init__(Position, color, KING)
        
    def IsValidMove(self, to):
        return True