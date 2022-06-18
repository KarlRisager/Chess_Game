import pygame
from .constants import COLS, WHITE, BLACK, BROWN, SQUARE_SIZE, ROWS
from .pieces import Pawn


class Board:
    def __init__(self):
        self.pieces = [Pawn(6,0, WHITE),Pawn(6,1, WHITE),Pawn(6,2, WHITE),Pawn(6,3, WHITE),Pawn(6,4, WHITE),Pawn(6,5, WHITE),Pawn(6,6, WHITE),Pawn(6,7, WHITE),
        Pawn(1,0, BLACK),Pawn(1,1, BLACK),Pawn(1,2, BLACK),Pawn(1,3, BLACK),Pawn(1,4, BLACK),Pawn(1,5, BLACK),Pawn(1,6, BLACK),Pawn(1,7, BLACK)]
        self.selected_piece = None
        
    def draw_board(self, win):
        win.fill(BROWN)
        for row in range(ROWS):
            for col in range(row%2, ROWS, 2):
                pygame.draw.rect(win, WHITE, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        pass
    
    def draw(self, win):
        self.draw_board(win)
        for piece in self.pieces:
                if piece != None:
                    piece.draw(win)




