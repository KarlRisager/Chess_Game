import pygame

from chess.pieces import Pawn, Rook, Bishop, Knight, King, Queen
from .constants import BLACK, SQUARE_SIZE, WHITE, BROWN, ROWS, COLS
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
    
    def remove(self,piece):
        self.board.pieces.remove(piece)
    
    def move(self, piece, row, col):
        color = piece.color
        piece_at_pos = self.board.get_piece(row,col)
        if piece_at_pos != None and piece_at_pos.color != color:
            self.remove(piece_at_pos)
        self.board.move(piece, row, col)
        self.pawn_to_queen()
    
    def get_pos_off_pieces(self, color):
        lst = []
        for piece in self.board.pieces:
            if piece.color == color:
                lst.append((piece.row,piece.col))
        return lst
    
    def get_valid_moves(self, piece):
        color = piece.color
        #f = [N,NE,E,SE,S,SW,W,NW]
        further = [True,True,True,True,True,True,True,True]
        row = piece.row
        col = piece.col
        valid_list = []
        typo = type(piece).__name__


        if typo == 'Pawn':
            if color == WHITE:
                if self.board.get_piece(row-1,col) == None:
                    valid_list.append((-1,0))
                if piece.unmoved and self.board.get_piece(row-2,col) == None:
                    valid_list.append((-2,0))
                if self.board.get_piece(row-1,col-1)!=None:
                    valid_list.append((-1,-1))
                if self.board.get_piece(row-1,col+1)!=None:
                    valid_list.append((-1,1))
            if piece.color == BLACK:
                if self.board.get_piece(row+1,col) == None:
                    valid_list.append((1,0))
                if piece.unmoved and self.board.get_piece(row+2,col) == None:
                    valid_list.append((2,0))
                if self.board.get_piece(row+1,col-1)!=None:
                    valid_list.append((1,-1))
                if self.board.get_piece(row+1,col+1)!=None:
                    valid_list.append((1,1))
                
        elif typo == 'Rook':

            for r in range(1,ROWS):
                if further[4]:
                    valid_list.append((r,0))
                    piece_at = self.board.get_piece(row+r,col)
                    if piece_at != None:
                        further[4] = False

                if further[0]:
                    valid_list.append((-r,0))
                    piece_at = self.board.get_piece(row-r,col)
                    if piece_at != None:
                        further[0] = False
                
                if further[2]:
                    valid_list.append((0,r))
                    piece_at = self.board.get_piece(row,col+r)
                    if piece_at != None:
                        further[2] = False


                if further[6]:
                    valid_list.append((0,-r))
                    piece_at = self.board.get_piece(row,col-r)
                    if piece_at != None:
                        further[6] = False
        elif typo == 'Bishop':
            for r in range(1,ROWS):
                if further[3]:
                    valid_list.append((r,r))
                    piece_at = self.board.get_piece(row+r,col+r)
                    if piece_at != None:
                        further[3] = False
                if further[1]:
                    valid_list.append((-r,r))
                    piece_at = self.board.get_piece(row-r,col+r)
                    if piece_at != None:
                        further[1] = False
                if further[5]:
                    valid_list.append((r,-r))
                    piece_at = self.board.get_piece(row+r,col-r)
                    if piece_at != None:
                        further[5] = False
                if further[7]:
                    valid_list.append((-r,-r))
                    piece_at = self.board.get_piece(row-r,col-r)
                    if piece_at != None:
                        further[7] = False
        elif typo == 'Knight':
            valid_list_knight = [(-1,-2),(-2,-1),(-1,2),(-2,1),(1,2),(2,1),(2,-1),(1,-2)]
            for move in valid_list_knight:
                valid_list.append(move)
        elif typo == 'King':
            valid_list_king = [(1,1),(1,0),(0,1),(-1,-1),(-1,0),(0,-1),(-1,1),(1,-1)]
            for move in valid_list_king:
                valid_list.append(move)
        elif typo == 'Queen':
            for r in range(1,ROWS):


                if further[3]:
                    valid_list.append((r,r))
                    piece_at = self.board.get_piece(row+r,col+r)
                    if piece_at != None:
                        further[3] = False
                if further[1]:
                    valid_list.append((-r,r))
                    piece_at = self.board.get_piece(row-r,col+r)
                    if piece_at != None:
                        further[1] = False
                if further[5]:
                    valid_list.append((r,-r))
                    piece_at = self.board.get_piece(row+r,col-r)
                    if piece_at != None:
                        further[5] = False
                if further[7]:
                    valid_list.append((-r,-r))
                    piece_at = self.board.get_piece(row-r,col-r)
                    if piece_at != None:
                        further[7] = False

                if further[4]:
                    valid_list.append((r,0))
                    piece_at = self.board.get_piece(row+r,col)
                    if piece_at != None:
                        further[4] = False

                if further[0]:
                    valid_list.append((-r,0))
                    piece_at = self.board.get_piece(row-r,col)
                    if piece_at != None:
                        further[0] = False
                
                if further[2]:
                    valid_list.append((0,r))
                    piece_at = self.board.get_piece(row,col+r)
                    if piece_at != None:
                        further[2] = False


                if further[6]:
                    valid_list.append((0,-r))
                    piece_at = self.board.get_piece(row,col-r)
                    if piece_at != None:
                        further[6] = False
        print('possible moves:')
        print(valid_list)
        temp_valid_list = valid_list
        for move in valid_list[:]:
            y,x = move
            r = row + y
            c = col + x
            
            if r > ROWS or r<0 or c > COLS or c<0:
                valid_list.remove(move)

            if (r,c) in self.get_pos_off_pieces(color):
                valid_list.remove(move)

    
        return valid_list

    def pawn_to_queen(self):
        for piece in self.board.pieces:
            typo = type(piece).__name__
            if typo == 'Pawn' and piece.color == WHITE and piece.row == 0:
                temp_piece = Queen(piece.row, piece.col, piece.color)
                self.board.pieces.remove(piece)
                self.board.pieces.append(temp_piece)
            if typo == 'Pawn' and piece.color == BLACK and piece.row == 7:
                temp_piece = Queen(piece.row, piece.col, piece.color)
                self.board.pieces.remove(piece)
                self.board.pieces.append(temp_piece)
    

