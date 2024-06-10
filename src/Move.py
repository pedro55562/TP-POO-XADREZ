from .Position import *
from .constantes import *

class Move:
    def __init__(self, start : Position , end : Position , board , isenpassant = False , isCastleMove = False ) -> None:
        # Armazenar Posiçoes...
        self.startRow = start.getRow()
        self.startCol = start.getCol()
        self.endRow = end.getRow()
        self.endCol = end.getCol()
        # Armazenar peças...
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveId = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol
        #Armazenar infos...
        self.isPawnPromotion = self.pieceMoved.getType() == PAWN and \
                                (self.pieceMoved.getColor() == BLACKn and self.endRow == 7) or \
                               (self.pieceMoved.getColor() == WHITEn and self.endRow == 0) 
        self.isCastleMove = isCastleMove
        self.isEnPassantMove = isenpassant
        
        if self.isEnPassantMove:
            self.pieceCaptured = board[self.startRow][self.endCol]
        
        
    def __eq__(self,other):
        if isinstance(other,Move):
            return (self.moveId == other.moveId)
        return False
    
    #implementando o rank-file notation   
    def getChessNotation(self) -> str:
        #ToDo: add things to make REAL chess notation
        return str(self.getRankFile(self.startRow, self.startCol)) +" " + str(self.getRankFile(self.endRow, self.endCol))
        
    def getRankFile(self, row, col):
        #file than rank 
        #ex: a8
        return colsTOfiles[col] + rowsTOranks[row]
