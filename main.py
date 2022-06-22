import pygame
from chess.constants import BLACK, WHITE, WIDTH, HEIGHT, SQUARE_SIZE
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
    choice_made = False
    r, c = -1,-1
    piece = game.board.pieces[30]
    piece2 = game.board.pieces[31]
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type ==pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_pos_from_mouse(pos)
                game.select((row,col))

                
        game.update()


    pygame.quit()

main()