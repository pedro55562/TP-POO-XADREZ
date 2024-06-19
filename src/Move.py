from .Position import *
from .constantes import *

class Move:
    '''
    :param start: Casa de inicio do movimento
    :param end: Casa de destino do movimento
    :param board: o estado atual do tabuleiro
    :param isenpassant: se o movimento é um enpassant
    :param iscastlemove: se o movimento é um roque
    '''  
    def __init__(self, start : Position , end : Position , board , isenpassant : bool = False , isCastleMove : bool = False ) -> None:
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
        
    '''
    :param other: Outro moviento a ser verficado 
    :return: Se o movimenntos sao iguais
    '''          
    def __eq__(self,other) -> bool:
        if isinstance(other,Move):
            return (self.moveId == other.moveId)
        return False
    
    '''
    :return: Notação de xadrez para o movimento( ex: "e2 e4" )
    '''  
    def getChessNotation(self) -> str:
        return str(self.getRankFile(self.startRow, self.startCol)) +" " + str(self.getRankFile(self.endRow, self.endCol))

    '''
    :param row: A linha
    :param col: A coluna 
    :return: A posicao na notação do xadrez
    '''          
    def getRankFile(self, row : int, col : int) -> str:
        return colsTOfiles[col] + rowsTOranks[row]
