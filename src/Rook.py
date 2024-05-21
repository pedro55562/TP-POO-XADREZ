from Piece import *
from constantes import *

class Rook(Piece):
    def __init__(self, Position, color) -> None:
        super().__init__(Position, color, ROOK)
        
    def IsValidMove(self, to):
        return True