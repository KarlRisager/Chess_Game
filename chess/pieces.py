import pygame
from .constants import BLACK, GREY, SQUARE_SIZE, WHITE

class Pawn:

    def __init__(self, row, col, color):
        self.color = color
        self.row = row
        self.col = col
        self.x = 0
        self.y = 0
        self.unmoved = True
        self.firstmove = False
        if self.color == WHITE:
            pic = pygame.image.load('Images/white_pawn.png').convert_alpha()
        else:
            pic = pygame.image.load('Images/black_pawn.png').convert_alpha()
        self.pic = pygame.transform.scale(pic, (SQUARE_SIZE, SQUARE_SIZE))
        self.calc_pos()
        self.block = pygame.Rect(self.x, self.y, SQUARE_SIZE, SQUARE_SIZE)

    def calc_pos(self):
        self.x = SQUARE_SIZE*self.col #+ SQUARE_SIZE//2
        self.y = SQUARE_SIZE*self.row #+ SQUARE_SIZE//2
        self.block = pygame.Rect(self.x, self.y, SQUARE_SIZE, SQUARE_SIZE)

    def draw(self, win):
        win.blit(self.pic, self.block)

    def move(self,r,c):
        if self.unmoved:
            self.firstmove = True
        self.unmoved = False
        self.row = r
        self.col = c
        self.calc_pos()

    


class Rook:

    def __init__(self, row, col, color):
        self.color = color
        self.row = row
        self.col = col
        self.x = 0
        self.y = 0
        self.unmoved = True
        if self.color == WHITE:
            pic = pygame.image.load('Images/white_rook.png').convert_alpha()
        else:
            pic = pygame.image.load('Images/black_rook.png').convert_alpha()
        self.pic = pygame.transform.scale(pic, (SQUARE_SIZE, SQUARE_SIZE))
        self.calc_pos()
        self.block = pygame.Rect(self.x, self.y, SQUARE_SIZE, SQUARE_SIZE)

    def calc_pos(self):
        self.x = SQUARE_SIZE*self.col #+ SQUARE_SIZE//2
        self.y = SQUARE_SIZE*self.row #+ SQUARE_SIZE//2
        self.block = pygame.Rect(self.x, self.y, SQUARE_SIZE, SQUARE_SIZE)

    def draw(self, win):
        win.blit(self.pic, self.block)

    def move(self,r,c):
        self.unmoved = False
        self.row = r
        self.col = c
        self.calc_pos()

class Bishop:

    def __init__(self, row, col, color):
        self.color = color
        self.row = row
        self.col = col
        self.x = 0
        self.y = 0
        if self.color == WHITE:
            pic = pygame.image.load('Images/white_bishop.png').convert_alpha()
        else:
            pic = pygame.image.load('Images/black_bishop.png').convert_alpha()
        self.pic = pygame.transform.scale(pic, (SQUARE_SIZE, SQUARE_SIZE))
        self.calc_pos()
        self.block = pygame.Rect(self.x, self.y, SQUARE_SIZE, SQUARE_SIZE)

    def calc_pos(self):
        self.x = SQUARE_SIZE*self.col #+ SQUARE_SIZE//2
        self.y = SQUARE_SIZE*self.row #+ SQUARE_SIZE//2
        self.block = pygame.Rect(self.x, self.y, SQUARE_SIZE, SQUARE_SIZE)

    def draw(self, win):
        win.blit(self.pic, self.block)

    def move(self,r,c):
        self.row = r
        self.col = c
        self.calc_pos()

class Knight:

    def __init__(self, row, col, color):
        self.color = color
        self.row = row
        self.col = col
        self.x = 0
        self.y = 0
        self.unmoved = True
        if self.color == WHITE:
            pic = pygame.image.load('Images/white_knight.png').convert_alpha()
        else:
            pic = pygame.image.load('Images/black_knight.png').convert_alpha()
        self.pic = pygame.transform.scale(pic, (SQUARE_SIZE, SQUARE_SIZE))
        self.calc_pos()
        self.block = pygame.Rect(self.x, self.y, SQUARE_SIZE, SQUARE_SIZE)

    def calc_pos(self):
        self.x = SQUARE_SIZE*self.col #+ SQUARE_SIZE//2
        self.y = SQUARE_SIZE*self.row #+ SQUARE_SIZE//2
        self.block = pygame.Rect(self.x, self.y, SQUARE_SIZE, SQUARE_SIZE)

    def draw(self, win):
        win.blit(self.pic, self.block)

    def move(self,r,c):
        self.unmoved = False
        self.row = r
        self.col = c
        self.calc_pos()

class King:

    def __init__(self, row, col, color):
        self.color = color
        self.row = row
        self.col = col
        self.x = 0
        self.y = 0
        self.unmoved = True
        if self.color == WHITE:
            pic = pygame.image.load('Images/white_king.png').convert_alpha()
        else:
            pic = pygame.image.load('Images/black_king.png').convert_alpha()
        self.pic = pygame.transform.scale(pic, (SQUARE_SIZE, SQUARE_SIZE))
        self.calc_pos()
        self.block = pygame.Rect(self.x, self.y, SQUARE_SIZE, SQUARE_SIZE)

    def calc_pos(self):
        self.x = SQUARE_SIZE*self.col #+ SQUARE_SIZE//2
        self.y = SQUARE_SIZE*self.row #+ SQUARE_SIZE//2
        self.block = pygame.Rect(self.x, self.y, SQUARE_SIZE, SQUARE_SIZE)

    def draw(self, win):
        win.blit(self.pic, self.block)

    def move(self,r,c):
        self.unmoved = False
        self.row = r
        self.col = c
        self.calc_pos()

class Queen:

    def __init__(self, row, col, color):
        self.color = color
        self.row = row
        self.col = col
        self.x = 0
        self.y = 0
        if self.color == WHITE:
            pic = pygame.image.load('Images/white_queen.png').convert_alpha()
        else:
            pic = pygame.image.load('Images/black_queen.png').convert_alpha()
        self.pic = pygame.transform.scale(pic, (SQUARE_SIZE, SQUARE_SIZE))
        self.calc_pos()
        self.block = pygame.Rect(self.x, self.y, SQUARE_SIZE, SQUARE_SIZE)

    def calc_pos(self):
        self.x = SQUARE_SIZE*self.col #+ SQUARE_SIZE//2
        self.y = SQUARE_SIZE*self.row #+ SQUARE_SIZE//2
        self.block = pygame.Rect(self.x, self.y, SQUARE_SIZE, SQUARE_SIZE)

    def draw(self, win):
        win.blit(self.pic, self.block)
    
    def move(self,r,c):
        self.row = r
        self.col = c
        self.calc_pos()



