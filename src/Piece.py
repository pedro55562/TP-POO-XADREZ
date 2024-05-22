from abc import ABC, abstractmethod

from .Position import *

class Piece(ABC):
    def __init__(self, Position, color, type) -> None:
        self.position = Position
        self.color = color
        self.type = type
    
    def attPosition(self, pos : Position):
        self.position.setPosition(pos)
    
    def getColor(self):
        return self.color    
    
    def getType(self):
        return self.type 
   
    @abstractmethod
    def IsValidMove(self, to):
        pass