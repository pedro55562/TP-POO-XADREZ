from abc import ABC, abstractmethod

from Position import *

class Piece(ABC):
    def __init__(self, Position) -> None:
        self.position = Position
        
        
    @abstractmethod
    def IsValidMove():
        pass