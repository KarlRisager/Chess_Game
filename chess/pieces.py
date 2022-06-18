import pygame
from .constants import GREY, SQUARE_SIZE, WHITE

class Pawn:

    def __init__(self, row, col, color):
        self.color = color
        self.row = row
        self.col = col
        self.x = 0
        self.y = 0
        if self.color == WHITE:
            pic = pygame.image.load('Images\white_pawn.png').convert_alpha()
        else:
            pass
        self.pic = pygame.transform.scale(pic, (SQUARE_SIZE, SQUARE_SIZE))
        self.calc_pos()
        self.block = pygame.Rect(self.x, self.y, SQUARE_SIZE, SQUARE_SIZE)

    def calc_pos(self):
        self.x = SQUARE_SIZE*self.col #+ SQUARE_SIZE//2
        self.y = SQUARE_SIZE*self.row #+ SQUARE_SIZE//2

    def draw(self, win):
        win.blit(self.pic, self.block)





