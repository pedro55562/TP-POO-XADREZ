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
    
class CastlingRights():
    def __init__(self, bks, bqs, wks, wqs) -> None:
        self.blackKingSide = bks
        self.blackQueenSide = bqs
        self.whiteKingSide = wks
        self.whiteQueenSide = wqs        

class ChessBoard():
    
    def __init__(self, fen) -> None:
        self.board = np.full((8, 8), Empty(Position(0,0)))
        
        self.white_king_pos = Position(-1,-1)
        self.black_king_pos = Position(-1,-1)
        
        self.move_log = []
        

        self.enpassantPossible = Position(-1,-1) # cordinates where en passant capture is possible
        self.isenpassantAvaliable = False
                
        partes = fen.split(" ")
        board, turn, castling = partes  
              
        row = 0
        col = 0
        # Loop para ler a FEN e carregar o tabuleiro, lendo e tratando cada char individualmente
        for c in board:
            # Fim da notação FEN
            if c == ' ':
                break
            # Caso o caractere for '/', significa que devemos partir para a próxima linha
            if c == '/':
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

        self.isWhiteTurn = (turn == 'w')

        self.castlingRights = CastlingRights(False, False, False, False)

        for i in range(len(castling)):
            key = castling[i]
            if key == 'K':
                self.castlingRights.whiteKingSide = True
            if key == 'Q':
                self.castlingRights.whiteQueenSide = True
            if key == 'k':
                self.castlingRights.blackKingSide = True
            if key == 'q':
                self.castlingRights.blackQueenSide = True
        
        self.castleRightLog = []
        self.castleRightLog.append(CastlingRights(self.castlingRights.blackKingSide, self.castlingRights.blackQueenSide,
                                              self.castlingRights.whiteKingSide, self.castlingRights.whiteQueenSide) )
                     
        self.moveMade = False
        self.validmoves = self.getValidMoves()
        
        self.checkMate = False
        self.stalteMate = False #  one side has NO legal moves to make and the king is not in check => DRAW
        
        self.playermademove = False
        
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
                print(" ", self.board[i][j].numofmoves, end="")
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
        self.board[move.endRow][move.endCol].numofmoves += 1
        self.moveMade = True
        #promovendo o peao
        if move.isPawnPromotion and move.pieceMoved.getType() == PAWN:
            self.board[move.endRow][move.endCol] = Queen( Position(move.endRow, move.endCol) , move.pieceMoved.getColor() )  
        if move.isEnPassantMove:
            self.board[move.startRow][move.endCol] = Empty(Position(move.startRow, move.endCol))
        self.isenpassantAvaliable = False
        #enpassant:
        #update enpassant rights
        if(move.pieceMoved.getType() == PAWN):
            #black
            if(move.pieceMoved.getColor() == BLACKn and move.startRow == 1 and move.endRow == 3):
                self.enpassantPossible = Position(move.endRow -1, move.endCol)
                self.isenpassantAvaliable = True
            #white
            elif(move.pieceMoved.getColor() == WHITEn and move.startRow == 6 and move.endRow == 4):
                self.enpassantPossible = Position(move.endRow +1, move.endCol)
                self.isenpassantAvaliable = True
       
       #Make the castle move:
        if (move.isCastleMove):
            dir = move.endCol - move.startCol
            if dir > 0: # king side castle(to the right)
                self.board[move.endRow][5] = self.board[move.endRow][7]
                self.board[move.endRow][5].numofmoves+=1
                self.board[move.endRow][5].attPosition(Position(move.endRow, 5))
                self.board[move.endRow][7] = Empty(Position(move.endRow, 7))
            if dir < 0: # queen side caste(to the left)
                self.board[move.endRow][3] = self.board[move.endRow][0]
                self.board[move.endRow][3].numofmoves+=1
                self.board[move.endRow][3].attPosition(Position(move.endRow, 3))
                self.board[move.endRow][0] = Empty(Position(move.endRow, 0))        
        
        #muda a posicao do rei
        if(self.board[move.endRow][move.endCol].getType() == KING ):
            if (self.board[move.endRow][move.endCol].getColor() == BLACKn):
                self.black_king_pos = Position(move.endRow, move.endCol)
                
            elif (self.board[move.endRow][move.endCol].getColor() == WHITEn):
                self.white_king_pos = Position(move.endRow, move.endCol)

        self.updateCastlingRights()
        
        self.castleRightLog.append(CastlingRights(self.castlingRights.blackKingSide, self.castlingRights.blackQueenSide, 
                                               self.castlingRights.whiteKingSide, self.castlingRights.whiteQueenSide))

    def printMoveLog(self):
        if len(self.move_log) == 0:
            return False
        for i in range( len(self.move_log)):
            print(f"{i+1}) {self.move_log[i].getChessNotation()  }")
            
            
# Todo: Refatorar o codigo:
# procurar um metodo mais simples p/ dar update nos CastlingRights
# preferencialmente sem considerar numofmoves de cada piece ( atribute deve ser removido a posteriori)
# obs: deve-se considerar que os metodos makemove e undomove sao chamados varias vezes
#       e eles chamam updateCastlingRights, portanto eles afetam diretamente CastlingRights
#       o alterando apenas para uma verificação temporaria
# --> ao chamar makemove e depois dar undomove o CastlingRights deve ser o mesmo antes do chamado de makemove
    def updateCastlingRights(self):
        # Positions to check: (row, col) format
        rows = [0,7]
        cols = [0,4,7]
        temp = [(0, 0), (0, 7), (7, 0), (7, 7), (0, 4), (7, 4)]

        #for rooks
        rookrights = CastlingRights(False, False, False, False)
        #for kings
        kingrights = CastlingRights(False, False, False, False)
               
        
        for row in rows:        
            for col in cols:

                piece = self.board[row][col]
                piece_type = piece.getType()
                piece_color = piece.getColor()
                num = piece.numofmoves
                 
                #verifying for the rooks:
                if row == 0 and col == 0: # rook on the black queen-side
                    if piece_type == ROOK and piece_color == BLACKn:
                        rookrights.blackQueenSide = (num == 0)
                    elif piece_type != ROOK or piece_color != BLACKn:
                        rookrights.blackQueenSide = False
                        
                if row == 0 and col == 7: # rook on the black king-side
                    if piece_type == ROOK and piece_color == BLACKn:
                        rookrights.blackKingSide = (num == 0)
                    else:
                        rookrights.blackKingSide = False
                        
                if row == 7 and col == 0: # rook on the white queen-side
                    if piece_type == ROOK and piece_color == WHITEn:
                        rookrights.whiteQueenSide = (num == 0)
                    elif piece_type != ROOK or piece_color != WHITEn:
                        rookrights.whiteQueenSide = False
                                        
                if row == 7 and col == 7: # rook on the white king-side
                    if piece_type == ROOK and piece_color == WHITEn:
                        rookrights.whiteKingSide = (num == 0)
                    elif piece_type != ROOK or piece_color != WHITEn:
                        rookrights.whiteKingSide = False
                        
                #if the piece is a black king
                if row == 0 and col == 4:
                    if piece_color == BLACKn and piece_type == KING:
                        kingrights.blackKingSide = (num == 0)
                        kingrights.blackQueenSide = (num == 0)
                    else:
                        kingrights.blackKingSide = False
                        kingrights.blackQueenSide = False
                #if the piece is a white king
                if row == 7 and col == 4:
                    if piece_color == WHITEn and piece_type == KING:
                        kingrights.whiteKingSide = (num == 0)
                        kingrights.whiteQueenSide = (num == 0)
                    else:
                        kingrights.whiteKingSide = False
                        kingrights.whiteQueenSide = False                                    
                
        #self.castlingRights = rookrights and kingrights      
        self.castlingRights.whiteKingSide = rookrights.whiteKingSide and kingrights.whiteKingSide
        self.castlingRights.whiteQueenSide = rookrights.whiteQueenSide and kingrights.whiteQueenSide
        self.castlingRights.blackKingSide = rookrights.blackKingSide and kingrights.blackKingSide
        self.castlingRights.blackQueenSide = rookrights.blackQueenSide and kingrights.blackQueenSide
                                  
    def printCastlingRights(self):
        temp = self.castleRightLog[-1]
        print("WHITE KING SIDE:",temp.whiteKingSide)
        print("WHITE QUEEN SIDE:",temp.whiteQueenSide)
        print("BLACK KING SIDE:",temp.blackKingSide)
        print("BLACK QUEEN SIDE:",temp.blackQueenSide)
           
    def setNewValidmoves(self):
        if (self.getMoveMade()):
            self.moveMade = False
            self.validmoves = self.getValidMoves()
            return True
        return False
          
    def undoMove(self):
        if len(self.move_log) != 0:
            lastmove = self.move_log.pop()
            if lastmove.startRow == lastmove.endRow and lastmove.startCol == lastmove.endCol:
                return 
            self.board[lastmove.startRow][lastmove.startCol] = lastmove.pieceMoved
            self.board[lastmove.endRow][lastmove.endCol] = lastmove.pieceCaptured
            self.board[lastmove.startRow][lastmove.startCol].attPosition( Position(lastmove.startRow, lastmove.startCol))
            self.board[lastmove.endRow][lastmove.endCol].attPosition( Position(lastmove.endRow, lastmove.endCol))
            self.isWhiteTurn = not self.isWhiteTurn 
            self.board[lastmove.startRow][lastmove.startCol].numofmoves -= 1
            self.moveMade = True
            
            #undo enpassant move:     
            if lastmove.isEnPassantMove:
                self.board[lastmove.endRow][lastmove.endCol] = Empty(Position(lastmove.endRow, lastmove.endCol))
                self.board[lastmove.startRow][lastmove.endCol] = lastmove.pieceCaptured
                self.board[lastmove.startRow][lastmove.endCol].attPosition( Position(lastmove.startRow, lastmove.endCol))
                self.enpassantPossible = Position(lastmove.endRow, lastmove.endCol)
                self.isenpassantAvaliable = True
            
            #undo pawn advanced moves
            if lastmove.pieceMoved.getType == PAWN and abs(lastmove.startRow - lastmove.endRow) == 2:
                self.isenpassantAvaliable = False

            #Make the castle move:
            if (lastmove.isCastleMove):
                dir = lastmove.endCol - lastmove.startCol
                if dir > 0: # king side castle(to the right)
                    self.board[lastmove.endRow][7] = self.board[lastmove.endRow][5]
                    self.board[lastmove.endRow][7].numofmoves-=1
                    self.board[lastmove.endRow][7].attPosition( Position(lastmove.endRow, 7) )
                    self.board[lastmove.endRow][5] = Empty(Position(lastmove.endRow, 5))
                if dir < 0: # queen side caste(to the left)
                    self.board[lastmove.endRow][0] = self.board[lastmove.endRow][3]
                    self.board[lastmove.endRow][0].numofmoves-=1
                    self.board[lastmove.endRow][0].attPosition(Position(lastmove.endRow,0))
                    self.board[lastmove.endRow][3] = Empty(Position(lastmove.endRow, 0))        

            #update king pos                
            if(self.board[lastmove.endRow][lastmove.endCol].getType() == KING ):
                if (self.board[lastmove.endRow][lastmove.endCol].getColor() == BLACKn):
                    self.black_king_pos = Position(lastmove.endRow, lastmove.endCol)
                    
                elif (self.board[lastmove.startRow][lastmove.startCol].getColor() == WHITEn):
                    self.white_king_pos = Position(lastmove.startRow, lastmove.startCol)
 
            #update king pos
            if(self.board[lastmove.startRow][lastmove.startCol].getType() == KING ):
                if (self.board[lastmove.startRow][lastmove.startCol].getColor() == BLACKn):
                    self.black_king_pos = Position(lastmove.startRow, lastmove.startCol)
                    
                elif (self.board[lastmove.startRow][lastmove.startCol].getColor() == WHITEn):
                    self.white_king_pos = Position(lastmove.startRow, lastmove.startCol)
            
            self.checkMate = False
            self.stalteMate = False
            
            self.castleRightLog.pop()
            self.castlingRights = self.castleRightLog[-1]
            self.updateCastlingRights()
            

    def getMoveMade(self):
        return self.moveMade
            
    def movePiece(self, from_ : Position , to : Position):
        if (from_ == to):
            print("EH IGUAL NÉ")
            return False     
        self.playermademove = self.isValidMove( Move(from_,to, self.board  ))
        if( self.playermademove):
            move = Move(from_,to,self.board)
            for i in range ( len(self.validmoves)):
                if self.validmoves[i].isEnPassantMove == True:
                    if move == self.validmoves[i]:
                        move = Move(from_,to,self.board, isenpassant = True)
                if self.validmoves[i].isCastleMove == True:
                    if move == self.validmoves[i]:
                        move = Move(from_,to,self.board, isCastleMove = True)
            self.makeMove(move)
            return self.playermademove
   
#Considerando o xeque
    def isValidMove(self, move : Move):
        for i in range ( len(self.validmoves)):
            if move == self.validmoves[i]:
                return True 
        return False

#SEM considerar o xeque
    def isPossibleMove(self, from_ : Position , to : Position):
        if(self.getPiece(to).getColor() == self.getPiece(from_).getColor()):
            return False
        
        #cavalo
        if( self.getPiece(from_).getType() == KNIGHT  ):
            return self.getPiece(from_).IsValidMove(to)
        #restante
        isclear = self.isPathClear(from_, to)
        
        #peao - com en passant
        if( self.getPiece(from_).getType() == PAWN ):
            return self.getPiece(from_).IsValidMove(to, self.getPiece(to).getColor()) and isclear
        
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
               
    def getMoves(self, pos  : Position) -> List[Position]:
        list_ = []
        piece = self.getPiece(pos)
        for move in self.validmoves:
            if move.startRow == pos.getRow() and move.startCol == pos.getCol():
                list_.append(Position(move.endRow, move.endCol))
        
        
        return list_

#TODOS Movimentos considerando o xeque
    def getValidMoves(self):
        tempEnPassant = self.enpassantPossible
        tempAvaliable = self.isenpassantAvaliable
        # 1) Generate all the possibles moves
        moves = self.getAllMoves()
        # 2) For each move, make the move
        for i in range(len(moves) - 1 , -1 , -1): # por estar removendo da lista, comece por tras
            self.makeMove( moves[i] )
            self.isWhiteTurn = not self.isWhiteTurn #destrocar os turnos porque make move o trocou
            # 3) Generate all opponent's moves 
            # 4) for each of your opponent's moves, see if they atack your king
            if self.inCheck():
                # 5) if they do atack your king, it's not valid
                moves.remove(moves[i])
            self.isWhiteTurn = not self.isWhiteTurn        
            self.undoMove()
        
        if ( len(moves) == 0): #Check mate or stalemate
            if self.inCheck():
                self.checkMate = True
            else:
                self.stalteMate = True
        else:
            self.checkMate = False
            self.stalteMate = False

        self.enpassantPossible = tempEnPassant
        self.isenpassantAvaliable = tempAvaliable
        
        #if it's a castle move
        moves.extend(self.getCastleMoves())
        
        return moves
    
    #determina se o jogador atual esta em xeque 
    def inCheck(self):
        if self.isWhiteTurn:
            return self.mySquareUnderAttack(self.white_king_pos)
        else:
            return self.mySquareUnderAttack(self.black_king_pos)
    
    #verifica se o OPONENTE ataca um quadrado especifico - considera getAllMoves
    def mySquareUnderAttack(self, square : Position):
        #switch to opponent's side of view, because i wanna see their moves
        self.isWhiteTurn = not self.isWhiteTurn
        #generate all of my opponent's moves
        oppmoves = self.getAllMoves()
        #verify if any of their moves attack my square
        for moves in oppmoves:
            if moves.endRow == square.getRow() and moves.endCol == square.getCol():
                self.isWhiteTurn = not self.isWhiteTurn # switch turns back
                return True
        self.isWhiteTurn = not self.isWhiteTurn # switch turns back
        return False
   
#TODOS Movimentos SEM considerar o xeque
    def getAllMoves(self):
        moves = []
        for row in range ( len(self.board)):
            for col in range (len(self.board[row])):
                piece = self.board[row][col]
                isWhitePiece = (piece.getColor() == WHITEn)
                if (isWhitePiece == self.isWhiteTurn):
                    pos = Position(row,col)
                    
                    if ( piece.getType() == KING):
                        moves.extend(self.getKingMoves(pos))

                    #Todo: modularizacao ( implementar separadamente getPawnMoves )
                    # bugs significativos foram encontrados em relacao ao en passant
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
                                if ( dest.getRow() < 0 or dest.getRow() > 7):
                                    continue                    
                                #considering the enpassant
                                if self.isenpassantAvaliable and (dest.getRow() == self.enpassantPossible.getRow() and \
                                    dest.getCol() == self.enpassantPossible.getCol()):
                                    if abs(dr) == 1 and (abs(dc) == 1 or dc == 0):
                                        if (self.isWhiteTurn == True) and (piece.getColor() == WHITEn):
                                            moves.append(Move(pos, dest, self.board , isenpassant=True))
                                        elif (self.isWhiteTurn == False) and (piece.getColor() == BLACKn):
                                            moves.append(Move(pos, dest, self.board , isenpassant=True))
                                if self.isPossibleMove(pos,dest) == True:
                                    moves.append(Move(pos, dest, self.board ))

                    if piece.getType() == BISHOP:
                        moves.extend(self.getBishopMoves(pos))

                        
                    if piece.getType() == QUEEN:
                        moves.extend(self.getQueenMoves(pos))


                    if piece.getType() == KNIGHT:
                        moves.extend(self.getKnightMoves(pos))

                    if piece.getType() == ROOK:
                        moves.extend(self.getRookMoves(pos))

        return moves                      
    
    def getKingMoves(self,start):
        kdir = [0, 1, -1]
        moves = []
        allycolor = self.getPiece(start).getColor()
        for dr in kdir:
            for dc in kdir:
                if dr == 0 and dc == 0:
                    continue     
                dest = Position(start.getRow() + dr , start.getCol() + dc)       
                if ( dest.getCol() < 0 or dest.getCol() > 7):
                    continue
                elif ( dest.getRow() < 0 or dest.getRow() > 7):
                    continue                    
                if self.isPossibleMove(start,dest) == True:
                    moves.append(Move(start, dest, self.board ))        
        
        return moves
     
#Todo:
# ao tentar implementar encontrei bugs fundamentais envolvendo o enpassant        
# como não eh essencial, deixei para depois
# alem disso o enpassant ja havia apresentado bugs( menos relevantes ) após a chamada de undomove
    def getPawnMoves(self,pos):
        pass

    def getBishopMoves(self,start):
        dir1 = [1, -1]
        dir2 = [1, -1]
        moves = []
        for dr in dir1:
            for dc in dir2:
                crow, ccol = start.getRow() + dr, start.getCol() + dc
                while 0 <= crow < 8 and 0 <= ccol < 8:
                    dest = Position(crow, ccol)
                    if self.isPossibleMove(start, dest):
                        moves.append(Move(start, dest, self.board ))
                    crow += dr
                    ccol += dc    
        return moves
    
    def getQueenMoves(self,start):
        moves = []
        dir_row = [1, -1, 0, 0]
        dir_col = [0, 0, 1, -1]
        for dr in dir_row:
            cur_row = start.getRow() + dr
            while 0 <= cur_row < 8:
                dest = Position(cur_row, start.getCol())
                if self.isPossibleMove(start, dest):
                    moves.append(Move(start, dest, self.board ))
                else:
                    break
                cur_row += dr

        for dc in dir_col:
            cur_col = start.getCol() + dc
            while 0 <= cur_col < 8:
                dest = Position(start.getRow(), cur_col)
                if self.isPossibleMove(start, dest):
                    moves.append(Move(start, dest, self.board ))
                else:
                    break
                cur_col += dc

        dir_diag = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in dir_diag:
            cur_row, cur_col = start.getRow() + dr, start.getCol() + dc
            while 0 <= cur_row < 8 and 0 <= cur_col < 8:
                dest = Position(cur_row, cur_col)
                if self.isPossibleMove(start, dest):
                    moves.append(Move(start, dest, self.board ))
                else:
                    break
                cur_row += dr
                cur_col += dc                      
        return moves
                
    def getKnightMoves(self,start : Position):
        moves = []
        valid_moves = [(-1, 2), (-1, -2), (1, 2), (1, -2), (-2, 1), (-2, -1), (2, 1), (2, -1)]
        for dr, dc in valid_moves:
            dest = Position(start.getRow() + dr, start.getCol() + dc)
            if 0 <= dest.getRow() < 8 and 0 <= dest.getCol() < 8:
                piece = self.board[dest.getRow()][dest.getCol()]
                if self.isPossibleMove(start, dest):
                    moves.append(Move(start, dest, self.board ))
        return moves
            
    def getRookMoves(self,start):
        dir_row = [1, -1]
        dir_col = [1, -1]
        moves = []
        for dr in dir_row:
            cur_row = start.getRow() + dr
            while 0 <= cur_row < 8:
                dest = Position(cur_row, start.getCol())
                piece = self.board[dest.getRow()][dest.getCol()]
                if self.isPossibleMove(start, dest):
                    moves.append(Move(start, dest, self.board ))
                else:
                    break
                cur_row += dr

        for dc in dir_col:
            cur_col = start.getCol() + dc
            while 0 <= cur_col < 8:
                dest = Position(start.getRow(), cur_col)
                piece = self.board[dest.getRow()][dest.getCol()]
                if self.isPossibleMove(start, dest):
                    moves.append(Move(start, dest, self.board ))
                else:
                    break
                cur_col += dc       
        return moves    
    
    def getCastleMoves(self):
        if self.inCheck():
            return []
        start = Position(7,4) if self.isWhiteTurn else Position(0,4)
        allycolor = WHITEn if self.isWhiteTurn else BLACKn
        
        moves = []
        moves.extend(self.getKingSideCastle(start ,allycolor))
        moves.extend(self.getQueenSideCastle(start ,allycolor))        
        
        return moves
    
    def getKingSideCastle(self, start, allycolor):
        row = start.getRow()
        col = start.getCol()
        moves = []
        
        if self.isPathClear(start, Position(row,7)) == False:
            return []
        if self.isPathSafe(start,Position(row,col + 3)) == False:
            return []
        
        if allycolor == WHITEn and self.castlingRights.whiteKingSide == True:
            moves.append(Move(start, Position(row, 6), self.board ,isCastleMove = True ))
        if allycolor == BLACKn and self.castlingRights.blackKingSide == True: 
            moves.append(Move(start, Position(row, 6), self.board ,isCastleMove = True ))


        return moves     

        
    def getQueenSideCastle(self, start, allycolor):
        row = start.getRow()    
        col = start.getCol()
        moves = []
        
        if self.isPathClear(start, Position(row,0)) == False:
            return []
        if self.isPathSafe(start,Position(row,col - 3)) == False:
            return []
        if allycolor == WHITEn and self.castlingRights.whiteQueenSide == True:
            moves.append(Move(start, Position(row, 2), self.board,isCastleMove = True ))
        if allycolor == BLACKn and self.castlingRights.blackQueenSide == True: 
            moves.append(Move(start, Position(row, 2), self.board,isCastleMove = True ))  


        return moves     
    
    #considera apenas movs. em linhas
    def isPathSafe(self, start : Position , to : Position):
        dr = to.getRow() - start.getRow()
        dc = to.getCol() - start.getCol()
        udr = 1 if dr > 0 else -1
        udc = 1 if dc > 0 else -1
        
        curcol = start.getCol()
        currow = start.getRow() 
            
        #mov. horizontal:
        if( dr == 0 and dc != 0):
            curcol+=udc
            while(curcol != to.getCol()):
                if( self.mySquareUnderAttack(Position(currow,curcol))):
                    return False
                curcol+=udc  
        
        return True
