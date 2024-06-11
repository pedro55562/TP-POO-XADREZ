from abc import ABC, abstractmethod
from src.Position import *
from typing import List

class ChessRenderInterface(ABC):
    @abstractmethod  
    def getSelectedPiecePos(self) -> Position:
        pass 
    
    @abstractmethod  
    def updateSelectedPiece(self, pos : Position) -> None:
        pass 
            
    @abstractmethod  
    def quit(self) -> None:
        pass 
            
    @abstractmethod  
    def setShouldclose(self) -> None:
        pass 
            
    @abstractmethod  
    def getShouldclose(self):
        pass 
        
    @abstractmethod  
    def render(self) -> None:
        pass 
            
    @abstractmethod  
    def handle_events(self):
        pass 
            
