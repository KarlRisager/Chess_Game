import pygame
from pyparsing import White
from .constants import COLS, WHITE, BLACK, BROWN, SQUARE_SIZE, ROWS
from .pieces import Pawn, Rook, Bishop, Knight, King, Queen


class Board:
    def __init__(self):
        self.pieces = [Pawn(6,0, WHITE),Pawn(6,1, WHITE),Pawn(6,2, WHITE),Pawn(6,3, WHITE),Pawn(6,4, WHITE),Pawn(6,5, WHITE),Pawn(6,6, WHITE),Pawn(6,7, WHITE),
        Pawn(1,0, BLACK),Pawn(1,1, BLACK),Pawn(1,2, BLACK),Pawn(1,3, BLACK),Pawn(1,4, BLACK),Pawn(1,5, BLACK),Pawn(1,6, BLACK),Pawn(1,7, BLACK),
        Rook(0,0,BLACK), Rook(0,7,BLACK), Rook(7,0,WHITE), Rook(7,7,WHITE),
        Bishop(0,2,BLACK), Bishop(0,5,BLACK), Bishop(7,2,WHITE), Bishop(7,5,WHITE),
        Knight(0,1,BLACK), Knight(0,6,BLACK), Knight(7,1,WHITE), Knight(7,6,WHITE),
        King(0,4,BLACK), King(7,4,WHITE), Queen(0,3,BLACK), Queen(7,3,WHITE)]
        self.dead = []
        self.selected_piece = None
        
    def draw_board(self, win):
        win.fill(BROWN)
        for row in range(ROWS):
            for col in range(row%2, ROWS, 2):
                pygame.draw.rect(win, WHITE, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        pass

    def get_piece(self, row, col):
        found = False
        for piece in self.pieces:
            pos = (piece.row, piece.col)
            if pos == (row,col):
                found = True
                return piece
        if not(found):
            return None

    def move(self, piece, row, col): #add piece as variable
        piece.move(row,col)
    
    def check_collision(self):
        pass



    def draw(self, win):
        self.draw_board(win)
        for piece in self.pieces:
                if piece != None:
                    piece.draw(win)




