from abc import ABC, abstractmethod
from src.Position import *
from src.Move import *
from typing import List

class ChessBoardInterface(ABC):
        
    @abstractmethod    
    def makeMove(self, move : Move):
        pass

    @abstractmethod      
    def undoMove(self):
        pass
    
    @abstractmethod 
    def movePiece(self, from_ : Position , to : Position):
        pass
    
    @abstractmethod 
    def isValidMove(self, move : Move):
        pass
        
    @abstractmethod 
    def getValidMoves(self):
        pass
    
    @abstractmethod 
    def getMoves(self, pos  : Position) -> List[Position]:
        pass