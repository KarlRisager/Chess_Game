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
    choice_made = False
    r, c = -1,-1
    piece = None
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type ==pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_pos_from_mouse(pos)
                if not(choice_made):
                    piece = game.board.get_piece(row, col)
                    if piece != None:
                        choice_made = True
                        c = piece.col
                        r = piece.row
                    break
                if choice_made:
                    move = (row-r, col-c)
                    valid_moves = game.get_valid_moves(piece)
                    if move in valid_moves:
                        game.move(piece, row, col)
                    choice_made = False
        game.update()


    pygame.quit()

main()