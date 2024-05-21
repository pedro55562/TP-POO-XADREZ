from Piece import *
from constantes import *

class Knight(Piece):
    def __init__(self, Position, color) -> None:
        super().__init__(Position, color, KNIGHT)
        
    def IsValidMove(self, to):
        return True