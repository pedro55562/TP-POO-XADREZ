from abc import ABC, abstractmethod
from src.Position import *
from src.Move import *
from typing import List

class PieceInterface(ABC):

    @abstractmethod
    def attPosition(self, pos : Position):
        pass 
        
    @abstractmethod    
    def getColor(self):
        pass 

    @abstractmethod    
    def getType(self):
        pass 

    @abstractmethod
    def getPosition(self):
        pass
    
    @abstractmethod
    def IsValidMove(self, to):
        pass