import pygame
from .constants import COLS, WHITE, BLACK, SQUARE_SIZE, ROWS
from .pieces import test_piece


class Board:
    def __init__(self):
        self.board = [[test_piece(5,4),None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None]]
        self.selected_piece = None
        
    def draw_board(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row%2, ROWS, 2):
                pygame.draw.rect(win, WHITE, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        pass
    
    def draw(self, win):
        self.draw_board(win)
        for r in range(ROWS):
            for c in range(COLS):
                piece = self.board[r][c]
                if piece != None:
                    piece.draw(win)




