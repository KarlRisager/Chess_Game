import pygame
from chess.constants import WIDTH, HEIGHT, SQUARE_SIZE
from chess.board import Board
from chess.game import Game
from chess.pieces import Pawn


FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')

def get_pos_from_mouse(pos):
    x, y = pos
    row = y//SQUARE_SIZE
    col = x//SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type ==pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_pos_from_mouse(pos)
                piece = game.board.get_piece(row, col)
                if piece != None:
                    c = piece.col
                    r = piece.row
                    game.move(piece, r-1,c)
        game.update()


    pygame.quit()

main()