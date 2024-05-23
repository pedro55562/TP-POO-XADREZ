import numpy as np
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

class Move:
    def __init__(self, start : Position , end : Position , board) -> None:
        # Armazenar Posiçoes...
        self.startRow = start.getRow()
        self.startCol = start.getCol()
        self.endRow = end.getRow()
        self.endCol = end.getCol()
        # Armazenar peças...
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveId = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol
    
    def __eq__(self,other):
        if isinstance(other,Move):
            return (self.moveId == other.moveId)
        return False
    
    #implementando o rank-file notation   
    def getChessNotation(self) -> str:
        #ToDo: add things to make REAL chess notation
        return str(self.getRankFile(self.startRow, self.startCol)) + str(self.getRankFile(self.endRow, self.endCol))
        
    def getRankFile(self, row, col):
        #file than rank 
        #ex: a8
        return colsTOfiles[col] + rowsTOranks[row]
    

class ChessBoard():
    
    def __init__(self, fen) -> None:
        self.board = np.full((8, 8), Empty(Position(0,0)))
        
        self.isWhiteTurn = True
        
        self.white_king_pos = Position(-1,-1)
        self.black_king_pos = Position(-1,-1)
        
        self.move_log = []
        
        row = 0
        col = 0
        # Loop para ler a FEN e carregar o tabuleiro, lendo e tratando cada char individualmente
        for c in fen:
            # Fim da notação FEN
            if c == ' ':
                break
            # Caso o caractere for '/', significa que devemos partir para a próxima linha
            elif c == '/':
                row += 1
                col = 0
            # Caso o caractere for um número, esse número indica a quantidade de casas vazias em sequência
            elif c.isdigit() == True:
                number_of_empty_spaces = int(c)
                # Loop para colocar no tabuleiro a quantidade de casas vazias
                for _ in range(0,number_of_empty_spaces):
                    self.board[row][col] = Empty(Position(row, col))
                    col += 1
            else:
                # Switch-case responsável por descobrir qual é a peça a ser inserida e inseri-la no tabuleiro
                piece = None
                if c == 'p':
                    piece = Pawn(Position(row,col) , BLACKn)
                elif c == 'P':
                    piece = Pawn(Position(row,col) , WHITEn)
                elif c == 'r':
                    piece = Rook(Position(row,col) , BLACKn)
                elif c == 'R':
                    piece = Rook(Position(row,col) , WHITEn)
                elif c == 'n':
                    piece = Knight(Position(row,col) , BLACKn)
                elif c == 'N':
                    piece = Knight(Position(row,col) , WHITEn)
                elif c == 'b':
                    piece = Bishop(Position(row,col) , BLACKn)
                elif c == 'B':
                    piece = Bishop(Position(row,col) , WHITEn)
                elif c == 'q':
                    piece = Queen(Position(row,col) , BLACKn)
                elif c == 'Q':
                    piece = Queen(Position(row,col) , WHITEn)
                elif c == 'k':
                    piece = King(Position(row,col) , BLACKn)
                    self.black_king_pos = Position(row, col)
                elif c == 'K':
                    piece = King(Position(row,col) , WHITEn)
                    self.white_king_pos = Position(row, col)
   
                if piece != None:
                    self.board[row][col] = piece
                    col += 1
        
        self.moveMade = False
        self.validmoves = self.getValidMoves()
        
    def getPiece(self,row,col) -> Piece:
        return self.board[row][col]

    def getPiece(self,pos : Position) -> Piece:
        return self.board[pos.getRow()][pos.getCol()]

    def printBoard(self):
        # Loop para imprimir os tipos das peças no tabuleiro
        print("\n Imprimindo o tipo das peças: \n")
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                print(" ", self.board[i][j].getType(), end="")
            print()  # Avança para a próxima linha após imprimir uma linha completa do tabuleiro

        # Loop para imprimir as cores das peças no tabuleiro
        print("\n Imprimindo a cor das peças: \n")
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                print(" ", self.board[i][j].getColor(), end="")
            print()  # Avança para a próxima linha após imprimir uma linha completa do tabuleiro

        # Imprime a posição dos reis
        print(f"Rei branco:{self.white_king_pos.getRow()} {self.white_king_pos.getCol()}")
        print(f"Rei preto:{self.black_king_pos.getRow()} {self.black_king_pos.getCol()}") 
        
    def makeMove(self, move : Move):
        self.getPiece(Position(move.startRow, move.startCol)).attPosition( Position(move.endRow, move.endCol))
        self.board[move.startRow][move.startCol] = Empty(Position(move.startRow, move.startCol))
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.move_log.append(move)
        self.isWhiteTurn = not self.isWhiteTurn 
        self.moveMade = True
        print(move.getChessNotation() )
        
    def setNewValidmoves(self):
        if (self.getMoveMade()):
            self.moveMade = False
            self.validmoves = self.getValidMoves()
            return True
        return False
          
    def undoMove(self):
        if len(self.move_log) != 0:
            lastmove = self.move_log.pop()
            self.board[lastmove.startRow][lastmove.startCol] = lastmove.pieceMoved
            self.board[lastmove.endRow][lastmove.endCol] = lastmove.pieceCaptured
            self.board[lastmove.startRow][lastmove.startCol].attPosition( Position(lastmove.startRow, lastmove.startCol))
            self.board[lastmove.endRow][lastmove.endCol].attPosition( Position(lastmove.endRow, lastmove.endCol))
            self.isWhiteTurn = not self.isWhiteTurn 
            self.moveMade = True

    def getMoveMade(self):
        return self.moveMade
            
    def movePiece(self, from_ : Position , to : Position):
        if( self.isValidMove( Move(from_,to, self.board  )) == True ):
            self.makeMove(Move(from_, to, self.board))
            #self.getPiece(from_).attPosition(to)
            #self.board[to.getRow()][to.getCol()] = self.board[from_.getRow()][from_.getCol()]
            #self.board[from_.getRow()][from_.getCol()] = Empty(from_)                
    
#Considerando o cheque
#ToDO
    def isValidMove(self, move : Move):
        if move in self.validmoves:
            return True
        return False

#SEM considerar o cheque o cheque
    def isPossibleMove(self, from_ : Position , to : Position):
        if(self.getPiece(to).getColor() == self.getPiece(from_).getColor()):
            return False
        
        #cavalo
        if( self.getPiece(from_).getType() == KNIGHT  ):
            return self.getPiece(from_).IsValidMove(to)
        
        #peao
        if( self.getPiece(from_).getType() == PAWN ):
            return self.getPiece(from_).IsValidMove(to, self.getPiece(to).getColor())
        
        
        #restante
        isclear = self.isPathClear(from_, to)
        
        valid = self.getPiece(from_).IsValidMove(to)
        
        return valid and isclear

    def isPathClear(self, start : Position , to : Position):
        dr = to.getRow() - start.getRow()
        dc = to.getCol() - start.getCol()
        udr = 1 if dr > 0 else -1
        udc = 1 if dc > 0 else -1
        
        curcol = start.getCol()
        currow = start.getRow() 
            
        #mov. horizontal ( pelas colunas):
        if( dr == 0 and dc != 0):
            curcol+=udc
            while(curcol != to.getCol()):
                if( self.getPiece(Position(currow,curcol)).getType() != EMPTY):
                    return False
                curcol+=udc      
        #mov. vertical ( pelas linhas):
        elif( dr != 0 and dc == 0):
            currow+=udr
            while(currow != to.getRow()):
                if( self.getPiece(Position(currow,curcol)).getType() != EMPTY):
                    return False
                currow+=udr
        #mov. diagonal...
        elif( abs(dr) == abs(dc)):
            curcol += udc
            currow += udr
            while(currow != to.getRow() and curcol != to.getCol()):
                if(self.getPiece(Position(currow, curcol)).getType() != EMPTY):
                    return False
                curcol += udc
                currow += udr
        else:
            return True
        return True
               
#METODO TEMPORARIO        
    def getMoves(self, pos  : Position) -> List[Position]:
        list_ = []
        piece = self.getPiece(pos)
        for move in self.validmoves:
            if move.startRow == pos.getRow() and move.startCol == pos.getCol():
                list_.append(Position(move.endRow, move.endCol))
        
        
        return list_

#TODOS Movimentos considerando o cheque
#ToDO
    def getValidMoves(self):
        return self.getAllMoves()
    
#TODOS Movimentos SEM considerar o cheque
    def getAllMoves(self):
        moves = []
        for row in range ( len(self.board)):
            for col in range (len(self.board[row])):
                piece = self.board[row][col]
                isWhitePiece = (piece.getColor() == WHITEn)
                if (isWhitePiece == self.isWhiteTurn):
                    pos = Position(row,col)
                    
                    if ( piece.getType() == KING):
                        kdir = [0, 1, -1]
                        for dr in kdir:
                            for dc in kdir:
                                if dr == 0 and dc == 0:
                                    continue
                                
                                dest = Position(pos.getRow() + dr , pos.getCol() + dc)
                                
                                if ( dest.getCol() < 0 or dest.getCol() > 7):
                                    continue
                                elif ( dest.getRow() < 0 or dest.getRow() > 7):
                                    continue                    

                                if self.isPossibleMove(pos,dest) == True:
                                    moves.append(Move(pos, dest, self.board ))

                    if ( piece.getType() == PAWN):
                        prow = [-1,-2,1,2]
                        pcol = [0,1,-1]
                        for dr in prow:
                            for dc in pcol:
                                if dr == 0 and dc == 0:
                                    continue
                                
                                dest = Position(pos.getRow() + dr , pos.getCol() + dc)
                                
                                if ( dest.getCol() < 0 or dest.getCol() > 7):
                                    continue
                                elif ( dest.getRow() < 0 or dest.getRow() > 7):
                                    continue                    

                                if self.isPossibleMove(pos,dest) == True:
                                    print(dest.getRow(),"---",dest.getCol())                    
                                    moves.append(Move(pos, dest, self.board ))

                    if piece.getType() == BISHOP:
                        dir1 = [1, -1]
                        dir2 = [1, -1]
                        
                        for dr in dir1:
                            for dc in dir2:
                                crow, ccol = pos.getRow() + dr, pos.getCol() + dc
                                while 0 <= crow < 8 and 0 <= ccol < 8:
                                    dest = Position(crow, ccol)

                                    if self.isPossibleMove(pos, dest):
                                        moves.append(Move(pos, dest, self.board ))

                                    crow += dr
                                    ccol += dc

                    if piece.getType() == QUEEN:
                        dir_row = [1, -1, 0, 0]
                        dir_col = [0, 0, 1, -1]
                        for dr in dir_row:
                            cur_row = pos.getRow() + dr
                            while 0 <= cur_row < 8:
                                dest = Position(cur_row, pos.getCol())
                                if self.isPossibleMove(pos, dest):
                                    moves.append(Move(pos, dest, self.board ))
                                else:
                                    break
                                cur_row += dr

                        for dc in dir_col:
                            cur_col = pos.getCol() + dc
                            while 0 <= cur_col < 8:
                                dest = Position(pos.getRow(), cur_col)
                                if self.isPossibleMove(pos, dest):
                                    moves.append(Move(pos, dest, self.board ))
                                else:
                                    break
                                cur_col += dc

                        dir_diag = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
                        for dr, dc in dir_diag:
                            cur_row, cur_col = pos.getRow() + dr, pos.getCol() + dc
                            while 0 <= cur_row < 8 and 0 <= cur_col < 8:
                                dest = Position(cur_row, cur_col)
                                if self.isPossibleMove(pos, dest):
                                    moves.append(Move(pos, dest, self.board ))
                                else:
                                    break
                                cur_row += dr
                                cur_col += dc

                    if piece.getType() == KNIGHT:
                        valid_moves = [(-1, 2), (-1, -2), (1, 2), (1, -2), (-2, 1), (-2, -1), (2, 1), (2, -1)]
                        for dr, dc in valid_moves:
                            dest = Position(pos.getRow() + dr, pos.getCol() + dc)
                            if 0 <= dest.getRow() < 8 and 0 <= dest.getCol() < 8:
                                if self.isPossibleMove(pos, dest) and self.getPiece(dest).getColor() != piece.getColor():
                                    moves.append(Move(pos, dest, self.board ))

                    if piece.getType() == ROOK:
                        dir_row = [1, -1]
                        dir_col = [1, -1]
                        for dr in dir_row:
                            cur_row = pos.getRow() + dr
                            while 0 <= cur_row < 8:
                                dest = Position(cur_row, pos.getCol())
                                if self.isPossibleMove(pos, dest) and self.getPiece(dest).getColor() != piece.getColor():
                                    moves.append(Move(pos, dest, self.board ))
                                else:
                                    break
                                cur_row += dr

                        for dc in dir_col:
                            cur_col = pos.getCol() + dc
                            while 0 <= cur_col < 8:
                                dest = Position(pos.getRow(), cur_col)
                                if self.isPossibleMove(pos, dest) and self.getPiece(dest).getColor() != piece.getColor():
                                    moves.append(Move(pos, dest, self.board ))
                                else:
                                    break
                                cur_col += dc
        return moves                      
                        