from abc import ABC, abstractmethod

from .Position import *
from interfaces import *

class Piece(PieceInterface, ABC):
    def __init__(self, Position, color, type, num=0) -> None:
        self.position = Position
        self.color = color
        self.type = type
        self.numofmoves = num
    
    def attPosition(self, pos : Position):
        self.position.setPosition(pos)
    
    def getColor(self):
        return self.color    
    
    def getType(self):
        return self.type 
   
    @abstractmethod
    def IsValidMove(self, to):
        pass