from abc import ABC, abstractmethod

from .Position import *
from interfaces import *

class Piece(PieceInterface, ABC):
    def __init__(self, Position, color, type, num=0) -> None:
        self.__position = Position
        self.__color = color
        self.__type = type
        self.numofmoves = num

    def getPosition(self):
        return self.__position

    def attPosition(self, pos : Position):
        self.__position.setPosition(pos)
    
    def getColor(self):
        return self.__color    
    
    def getType(self):
        return self.__type 
   
    @abstractmethod
    def IsValidMove(self, to):
        pass