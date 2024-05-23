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

class ChessRender():
    def __init__(self, board : ChessBoard) -> None:
        self.shouldclose = False
        self.board = board
        pygame.init()
        self.screen =  pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption('Chess Game')
        self.clock = pygame.time.Clock()
        self.isPieceSelected = False
        self.SelectedPiece = Position(-1,-1)

    def getSelectedPiecePos(self) -> Position:
        return self.SelectedPiece

    def updateSelectedPiece(self, pos : Position):
        self.SelectedPiece = pos
        self.isPieceSelected = not(self.isPieceSelected)
        
    def quit(self) -> None:
        pygame.quit()
    
    def setShouldclose(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.shouldclose = True
    
    def getShouldclose(self):
        return self.shouldclose
        
    def renderBoard(self):
        for row in range (0,8):
            for col in range (0,8):
                isLight = (row + col) % 2 == 0
                rec = pygame.Rect(col*squareSize, row*squareSize,squareSize,squareSize )
                if (isLight == True):
                    pygame.draw.rect(self.screen , light, rec)
                elif (isLight == False):
                    pygame.draw.rect(self.screen , dark, rec)
    
    def renderPiece(self):
        for row in range (0,8):
            for col in range (0,8):
                piece = self.board.getPiece(Position(row,col))
                if (piece.getType() == EMPTY):
                    continue
                piece_image = pygame.image.load( base_path + Type[piece.getType()] +'_'+ Color[piece.getColor()] + '.png')
                piece_image = pygame.transform.scale(piece_image, (squareSize, squareSize) )
                self.screen.blit(piece_image,(col*squareSize,row*squareSize))
    
    def renderAllMoves(self):
        if self.isPieceSelected == False:
            return
        movess = self.board.validmoves
        if movess is not None:
            for move in movess:
                pos = Position(move.endRow , move.endCol)
                rec = pygame.Rect(pos.getCol()*squareSize, pos.getRow()*squareSize,squareSize,squareSize )
                pygame.draw.rect(self.screen , red_, rec)
    
    def renderPossibleDestinations(self):
        if self.isPieceSelected == False:
            return
        list_ = self.board.getMoves(self.SelectedPiece)
        if list_ is not None:
            for pos in list_:
                rec = pygame.Rect(pos.getCol()*squareSize, pos.getRow()*squareSize,squareSize,squareSize )
                pygame.draw.rect(self.screen , red_, rec)

    def render(self):
        self.renderBoard()
        self.renderPossibleDestinations()
        self.renderPiece()
        pygame.display.update()
        
    def targetFps(self):
        self.clock.tick(1)
    
    def HandleMouseInput(self):
        waiting = True
        while waiting:
            if self.getShouldclose():
                return -1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.shouldclose = True
                    return -1
                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_focused():
                    if event.button == 1:
                        waiting = False
                        mouse_pos = pygame.mouse.get_pos()
                        board_pos = Position( mouse_pos[1] // 100 ,mouse_pos[0] // 100   )
                        if(-1 < board_pos.getRow() < 8) and (-1 < board_pos.getCol() < 8):
                            return Position( mouse_pos[1] // 100 ,mouse_pos[0] // 100   )
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        self.board.undoMove()
                        return -2
        return -1
    
