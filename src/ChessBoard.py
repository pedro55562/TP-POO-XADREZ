import numpy as np

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


class ChessBoard():
    
    def __init__(self, fen) -> None:
        self.board = np.full((8, 8), Empty(Position(0,0)))
        
        isWhiteTurn = True
        
        row = 0
        col = 0
        
        self.white_king_pos = Position(-1,-1)
        self.black_king_pos = Position(-1,-1)
        

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

    def getPiece(self,row,col):
        return self.board[row][col]

    def printBoard(self):
        # Loop para imprimir os tipos das peças no tabuleiro
        print("\n Imprimindo o tipo das peças: \n")
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                print(" ", self.board[i][j].getType(), end="")
            print()  # Avança para a próxima linha após imprimir uma linha completa do tabuleiro

        # Loop para imprimir as cores das peças no tabuleiro
        print("\n Imprimindo o tipo das peças: \n")
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                print(" ", self.board[i][j].getColor(), end="")
            print()  # Avança para a próxima linha após imprimir uma linha completa do tabuleiro

        # Imprime a posição dos reis
        print(f"Rei branco:{self.white_king_pos.getRow()} {self.white_king_pos.getCol()}")
        print(f"Rei preto:{self.black_king_pos.getRow()} {self.black_king_pos.getCol()}") 