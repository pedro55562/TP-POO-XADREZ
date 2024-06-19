import numpy as np
from typing import List

from interfaces import *

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
from .Move import *
    
class CastlingRights():
    def __init__(self, bks, bqs, wks, wqs) -> None:
        self.blackKingSide = bks
        self.blackQueenSide = bqs
        self.whiteKingSide = wks
        self.whiteQueenSide = wqs        

class ChessBoard(ChessBoardInterface):
    '''
    :param fen: Fen o qual o tabuleiro deve ser inicializado
    : vide: https://www.chess.com/terms/fen-chess
    '''     
    def __init__(self, fen : str) -> None:
        self.__board = np.full((8, 8), Empty(Position(0,0)))
        
        self.__white_king_pos = Position(-1,-1)
        self.__black_king_pos = Position(-1,-1)
        
        self.__move_log = []
        

        self.__enpassantPossible = Position(-1,-1)
        self.__isenpassantAvaliable = False
                
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
                    self.__board[row][col] = Empty(Position(row, col))
                    col += 1
            else:
                #if responsável por descobrir qual é a peça a ser inserida e inseri-la no tabuleiro
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
                    self.__black_king_pos = Position(row, col)
                elif c == 'K':
                    piece = King(Position(row,col) , WHITEn)
                    self.__white_king_pos = Position(row, col)
   
                if piece != None:
                    self.__board[row][col] = piece
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
        self.stalteMate = False #empate => NÃO esta em check e nao tem movs. validos
        
        self.playermademove = False

    '''
    :param row: linha da peca
    :parm col: coluna da peca
    :return: retorna a peça nessa posicao
    '''          
    def getPiece(self,row :int ,col : int) -> Piece:
        return self.__board[row][col]

    '''
    :param pos ; a posicao da peça
    :return: retorna a peça nessa posicao
    ''' 
    def getPiece(self,pos : Position) -> Piece:
        return self.__board[pos.getRow()][pos.getCol()]
    
    '''
    : => Imprime o estado atual do tabuleiro no terminal
    '''  
    def printBoard(self) -> None:
        print("\n Imprimindo o tipo das peças: \n")
        for i in range(len(self.__board)):
            for j in range(len(self.__board[i])):
                print(" ", self.__board[i][j].getType(), end="")
            print()  

        print("\n Imprimindo a cor das peças: \n")
        for i in range(len(self.__board)):
            for j in range(len(self.__board[i])):
                print(" ", self.__board[i][j].numofmoves, end="")
            print()  

        print(f"Rei branco:{self.__white_king_pos.getRow()} {self.__white_king_pos.getCol()}")
        print(f"Rei preto:{self.__black_king_pos.getRow()} {self.__black_king_pos.getCol()}") 


    '''
    : param Move: Movimento a ser realizado
    '''       
    def __makeMove(self, move : Move) -> None: 
        self.getPiece(Position(move.startRow, move.startCol)).attPosition( Position(move.endRow, move.endCol))
        self.__board[move.startRow][move.startCol] = Empty(Position(move.startRow, move.startCol))
        self.__board[move.endRow][move.endCol] = move.pieceMoved
        self.__move_log.append(move)
        self.isWhiteTurn = not self.isWhiteTurn 
        self.__board[move.endRow][move.endCol].numofmoves += 1
        self.moveMade = True
        #promovendo o peao
        if move.isPawnPromotion and move.pieceMoved.getType() == PAWN:
            self.__board[move.endRow][move.endCol] = Queen( Position(move.endRow, move.endCol) , move.pieceMoved.getColor() )  
        if move.isEnPassantMove:
            self.__board[move.startRow][move.endCol] = Empty(Position(move.startRow, move.endCol))
        self.__isenpassantAvaliable = False
        #enpassant:
        #update enpassant rights
        if(move.pieceMoved.getType() == PAWN):
            #black
            if(move.pieceMoved.getColor() == BLACKn and move.startRow == 1 and move.endRow == 3):
                self.__enpassantPossible = Position(move.endRow -1, move.endCol)
                self.__isenpassantAvaliable = True
            #white
            elif(move.pieceMoved.getColor() == WHITEn and move.startRow == 6 and move.endRow == 4):
                self.__enpassantPossible = Position(move.endRow +1, move.endCol)
                self.__isenpassantAvaliable = True
       
       #Make the castle move:
        if (move.isCastleMove):
            dir = move.endCol - move.startCol
            if dir > 0: # king side castle(to the right)
                self.__board[move.endRow][5] = self.__board[move.endRow][7]
                self.__board[move.endRow][5].numofmoves+=1
                self.__board[move.endRow][5].attPosition(Position(move.endRow, 5))
                self.__board[move.endRow][7] = Empty(Position(move.endRow, 7))
            if dir < 0: # queen side caste(to the left)
                self.__board[move.endRow][3] = self.__board[move.endRow][0]
                self.__board[move.endRow][3].numofmoves+=1
                self.__board[move.endRow][3].attPosition(Position(move.endRow, 3))
                self.__board[move.endRow][0] = Empty(Position(move.endRow, 0))        
        
        #muda a posicao do rei
        if(self.__board[move.endRow][move.endCol].getType() == KING ):
            if (self.__board[move.endRow][move.endCol].getColor() == BLACKn):
                self.__black_king_pos = Position(move.endRow, move.endCol)
                
            elif (self.__board[move.endRow][move.endCol].getColor() == WHITEn):
                self.__white_king_pos = Position(move.endRow, move.endCol)

        self.updateCastlingRights()
        
        self.castleRightLog.append(CastlingRights(self.castlingRights.blackKingSide, self.castlingRights.blackQueenSide, 
                                               self.castlingRights.whiteKingSide, self.castlingRights.whiteQueenSide))
    
    '''
    : => Imprime o historico de movimentos no terminal
    ''' 
    def printMoveLog(self) -> None:
        if len(self.__move_log) == 0:
            return False
        for i in range( len(self.__move_log)):
            print(f"{i+1}) {self.__move_log[i].getChessNotation()  }")

    '''
    : => Atualiza os direitos ao roque
    '''             
    def updateCastlingRights(self) -> None:
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

                piece = self.__board[row][col]
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

    '''
    : => Imprime os direitos ao roque no terminal
    '''                                    
    def printCastlingRights(self)-> None:
        temp = self.castleRightLog[-1]
        print("WHITE KING SIDE:",temp.whiteKingSide)
        print("WHITE QUEEN SIDE:",temp.whiteQueenSide)
        print("BLACK KING SIDE:",temp.blackKingSide)
        print("BLACK QUEEN SIDE:",temp.blackQueenSide)

    '''
    : => Se um moiemento foi realizadom, att. a lista de movs. validos
    : return: se a lista foi atualizada
    '''             
    def setNewValidmoves(self) -> bool:
        if (self.getMoveMade()):
            self.moveMade = False
            self.validmoves = self.getValidMoves()
            return True
        return False

    '''
    : => Desfaz o ultimo movimento
    '''            
    def undoMove(self) -> None:
        if len(self.__move_log) != 0:
            lastmove = self.__move_log.pop()
            if lastmove.startRow == lastmove.endRow and lastmove.startCol == lastmove.endCol:
                return 
            self.__board[lastmove.startRow][lastmove.startCol] = lastmove.pieceMoved
            self.__board[lastmove.endRow][lastmove.endCol] = lastmove.pieceCaptured
            self.__board[lastmove.startRow][lastmove.startCol].attPosition( Position(lastmove.startRow, lastmove.startCol))
            self.__board[lastmove.endRow][lastmove.endCol].attPosition( Position(lastmove.endRow, lastmove.endCol))
            self.isWhiteTurn = not self.isWhiteTurn 
            self.__board[lastmove.startRow][lastmove.startCol].numofmoves -= 1
            self.moveMade = True
            
            #undo enpassant move:     
            if lastmove.isEnPassantMove:
                self.__board[lastmove.endRow][lastmove.endCol] = Empty(Position(lastmove.endRow, lastmove.endCol))
                self.__board[lastmove.startRow][lastmove.endCol] = lastmove.pieceCaptured
                self.__board[lastmove.startRow][lastmove.endCol].attPosition( Position(lastmove.startRow, lastmove.endCol))
                self.__enpassantPossible = Position(lastmove.endRow, lastmove.endCol)
                self.__isenpassantAvaliable = True
            
            #undo double pawn push
            if lastmove.pieceMoved.getType == PAWN and abs(lastmove.startRow - lastmove.endRow) == 2:
                self.__isenpassantAvaliable = False
                self.__enpassantPossible = Position(-1,-1)

            if (lastmove.isCastleMove):
                dir = lastmove.endCol - lastmove.startCol
                if dir > 0: # king side castle(to the right)
                    self.__board[lastmove.endRow][7] = self.__board[lastmove.endRow][5]
                    self.__board[lastmove.endRow][7].numofmoves-=1
                    self.__board[lastmove.endRow][7].attPosition( Position(lastmove.endRow, 7) )
                    self.__board[lastmove.endRow][5] = Empty(Position(lastmove.endRow, 5))
                if dir < 0: # queen side caste(to the left)
                    self.__board[lastmove.endRow][0] = self.__board[lastmove.endRow][3]
                    self.__board[lastmove.endRow][0].numofmoves-=1
                    self.__board[lastmove.endRow][0].attPosition(Position(lastmove.endRow,0))
                    self.__board[lastmove.endRow][3] = Empty(Position(lastmove.endRow, 0))        

            #update king pos                
            if(self.__board[lastmove.endRow][lastmove.endCol].getType() == KING ):
                if (self.__board[lastmove.endRow][lastmove.endCol].getColor() == BLACKn):
                    self.__black_king_pos = Position(lastmove.endRow, lastmove.endCol)
                    
                elif (self.__board[lastmove.startRow][lastmove.startCol].getColor() == WHITEn):
                    self.__white_king_pos = Position(lastmove.startRow, lastmove.startCol)
 
            #update king pos
            if(self.__board[lastmove.startRow][lastmove.startCol].getType() == KING ):
                if (self.__board[lastmove.startRow][lastmove.startCol].getColor() == BLACKn):
                    self.__black_king_pos = Position(lastmove.startRow, lastmove.startCol)
                    
                elif (self.__board[lastmove.startRow][lastmove.startCol].getColor() == WHITEn):
                    self.__white_king_pos = Position(lastmove.startRow, lastmove.startCol)
            
            self.checkMate = False
            self.stalteMate = False
            
            self.castleRightLog.pop()
            self.castlingRights = self.castleRightLog[-1]
            self.updateCastlingRights()
            
    '''
    : return: se um movimento foi realizado
    '''  
    def getMoveMade(self) -> bool:
        return self.moveMade

    '''
    : param from_: posicao de inicio
    : param to : posicao de destino
    : return: Se o movimento foi realizado com sucesso
    '''            
    def movePiece(self, from_ : Position , to : Position) -> bool:
        if (from_ == to):
            return False     
        self.playermademove = self.isValidMove( Move(from_,to, self.__board  ))
        if( self.playermademove):
            move = Move(from_,to,self.__board)
            for i in range ( len(self.validmoves)):
                if self.validmoves[i].isEnPassantMove == True:
                    if move == self.validmoves[i]:
                        move = Move(from_,to,self.__board, isenpassant = True)
                if self.validmoves[i].isCastleMove == True:
                    if move == self.validmoves[i]:
                        move = Move(from_,to,self.__board, isCastleMove = True)
            self.__makeMove(move)
            return self.playermademove

    '''
    : param move: movimento a ser realizado
    : return: Se o movimento eh valido( considera o check )
    '''         
    def isValidMove(self, move : Move) -> bool:
        for i in range ( len(self.validmoves)):
            if move == self.validmoves[i]:
                return True 
        return False

    '''
    : param from_: posicao de inicio
    : param to : posicao de destino
    : return: Se o movimento eh possivel( sem consideram o check)
    ''' 
    def __isPossibleMove(self, from_ : Position , to : Position) -> bool:
        if(self.getPiece(to).getColor() == self.getPiece(from_).getColor()):
            return False
        
        #cavalo
        if( self.getPiece(from_).getType() == KNIGHT  ):
            return self.getPiece(from_).IsValidMove(to)
        #restante
        isclear = self.__isPathClear(from_, to)
        
        #peao - com en passant
        if( self.getPiece(from_).getType() == PAWN ):
            return self.getPiece(from_).IsValidMove(to, self.getPiece(to).getColor()) and isclear
        
        valid = self.getPiece(from_).IsValidMove(to)
        
        return valid and isclear

    '''
    : param from_: posicao de inicio
    : param to : posicao de destino
    : return: Se o caminho esntre 2 posicoes esta limpo( nao possui pecas no caminho)
    ''' 
    def __isPathClear(self, start : Position , to : Position):
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
    
    '''           
    : param pos: posicao da peça
    : return: Retorna uma lista de desinos que uma peça em uma dada pos pode ir realizar
    ''' 
    def getMoves(self, pos  : Position) -> List[Position]:
        list_ = []
        piece = self.getPiece(pos)
        for move in self.validmoves:
            if move.startRow == pos.getRow() and move.startCol == pos.getCol():
                list_.append(Position(move.endRow, move.endCol))
        
        
        return list_

    '''           
    : return: Uma lista com todos movimentos validos( considerando o check)
    ''' 
    def getValidMoves(self) -> List[Move]:
        tempEnPassant = self.__enpassantPossible
        tempAvaliable = self.__isenpassantAvaliable
        moves = self.__getAllMoves()
        for i in range(len(moves) - 1 , -1 , -1): 
            self.__makeMove( moves[i] )
            self.isWhiteTurn = not self.isWhiteTurn 
            if self.__inCheck():
                moves.remove(moves[i])
            self.isWhiteTurn = not self.isWhiteTurn        
            self.undoMove()
        
        if ( len(moves) == 0): 
            if self.__inCheck():
                self.checkMate = True
            else:
                self.stalteMate = True
        else:
            self.checkMate = False
            self.stalteMate = False

        self.__enpassantPossible = tempEnPassant
        self.__isenpassantAvaliable = tempAvaliable
        
        moves.extend(self.__getCastleMoves())
        
        return moves
    

    '''           
    : return: se jogador atual esta em check
    ''' 
    def __inCheck(self) -> bool:
        if self.isWhiteTurn:
            return self.__mySquareUnderAttack(self.__white_king_pos)
        else:
            return self.__mySquareUnderAttack(self.__black_king_pos)

    ''' 
    : param square: posicao no tabuleiro          
    : return: se o oponente atk um dado square
    '''    
    def __mySquareUnderAttack(self, square : Position) -> bool:
        self.isWhiteTurn = not self.isWhiteTurn
        oppmoves = self.__getAllMoves()
        for moves in oppmoves:
            if moves.endRow == square.getRow() and moves.endCol == square.getCol():
                self.isWhiteTurn = not self.isWhiteTurn
                return True
        self.isWhiteTurn = not self.isWhiteTurn 
        return False
   
    ''' 
    : return: todos movimentos possiveis( sem consideram o check)
    '''    
    def __getAllMoves(self) -> List[Move]:
        moves = []
        for row in range ( len(self.__board)):
            for col in range (len(self.__board[row])):
                piece = self.__board[row][col]
                isWhitePiece = (piece.getColor() == WHITEn)
                if (isWhitePiece == self.isWhiteTurn):
                    pos = Position(row,col)
                    
                    if ( piece.getType() == KING):
                        moves.extend(self.__getKingMoves(pos))

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
                                if self.__isenpassantAvaliable and (dest.getRow() == self.__enpassantPossible.getRow() and \
                                    dest.getCol() == self.__enpassantPossible.getCol()):
                                    if abs(dr) == 1 and (abs(dc) == 1 or dc == 0):
                                        if (self.isWhiteTurn == True) and (piece.getColor() == WHITEn):
                                            moves.append(Move(pos, dest, self.__board , isenpassant=True))
                                        elif (self.isWhiteTurn == False) and (piece.getColor() == BLACKn):
                                            moves.append(Move(pos, dest, self.__board , isenpassant=True))
                                if self.__isPossibleMove(pos,dest) == True:
                                    moves.append(Move(pos, dest, self.__board ))

                    if piece.getType() == BISHOP:
                        moves.extend(self.__getBishopMoves(pos))

                        
                    if piece.getType() == QUEEN:
                        moves.extend(self.__getQueenMoves(pos))


                    if piece.getType() == KNIGHT:
                        moves.extend(self.__getKnightMoves(pos))

                    if piece.getType() == ROOK:
                        moves.extend(self.__getRookMoves(pos))

        return moves                      

    ''' 
    : param start: A posicao a partir da qual os movs. serao gerados 
    : return: todos os movimentos do rei a partir de uma dada posicao
    '''   
    def __getKingMoves(self,start : Position) -> List[Move]:
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
                if self.__isPossibleMove(start,dest) == True:
                    moves.append(Move(start, dest, self.__board ))        
        
        return moves

    ''' 
    : param start: A posicao a partir da qual os movs. serao gerados 
    : return: todos os movimentos do bispo a partir de uma dada posicao
    '''       
    def __getBishopMoves(self,start : Position)  -> List[Move]:
        dir1 = [1, -1]
        dir2 = [1, -1]
        moves = []
        for dr in dir1:
            for dc in dir2:
                crow, ccol = start.getRow() + dr, start.getCol() + dc
                while 0 <= crow < 8 and 0 <= ccol < 8:
                    dest = Position(crow, ccol)
                    if self.__isPossibleMove(start, dest):
                        moves.append(Move(start, dest, self.__board ))
                    crow += dr
                    ccol += dc    
        return moves

    ''' 
    : param start: A posicao a partir da qual os movs. serao gerados 
    : return: todos os movimentos da rainha a partir de uma dada posicao
    '''  
    def __getQueenMoves(self,start : Position) -> List[Move]:
        moves = []
        dir_row = [1, -1, 0, 0]
        dir_col = [0, 0, 1, -1]
        for dr in dir_row:
            cur_row = start.getRow() + dr
            while 0 <= cur_row < 8:
                dest = Position(cur_row, start.getCol())
                if self.__isPossibleMove(start, dest):
                    moves.append(Move(start, dest, self.__board ))
                else:
                    break
                cur_row += dr

        for dc in dir_col:
            cur_col = start.getCol() + dc
            while 0 <= cur_col < 8:
                dest = Position(start.getRow(), cur_col)
                if self.__isPossibleMove(start, dest):
                    moves.append(Move(start, dest, self.__board ))
                else:
                    break
                cur_col += dc

        dir_diag = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in dir_diag:
            cur_row, cur_col = start.getRow() + dr, start.getCol() + dc
            while 0 <= cur_row < 8 and 0 <= cur_col < 8:
                dest = Position(cur_row, cur_col)
                if self.__isPossibleMove(start, dest):
                    moves.append(Move(start, dest, self.__board ))
                else:
                    break
                cur_row += dr
                cur_col += dc                      
        return moves

    ''' 
    : param start: A posicao a partir da qual os movs. serao gerados 
    : return: todos os movimentos do cavalo a partir de uma dada posicao
    '''                
    def __getKnightMoves(self,start : Position) -> List[Move]:
        moves = []
        valid_moves = [(-1, 2), (-1, -2), (1, 2), (1, -2), (-2, 1), (-2, -1), (2, 1), (2, -1)]
        for dr, dc in valid_moves:
            dest = Position(start.getRow() + dr, start.getCol() + dc)
            if 0 <= dest.getRow() < 8 and 0 <= dest.getCol() < 8:
                piece = self.__board[dest.getRow()][dest.getCol()]
                if self.__isPossibleMove(start, dest):
                    moves.append(Move(start, dest, self.__board ))
        return moves

    ''' 
    : param start: A posicao a partir da qual os movs. serao gerados 
    : return: todos os movimentos da torre a partir de uma dada posicao
    '''             
    def __getRookMoves(self,start) -> List[Move]:
        dir_row = [1, -1]
        dir_col = [1, -1]
        moves = []
        for dr in dir_row:
            cur_row = start.getRow() + dr
            while 0 <= cur_row < 8:
                dest = Position(cur_row, start.getCol())
                piece = self.__board[dest.getRow()][dest.getCol()]
                if self.__isPossibleMove(start, dest):
                    moves.append(Move(start, dest, self.__board ))
                else:
                    break
                cur_row += dr

        for dc in dir_col:
            cur_col = start.getCol() + dc
            while 0 <= cur_col < 8:
                dest = Position(start.getRow(), cur_col)
                piece = self.__board[dest.getRow()][dest.getCol()]
                if self.__isPossibleMove(start, dest):
                    moves.append(Move(start, dest, self.__board ))
                else:
                    break
                cur_col += dc       
        return moves    

    ''' 
    : return: todos os movimentos de roque
    '''     
    def __getCastleMoves(self) -> List[Move]:
        if self.__inCheck():
            return []
        start = Position(7,4) if self.isWhiteTurn else Position(0,4)
        allycolor = WHITEn if self.isWhiteTurn else BLACKn
        
        moves = []
        moves.extend(self.__getKingSideCastle(start ,allycolor))
        moves.extend(self.__getQueenSideCastle(start ,allycolor))        
        
        return moves
  
    ''' 
    : parm start: posicao do rei de inicio
    : param allycolor: cor dos aliados
    : return: todos os movimentos de p/ o lado do rei
    '''    
    def __getKingSideCastle(self, start : Position, allycolor : int):
        row = start.getRow()
        col = start.getCol()
        moves = []
        
        if self.__isPathClear(start, Position(row,7)) == False:
            return []
        if self.__isPathSafe(start,Position(row,col + 3)) == False:
            return []
        
        if allycolor == WHITEn and self.castlingRights.whiteKingSide == True:
            moves.append(Move(start, Position(row, 6), self.__board ,isCastleMove = True ))
        if allycolor == BLACKn and self.castlingRights.blackKingSide == True: 
            moves.append(Move(start, Position(row, 6), self.__board ,isCastleMove = True ))


        return moves     

    ''' 
    : parm start: posicao do rei de inicio
    : param allycolor: cor dos aliados
    : return: todos os movimentos de p/ o lado da rainha
    '''           
    def __getQueenSideCastle(self, start : Position , allycolor : int) -> List[Move]:
        row = start.getRow()    
        col = start.getCol()
        moves = []
        
        if self.__isPathClear(start, Position(row,0)) == False:
            return []
        if self.__isPathSafe(start,Position(row,col - 3)) == False:
            return []
        if allycolor == WHITEn and self.castlingRights.whiteQueenSide == True:
            moves.append(Move(start, Position(row, 2), self.__board,isCastleMove = True ))
        if allycolor == BLACKn and self.castlingRights.blackQueenSide == True: 
            moves.append(Move(start, Position(row, 2), self.__board,isCastleMove = True ))  


        return moves     
   
    ''' 
    : param start: posicao de inicio
    : param to: posicao de destino
    : return: se o caminho entre start e to eh seguro
    '''        
    def __isPathSafe(self, start : Position , to : Position) -> bool:
        dr = to.getRow() - start.getRow()
        dc = to.getCol() - start.getCol()
        udr = 1 if dr > 0 else -1
        udc = 1 if dc > 0 else -1
        
        curcol = start.getCol()
        currow = start.getRow() 
            
        if( dr == 0 and dc != 0):
            curcol+=udc
            while(curcol != to.getCol()):
                if( self.__mySquareUnderAttack(Position(currow,curcol))):
                    return False
                curcol+=udc  
        
        return True

