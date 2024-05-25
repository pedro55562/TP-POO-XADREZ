import numpy as np
import random

from typing import List

from .Position import *
from .Piece import *
from .constantes import *

from .Bishop import *
from .Pawn import *
from .King import *
from .Knight import *
from .Queen import *
from .Rook import *
from .Empty import *
from .ChessBoard import *

class Chessbot():
    def __init__(self, board : ChessBoard) -> None:
        self.board = board
        
    def randomMove(self):
        return random.choice(self.board.getValidMoves())
    
    def findGoodMove(self):
        pass
    
    
    
    def moveGenTest(self, depth : int):
        num = 0
        moves = self.board.getValidMoves()
        if depth == 0:
            return 1
        
        for move in moves:
            self.board.makeMove(move)
            num += self.moveGenTest(depth - 1)
            self.board.undoMove()
            
        return num
            
