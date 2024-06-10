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
        self.shouldclose = False
        self.board = board
        pygame.init()
        self.screen =  pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption('Chess Game')
        self.clock = pygame.time.Clock()
        
        self.alpha_surface = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
        
        self.isPieceSelected = False
        self.SelectedPiece = Position(-1,-1)
        self.possibleDest = []

    def getSelectedPiecePos(self) -> Position:
        return self.SelectedPiece

    def updateSelectedPiece(self, pos : Position):
        self.SelectedPiece = pos
        self.isPieceSelected = not(self.isPieceSelected)
        if self.isPieceSelected:
            self.possibleDest = self.board.getMoves(self.SelectedPiece)
        
    def quit(self) -> None:
        pygame.quit()
    
    def setShouldclose(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.shouldclose = True
    
    def getShouldclose(self):
        return self.shouldclose
        
    def renderBoard(self) -> None:
        for row in range (0,8):
            for col in range (0,8):
                isLight = (row + col) % 2 == 0
                rec = pygame.Rect(col*squareSize, row*squareSize,squareSize,squareSize )
                if (isLight == True):
                    pygame.draw.rect(self.screen , light, rec)
                elif (isLight == False):
                    pygame.draw.rect(self.screen , dark, rec)
    
    def renderPiece(self) -> None:
        for row in range (0,8):
            for col in range (0,8):
                piece = self.board.getPiece(Position(row,col))
                if (piece.getType() == EMPTY):
                    continue
                piece_image = pygame.image.load( base_path + Type[piece.getType()] +'_'+ Color[piece.getColor()] + '.png')
                piece_image = pygame.transform.scale(piece_image, (squareSize, squareSize) )
                self.screen.blit(piece_image,(col*squareSize,row*squareSize))
    
    def renderAllMoves(self) -> None:
        if self.isPieceSelected == False:
            return
        movess = self.board.validmoves
        if movess is not None:
            for move in movess:
                pos = Position(move.endRow , move.endCol)
                rec = pygame.Rect(pos.getCol()*squareSize, pos.getRow()*squareSize,squareSize,squareSize )
                pygame.draw.rect(self.screen , reddd, rec)
    
    def renderPossibleDestinations(self) -> None:
        if (self.board.getMoveMade() == True) and (self.isPieceSelected == False):
            self.alpha_surface.fill((255, 255, 255,0))
        elif self.possibleDest is not None:
            for pos in self.possibleDest:
                rec = pygame.Rect(pos.getCol()*squareSize, pos.getRow()*squareSize,squareSize,squareSize )
                pygame.draw.rect(self.alpha_surface , reddd , rec)

    def render(self) -> None:
        self.renderBoard()
        self.renderPossibleDestinations()
        self.renderPiece()
        self.screen.blit(self.alpha_surface, (0,0))
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
                    self.shouldclose = True
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
                        if self.isPieceSelected:
                            continue
                        self.board.undoMove()
                        return UNDOMOVE
        return -1
    
