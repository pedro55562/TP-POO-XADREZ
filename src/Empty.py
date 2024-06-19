from .Piece import *
from .constantes import *

class Empty(Piece):
    def __init__(self, Position : Position) -> None:
        super().__init__(Position, EMPTY, EMPTY)
        
    def IsValidMove(self, to : Position) -> bool:
        return False