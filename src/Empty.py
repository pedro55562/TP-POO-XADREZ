from .Piece import *
from .constantes import *

class Empty(Piece):
    def __init__(self, Position) -> None:
        super().__init__(Position, EMPTY, EMPTY)
        
    def IsValidMove(self, to):
        return False