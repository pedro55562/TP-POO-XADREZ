from abc import ABC, abstractmethod

from .Position import *
from interfaces import *

class Piece(PieceInterface, ABC):
    '''
    :param Position: Posição da peça
    :param color : a cor da peça
    :param type : tipo da peça
    :param num : numero de vezes que a peça se moveu
    '''    
    def __init__(self, Position : Position, color : int, type : int, num=0) -> None:
        self.__position = Position
        self.__color = color
        self.__type = type
        self.numofmoves = num

    '''
    :return: A posicao da peça
    '''   
    def getPosition(self) -> Position:
        return self.__position
    '''
    :param: A nova posicao da peça
    '''    
    def attPosition(self, pos : Position):
        self.__position.setPosition(pos)

    '''
    :return: A cor da peça
    '''        
    def getColor(self)->int:
        return self.__color    
    '''
    :return: O tipo da peça
    '''    
    def getType(self)-> int:
        return self.__type 

    '''
    :param to: casa de destino do moviento 
    :return: Se o movimento eh valido
    '''
    @abstractmethod
    def IsValidMove(self, to : Position) -> bool:
        pass