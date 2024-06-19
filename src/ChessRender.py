import numpy as np
import pygame
from typing import List

from .Position import *
from .Piece import *
from .constantes import *
from .ChessBoard import *


from .Bishop import *
from .Pawn import *
from .King import *
from .Knight import *
from .Queen import *
from .Rook import *
from .Empty import *

from interfaces import *

class ChessRender(ChessRenderInterface):
    '''
    :param board: o estado do jogo (eh att automaticamente)
    : => Desse modo, ao att. no jogo att. automaticamente na tela
    ''' 
    def __init__(self, board : ChessBoard) -> None:
        self.__shouldclose = False
        self.__board = board
        pygame.init()
        self.__screen =  pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption('Chess Game')
        self.clock = pygame.time.Clock()
        
        self.__alpha_surface = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
        
        self.__isPieceSelected = False
        self.__SelectedPiece = Position(-1,-1)
        self.__possibleDest = []


    '''
    :return: retorna a posicao da peça selecionada
    ''' 
    def getSelectedPiecePos(self) -> Position:
        return self.__SelectedPiece

    '''
    : => Metodo responsavel por att. a peça selecionada
    :param pos: Posicao da nova peça selecionada
    ''' 
    def updateSelectedPiece(self, pos : Position) -> None:
        self.__SelectedPiece = pos
        self.__isPieceSelected = not(self.__isPieceSelected)
        if self.__isPieceSelected:
            self.__possibleDest = self.__board.getMoves(self.__SelectedPiece)

    '''
    : => Metodo responsavel por fechar a janela
    '''        
    def quit(self) -> None:
        pygame.quit()


    '''
    : => Metodo responsavel por verificar e settar se a janela deve fechar
    '''   
    def setShouldclose(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__shouldclose = True
 
 
    '''
    : return: retorna se a janela deve fechar
    '''   
    def getShouldclose(self) -> bool:
        return self.__shouldclose
    
    '''
    : => Metodo auxiliar responsavel por renderizar o tabuleiro
    '''    
    def __renderBoard(self) -> None:
        for row in range (0,8):
            for col in range (0,8):
                isLight = (row + col) % 2 == 0
                rec = pygame.Rect(col*squareSize, row*squareSize,squareSize,squareSize )
                if (isLight == True):
                    pygame.draw.rect(self.__screen , light, rec)
                elif (isLight == False):
                    pygame.draw.rect(self.__screen , dark, rec)


    '''
    : => Metodo auxiliar responsavel por renderizar todas as peças no tabuleiro
    '''    
    def __renderPiece(self) -> None:
        for row in range (0,8):
            for col in range (0,8):
                piece = self.__board.getPiece(Position(row,col))
                if (piece.getType() == EMPTY):
                    continue
                piece_image = pygame.image.load( base_path + Type[piece.getType()] +'_'+ Color[piece.getColor()] + '.png')
                piece_image = pygame.transform.scale(piece_image, (squareSize, squareSize) )
                self.__screen.blit(piece_image,(col*squareSize,row*squareSize))
    

    '''
    : => Metodo auxiliar responsavel por renderizar todos destinos de um dado jogador
    '''  
    def __renderAllMoves(self) -> None:
        if self.__isPieceSelected == False:
            return
        movess = self.__board.validmoves
        if movess is not None:
            for move in movess:
                pos = Position(move.endRow , move.endCol)
                rec = pygame.Rect(pos.getCol()*squareSize, pos.getRow()*squareSize,squareSize,squareSize )
                pygame.draw.rect(self.__screen , reddd, rec)

    '''
    : => Metodo auxiliar responsavel por renderizar possiveis destinos
    '''   
    def __renderPossibleDestinations(self) -> None:
        if (self.__board.getMoveMade() == True) and (self.__isPieceSelected == False):
            self.__alpha_surface.fill((255, 255, 255,0))
        elif self.__possibleDest is not None:
            for pos in self.__possibleDest:
                rec = pygame.Rect(pos.getCol()*squareSize, pos.getRow()*squareSize,squareSize,squareSize )
                pygame.draw.rect(self.__alpha_surface , reddd , rec)
    '''
    : => Metodo responsavel por renderizar a janela + infos na tela
    '''
    def render(self) -> None:
        self.__renderBoard()
        self.__renderPossibleDestinations()
        self.__renderPiece()
        self.__screen.blit(self.__alpha_surface, (0,0))
        pygame.display.flip()
        
    def targetFps(self) -> None:
        self.clock.tick(1)
        
    '''
    : => Metodo responsavel por lidar com eventos
    :return: retorna o evendo ocorrido( ex : CLOSEGAME , UNDOMOVE , clique na tela )
    '''  
    def handle_events(self):
        waiting = True
        while waiting:
            if self.getShouldclose():
                return CLOSEGAME
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__shouldclose = True
                    return CLOSEGAME
                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_focused():
                    if event.button == 1:
                        waiting = False
                        mouse_pos = pygame.mouse.get_pos()
                        board_pos = Position( mouse_pos[1] // 100 ,mouse_pos[0] // 100   )
                        if(-1 < board_pos.getRow() < 8) and (-1 < board_pos.getCol() < 8):
                            return Position( mouse_pos[1] // 100 ,mouse_pos[0] // 100   )
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        if self.__isPieceSelected:
                            continue
                        self.__board.undoMove()
                        return UNDOMOVE
        return -1
    
