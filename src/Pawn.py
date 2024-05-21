from Piece import *
from constantes import *

class Pawn(Piece):
    def __init__(self, Position, color) -> None:
        super().__init__(Position, color, PAWN)
        
    def IsValidMove(self, to):
        return True