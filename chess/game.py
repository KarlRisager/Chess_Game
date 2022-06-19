import pygame

from chess.pieces import Pawn, Rook, Bishop, Knight, King, Queen
from .constants import BLACK, WHITE, ROWS, COLS
from.board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        pygame.display.update()
    
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
    
    def reset(self):
        self._init()
    
    def move(self, piece, row, col):
        self.board.move(piece, row, col)
    
    def get_valid_moves(self, piece):
        row = piece.row
        col = piece.col
        valid_list = []
        type = type(piece).__name__
        if type == 'Pawn':
            valid_list.append((-1,0))
            if piece.unmoved:
                valid_list.append((-2,0))
            if self.board.get_piece(row-1,col-1)!=None:
                valid_list.append((-1,-1))
            if self.board.get_piece(row-1,col+1)!=None:
                valid_list.append((-1,1))
        elif type == 'Rook':
            for r in range(ROWS):
                valid_list.append((r,0))
                valid_list.append((-r,0))
            for c in range(COLS):
                valid_list.append((0,c))
                valid_list.append((0,-c))
        elif type == 'Bishop':
            pass
        elif type == 'Knight':
            pass
        elif type == 'King':
            pass
        elif type == 'Queen':
            pass

