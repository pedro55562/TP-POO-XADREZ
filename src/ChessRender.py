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

    def getSelectedPiecePos(self) -> Position:
        return self.__SelectedPiece

    def updateSelectedPiece(self, pos : Position):
        self.__SelectedPiece = pos
        self.__isPieceSelected = not(self.__isPieceSelected)
        if self.__isPieceSelected:
            self.__possibleDest = self.__board.getMoves(self.__SelectedPiece)
        
    def quit(self) -> None:
        pygame.quit()
    
    def setShouldclose(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__shouldclose = True
    
    def getShouldclose(self):
        return self.__shouldclose
        
    def renderBoard(self) -> None:
        for row in range (0,8):
            for col in range (0,8):
                isLight = (row + col) % 2 == 0
                rec = pygame.Rect(col*squareSize, row*squareSize,squareSize,squareSize )
                if (isLight == True):
                    pygame.draw.rect(self.__screen , light, rec)
                elif (isLight == False):
                    pygame.draw.rect(self.__screen , dark, rec)
    
    def renderPiece(self) -> None:
        for row in range (0,8):
            for col in range (0,8):
                piece = self.__board.getPiece(Position(row,col))
                if (piece.getType() == EMPTY):
                    continue
                piece_image = pygame.image.load( base_path + Type[piece.getType()] +'_'+ Color[piece.getColor()] + '.png')
                piece_image = pygame.transform.scale(piece_image, (squareSize, squareSize) )
                self.__screen.blit(piece_image,(col*squareSize,row*squareSize))
    
    def renderAllMoves(self) -> None:
        if self.__isPieceSelected == False:
            return
        movess = self.__board.validmoves
        if movess is not None:
            for move in movess:
                pos = Position(move.endRow , move.endCol)
                rec = pygame.Rect(pos.getCol()*squareSize, pos.getRow()*squareSize,squareSize,squareSize )
                pygame.draw.rect(self.__screen , reddd, rec)
    
    def renderPossibleDestinations(self) -> None:
        if (self.__board.getMoveMade() == True) and (self.__isPieceSelected == False):
            self.__alpha_surface.fill((255, 255, 255,0))
        elif self.__possibleDest is not None:
            for pos in self.__possibleDest:
                rec = pygame.Rect(pos.getCol()*squareSize, pos.getRow()*squareSize,squareSize,squareSize )
                pygame.draw.rect(self.__alpha_surface , reddd , rec)

    def render(self) -> None:
        self.renderBoard()
        self.renderPossibleDestinations()
        self.renderPiece()
        self.__screen.blit(self.__alpha_surface, (0,0))
        pygame.display.flip()
        
    def targetFps(self) -> None:
        self.clock.tick(1)
    
    def handle_events(self):
        waiting = True
        while waiting:
            if self.getShouldclose():
                return -1
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
    
