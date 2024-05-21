from Piece import *
from constantes import *

class Queen(Piece):
    def __init__(self, Position, color) -> None:
        super().__init__(Position, color, QUEEN)
        
    def IsValidMove(self, to):
        return True