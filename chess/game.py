from pickle import FALSE
from tabnanny import check
import pygame
from pyparsing import White

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
    
    def get_pieces(self, color):
        lst = []
        for piece in self.board.pieces:
            if piece.color == color:
                lst.append(piece)
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

        for move in valid_list[:]:
            y,x = move
            r = row + y
            c = col + x
            
            if r > ROWS or r<0 or c > COLS or c<0:
                valid_list.remove(move)

            if (r,c) in self.get_pos_off_pieces(color):
                valid_list.remove(move)

    
        return valid_list

    def possible_next_pos(self, piece):
        lst = []
        for pos in self.get_valid_moves(piece):
            r,c = pos
            next_pos = (piece.row + r, piece.col + c)
            lst.append(next_pos)
        lst.append((piece.row, piece.col))
        return lst

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
    #pos should only not be None, if used in check_chech_mate
    

    def check_check(self, color, pos):
        lst = []
        king = None
        op = None
        king_pos = pos
        if pos == None:
            king = self.get_king(color)
            king_pos = (king.row, king.col)
        if color == WHITE:
            op = BLACK
        else:
            op = WHITE
        op_pieces = self.get_pieces(op)
        for piece in op_pieces:
            lst.extend(self.possible_next_pos(piece))
        if king_pos in lst:
            return True
        else:
            return False
 

    def check_check_mate(self, color):
        king = self.get_king(color)
        possible_king_pos = self.possible_next_pos(king)
        check_mate = []
        for pos in possible_king_pos:
            check_mate.append(self.check_check(color, pos))
        if False in check_mate or len(check_mate) == 0:
            return False
        else:
            if color == WHITE:
                op = BLACK
            else:
                op = WHITE
            offensive_pieces = self.get_pieces(op)
            deffensive_pieces = self.get_pieces(color)
            number_of = 0
            number_of_in_danger =0
            for piece in offensive_pieces:
                if self.is_danger_to2(piece, king):
                    number_of += 1
                    for def_piece in deffensive_pieces:
                        if self.is_danger_to2(def_piece, piece):
                            number_of_in_danger += 1
                            break
            print(number_of,number_of_in_danger)
            
            if number_of == number_of_in_danger:
                return False
        return True

        
    def is_danger_to(self, piece):
        possible_pos = self.possible_next_pos(piece)
        op = BLACK
        if piece.color == BLACK:
            op = WHITE
        scared_pieces = self.get_pieces(op)
        for piece in scared_pieces[:]:
            pos = (piece.row, piece.col)
            if not(pos in possible_pos):
                scared_pieces.remove(piece)
        return scared_pieces

    def is_danger_to2(self,offensive_piece, defensive_piece):
        possible_attack_squares = self.possible_next_pos(offensive_piece)
        def_pos = (defensive_piece.row, defensive_piece.col)
        if def_pos in possible_attack_squares:
            return True
        else:
            return False


    def is_in_danger(self, piece):
        pos = (piece.row,piece.col)
        lst = []
        if piece.color == WHITE:
            op = BLACK
        else:
            op = WHITE
        op_pieces = self.get_pieces(op)
        for piece in op_pieces:
            lst.extend(self.possible_next_pos(piece))
        if pos in lst:
            return True
        else:
            return False



    def get_king(self, color):
        for piece in self.get_pieces(color):
            typo = type(piece).__name__
            if typo == 'King':
                return piece
        

    

