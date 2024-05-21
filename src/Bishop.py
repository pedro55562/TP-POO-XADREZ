from Piece import *
from constantes import *

class Bishop(Piece):
    def __init__(self, Position, color) -> None:
        super().__init__(Position, color, BISHOP)
        
    def IsValidMove(self, to):
        return True