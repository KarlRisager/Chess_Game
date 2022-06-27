from string import whitespace
import pygame

from chess.pieces import Pawn, Rook, Bishop, Knight, King, Queen
from .constants import BLACK, SQUARE_SIZE, WHITE, BROWN, ROWS, COLS
from.board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        '''Draws all changes and updates thescreen'''
        self.board.draw(self.win)
        pygame.display.update()
    
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.MoveLog = []
    
    def reset(self):
        '''Resets the game'''
        self._init()
        self.update()
    
    def remove(self,piece):
        '''Removes piece from board'''
        self.board.dead_pieces.append(piece)
        self.board.pieces.remove(piece)

    def move(self, piece, row, col):
        ''''Moves piece to position (row,col)'''
        MoveLogInstanse = [(piece, (piece.row, piece.col), (row, col))]
        color = piece.color
        piece_at_pos = self.board.get_piece(row,col)
        if piece_at_pos != None and piece_at_pos.color != color:
            MoveLogInstanse.append((piece_at_pos, (piece_at_pos.row,piece_at_pos.col), (-1,-1)))
            self.remove(piece_at_pos)
        self.MoveLog.append(MoveLogInstanse)
        self.board.move(piece, row, col)
        typo = type(piece).__name__
        if typo == 'Pawn' and piece.color == WHITE and piece.row == 0:
            temp_piece = Queen(piece.row, piece.col, piece.color)
            self.board.pieces.remove(piece)
            self.board.pieces.append(temp_piece)
        if typo == 'Pawn' and piece.color == BLACK and piece.row == 7:
            temp_piece = Queen(piece.row, piece.col, piece.color)
            self.board.pieces.remove(piece)
            self.board.pieces.append(temp_piece)
        #self.pawn_to_queen()
    
    def unmove(self):
        if len(self.MoveLog)!=0:
            last_moves = self.MoveLog.pop(len(self.MoveLog)-1)
            for move in last_moves:
                r, c = move[1]
                if move[2] == (-1,-1):
                    self.board.pieces.append(move[0])
                if not(move[0] in self.board.pieces):
                    piece_at = self.board.get_piece(move[0].row, move[0].col)
                    self.remove(piece_at)
                    self.board.pieces.append(move[0])
                self.move(move[0], r, c)
            if self.turn == BLACK:
                self.turn = WHITE
            else:
                self.turn = BLACK
            #self.update()
    
    def get_pos_off_pieces(self, color):
        '''Returns a list of positions of pieces, that have the color color'''
        lst = []
        for piece in self.board.pieces:
            if piece.color == color:
                lst.append((piece.row,piece.col))
        return lst
    
    def get_pieces(self, color):
        '''Returns a list of pieces, that have the color color'''
        lst = []
        for piece in self.board.pieces:
            if piece.color == color:
                lst.append(piece)
        return lst

    def get_valid_moves(self, piece):
        '''Returns a list of moves, that are valid for piece'''
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
            
            if r > (ROWS -1) or r<0 or c > (COLS-1) or c<0:
                valid_list.remove(move)

            if (r,c) in self.get_pos_off_pieces(color):
                valid_list.remove(move)

    
        return valid_list

    def possible_next_pos(self, piece):
        '''Returns a list of position, that piece can have after a single valid move'''
        lst = []
        for pos in self.get_valid_moves(piece):
            r,c = pos
            next_pos = (piece.row + r, piece.col + c)
            lst.append(next_pos)
        lst.append((piece.row, piece.col))
        return lst
    def possible_next_pos_after_move(self, piece):
        lst = []
        for pos in self.get_valid_moves(piece):
            r,c = pos
            next_pos = (piece.row + r, piece.col + c)
            lst.append(next_pos)
        return lst

    

    def check_check(self, color, pos):
        '''checks if the king of color is checked, or the king of color in position pos is checked'''
        lst = []
        king = None
        op = None
        king_pos = pos
        if pos == None:
            king = self.get_king(color)
            king_pos = (king.row, king.col)
        if color == WHITE:
            op = BLACK
        elif color == BLACK:
            op = WHITE
        op_pieces = self.get_pieces(op)
        for piece in op_pieces:
            lst.extend(self.possible_next_pos(piece))
        if king_pos in lst:
            return True
        else:
            return False
    def check_mate(self,color):
        pieces = self.get_pieces(color)
        for piece in pieces:
            pos_next_pos = self.possible_next_pos(piece)
            for (r,c) in pos_next_pos:
                self.move(piece, r, c)
                if not(self.check_check(color, None)):
                    if self.turn == WHITE:
                        self.turn = BLACK
                    else:
                        self.turn = WHITE
                    self.unmove()
                    return False
                self.unmove()
        return True
    
    #not working properly yet
    def stale_mate(self, color):
        pieces = self.get_pieces(color)
        for piece in pieces:
            pos_next_pos = self.possible_next_pos_after_move(piece)
            for (r,c) in pos_next_pos:
                self.move(piece, r, c)
                if not(self.check_check(color, None)):
                    if self.turn == WHITE:
                        self.turn = BLACK
                    else:
                        self.turn = WHITE
                    self.unmove()
                    return False
                self.unmove()
        print('stalemate')
        return True


    def temp_check_check_mate(self, color):
        check_mate = True
        king = self.get_king(color)
        check = self.check_check(color, None)
        pieces = self.get_pieces(color)
        for piece in pieces:
            next_poses = self.possible_next_pos(piece)
            for pos in next_poses:
                if not(self.results_in_check(piece, pos[0], pos[1])):
                    check_mate = False
        return check_mate
                


    def check_check_mate(self, color):
        '''checks if there is a check mate i.e. the game is over'''
        print('--------------------')
        king = self.get_king(color)
        if color == BLACK:
            print('Black king at (%i,%i)'%(king.row, king.col))
        elif color == WHITE:
            print('White king at (%i,%i)'%(king.row, king.col))
        possible_king_pos = self.possible_next_pos(king)
        check_mate = []
        for pos in possible_king_pos:
            print('checking that following doesn\'t check')
            print(pos)
            print(self.check_check(color,pos))
            check_mate.append(self.check_check(color, pos))
        if True in check_mate:#maybe remove
            print('check')
        if False in check_mate or len(check_mate) == 0:
            print('King can move')
            print('--------------------')
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
            print('king can not move')
            print('--------------------')
            for piece in offensive_pieces:
                line = []
                if self.is_danger_to2(piece, king):
                    print('piece at (%i,%i) is danger to king'%(piece.row,piece.col))
                    line = self.get_line_between(piece, king)
                    number_of += 1
                    for def_piece in deffensive_pieces:
                        block = False
                        if type(def_piece).__name__ != 'King':
                            def_piece_possible_next_pos = self.possible_next_pos(def_piece)
                            for pos_def_pos in def_piece_possible_next_pos:
                                if pos_def_pos in line:
                                    print('     But is blocked by piece at (%i,%i)'%(def_piece.row,def_piece.col))
                                    block = True
                                    break
                        if self.is_danger_to2(def_piece, piece) or block:
                            if self.is_danger_to2(def_piece,piece) and not(self.results_in_check(def_piece,piece.row, piece.col)):
                                print('     But it is threatened by piece at (%i,%i)'%(def_piece.row,def_piece.col))
                            number_of_in_danger += 1
                            break

            
            if number_of == number_of_in_danger == 1:
                return False
        return True

        
    def is_danger_to(self, piece):
        '''Returns a list of pieces, that piece threatens'''
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
        '''checks if offensive_piece threatens defensive_piece'''
        possible_attack_squares = self.possible_next_pos(offensive_piece)
        def_pos = (defensive_piece.row, defensive_piece.col)
        if def_pos in possible_attack_squares:
            return True
        else:
            return False


    def is_in_danger(self, piece):
        '''checks if piece is threatend'''
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
        '''returns king of color'''
        for piece in self.get_pieces(color):
            typo = type(piece).__name__
            if typo == 'King':
                return piece
    
    def get_copy_at_pos(self, piece, pos):
        color = piece.color
        r, c = pos
        typo = type(piece).__name__
        if typo == 'Pawn':
            return Pawn(r,c,color)
        elif typo == 'Rook':
            return Rook(r,c,color)
        elif typo == 'Knight':
            return Knight(r,c,color)
        elif typo == 'Bishop':
            return Bishop(r,c,color)
        elif typo == 'Queen':
            return Queen(r,c,color)
        elif typo == 'King':
            return King(r,c,color)
        else:
            return None
    
    def inverse_col(self, col):
        if col == 0:
            return 7
        if col == 1:
            return 6
        if col == 2:
            return 5
        if col == 3:
            return 4
        if col == 4:
            return 3
        if col == 5:
            return 2
        if col == 6:
            return 1
        if col == 7:
            return 0
    
    def on_board(self,pos):
        r,c = pos
        if r>0 and r<(ROWS-1) and c>0 and c<(COLS-1):
            return True
        else:
            return False


    def get_line_ignoring_pieces(self,piece1, piece2):
        lst = []
        direction = ''
        piece1_type = type(piece1).__name__
        peice2_pos = (piece2.row, piece2.col)
        if piece1_type == 'Queen':
            pos_lst = []
            for r in range(ROWS):
                if r != piece1.row:
                    pos_lst.append((r,piece1.col))
            for c in range(COLS):
                if c != piece1.col:
                    pos_lst.append((piece1.row,c))
            for k in range(ROWS):
                pos_SE = (piece1.row+k, piece1.col+k)
                if self.on_board(pos_SE):
                    pos_lst.append(pos_SE)
                pos_NW = (piece1.row-k,piece1.col-k)
                if self.on_board(pos_NW):
                    pos_lst.append(pos_NW)
                pos_NE = (piece1.row-k,piece1.col+k)
                if self.on_board(pos_NE):
                    pos_lst.append(pos_NE)
                pos_SW = (piece1.row+k,piece1.col-k)
                if self.on_board(pos_SW):
                    pos_lst.append(pos_SW)
            
            piece1_sum = piece1.row+piece1.col
            piece2_sum = piece2.row+piece2.col
            piece1_wierd_sum = piece1.row + self.inverse_col(piece1.col)
            piece2_wierd_sum = piece2.row + self.inverse_col(piece2.col)

            if piece1.row == piece2.row:
                    if piece1.col < piece2.col:
                        direction = 'east'
                    if piece1.col > piece2.col:
                        direction = 'west'
            if piece1.col == piece2.col:
                    if piece1.row < piece2.row:
                        direction = 'south'
                    if piece1.row > piece2.row:
                        direction = 'north'
            if direction == 'north':
                    for pos in pos_lst:
                        if pos[0]<piece1.row:
                            if pos[1] == piece2.col and pos[0]>piece2.row:
                                lst.append(pos)
                    return lst
            elif direction == 'south':
                    for pos in pos_lst:
                        if pos[0]>piece1.row:
                            if pos[1] == piece2.col and pos[0] < piece2.row:
                                lst.append(pos)
                    return lst
            elif direction == 'east':
                    for pos in pos_lst:
                        if pos[1]>piece1.col:
                            if pos[0] == piece2.row and pos[1]< piece2.col:
                                lst.append(pos)
                    return lst
            elif direction == 'west':
                    for pos in pos_lst:
                        if pos[1]<piece1.col:
                            if pos[0] == piece2.row and pos[1] > piece2.col:
                                lst.append(pos)
                    return lst
            
            elif piece1_sum == piece2_sum:
                if piece1.row < piece2.row:
                    r = piece1.row + 1
                    c = piece1.col - 1
                    while r < piece2.row and c > piece2.col:
                        if (r,c) in pos_lst:
                            lst.append((r,c))
                        r += 1
                        c -= 1
                    return lst
                if piece1.row > piece2.row:
                    r = piece1.row - 1
                    c = piece1.col + 1
                    while r > piece2.row and c < piece2.col:
                        if (r,c) in pos_lst:
                            lst.append((r,c))
                        r -= 1
                        c += 1
                    return lst
            elif piece1_wierd_sum == piece2_wierd_sum:
                if piece1.row < piece2.row:
                    r = piece1.row + 1
                    c = piece1.col + 1
                    while r < piece2.row and c < piece2.col:
                        if (r,c) in pos_lst:
                            lst.append((r,c))
                        r += 1
                        c += 1
                    return lst
                if piece1.row > piece2.row:
                    r = piece1.row - 1
                    c = piece1.col - 1
                    while r > piece2.row and c > piece2.col:
                        if (r,c) in pos_lst:
                            lst.append((r,c))
                        r -= 1
                        c -= 1
                    return lst
            else:
                return lst

        elif piece1_type == 'Rook':
            pos_lst = []
            for r in range(ROWS):
                if r != piece1.row:
                    pos_lst.append((r,piece1.col))
            for c in range(COLS):
                if c != piece1.col:
                    pos_lst.append((piece1.row,c))

            if piece1.row == piece2.row:
                    if piece1.col < piece2.col:
                        direction = 'east'
                    if piece1.col > piece2.col:
                        direction = 'west'
            if piece1.col == piece2.col:
                    if piece1.row < piece2.row:
                        direction = 'south'
                    if piece1.row > piece2.row:
                        direction = 'north'
            else:
                return lst
            if direction == 'north':
                    for pos in pos_lst:
                        if pos[0]<piece1.row:
                            if pos[1] == piece2.col and pos[0]>piece2.row:
                                lst.append(pos)
                    return lst
            if direction == 'south':
                    for pos in pos_lst:
                        if pos[0]>piece1.row:
                            if pos[1] == piece2.col and pos[0] < piece2.row:
                                lst.append(pos)
                    return lst
            if direction == 'east':
                    for pos in pos_lst:
                        if pos[1]>piece1.col:
                            if pos[0] == piece2.row and pos[1]< piece2.col:
                                lst.append(pos)
                    return lst
            if direction == 'west':
                    for pos in pos_lst:
                        if pos[1]<piece1.col:
                            if pos[0] == piece2.row and pos[1] > piece2.col:
                                lst.append(pos)
                    return lst
            return lst
                
        elif piece1_type == 'Bishop':
            pos_lst = []
            for k in range(ROWS):
                pos_SE = (piece1.row+k, piece1.col+k)
                if self.on_board(pos_SE):
                    pos_lst.append(pos_SE)
                pos_NW = (piece1.row-k,piece1.col-k)
                if self.on_board(pos_NW):
                    pos_lst.append(pos_NW)
                pos_NE = (piece1.row-k,piece1.col+k)
                if self.on_board(pos_NE):
                    pos_lst.append(pos_NE)
                pos_SW = (piece1.row+k,piece1.col-k)
                if self.on_board(pos_SW):
                    pos_lst.append(pos_SW)
            
            piece1_sum = piece1.row+piece1.col
            piece2_sum = piece2.row+piece2.col
            piece1_wierd_sum = piece1.row + self.inverse_col(piece1.col)
            piece2_wierd_sum = piece2.row + self.inverse_col(piece2.col)
            if piece1_sum == piece2_sum:
                if piece1.row < piece2.row:
                    r = piece1.row + 1
                    c = piece1.col - 1
                    while r < piece2.row and c > piece2.col:
                        if (r,c) in pos_lst:
                            lst.append((r,c))
                        r += 1
                        c -= 1
                    return lst
                if piece1.row > piece2.row:
                    r = piece1.row - 1
                    c = piece1.col + 1
                    while r > piece2.row and c < piece2.col:
                        if (r,c) in pos_lst:
                            lst.append((r,c))
                        r -= 1
                        c += 1
                    return lst
            elif piece1_wierd_sum == piece2_wierd_sum:
                if piece1.row < piece2.row:
                    r = piece1.row + 1
                    c = piece1.col + 1
                    while r < piece2.row and c < piece2.col:
                        if (r,c) in pos_lst:
                            lst.append((r,c))
                        r += 1
                        c += 1
                    return lst
                if piece1.row > piece2.row:
                    r = piece1.row - 1
                    c = piece1.col - 1
                    while r > piece2.row and c > piece2.col:
                        if (r,c) in pos_lst:
                            lst.append((r,c))
                        r -= 1
                        c -= 1
                    return lst
            return lst
        
        return lst

            



    def get_line_between(self, piece1, piece2):
        lst = []
        direction = ''
        piece1_type = type(piece1).__name__
        piece1_possible_next_pos = self.possible_next_pos(piece1)
        peice2_pos = (piece2.row, piece2.col)
        if not(peice2_pos in piece1_possible_next_pos):
            return lst
        if piece1_type == 'Queen':
            piece1_sum = piece1.row+piece1.col
            piece2_sum = piece2.row+piece2.col
            piece1_wierd_sum = piece1.row + self.inverse_col(piece1.col)
            piece2_wierd_sum = piece2.row + self.inverse_col(piece2.col)
            if piece1_sum == piece2_sum:
                if piece1.row < piece2.row:
                    r = piece1.row + 1
                    c = piece1.col - 1
                    while r < piece2.row and c > piece2.col:
                        if (r,c) in piece1_possible_next_pos:
                            lst.append((r,c))
                        r += 1
                        c -= 1
                    return lst
                if piece1.row > piece2.row:
                    r = piece1.row - 1
                    c = piece1.col + 1
                    while r > piece2.row and c < piece2.col:
                        if (r,c) in piece1_possible_next_pos:
                            lst.append((r,c))
                        r -= 1
                        c += 1
                    return lst
            elif piece1_wierd_sum == piece2_wierd_sum:
                if piece1.row < piece2.row:
                    r = piece1.row + 1
                    c = piece1.col + 1
                    while r < piece2.row and c < piece2.col:
                        if (r,c) in piece1_possible_next_pos:
                            lst.append((r,c))
                        r += 1
                        c += 1
                    return lst
                if piece1.row > piece2.row:
                    r = piece1.row - 1
                    c = piece1.col - 1
                    while r > piece2.row and c > piece2.col:
                        if (r,c) in piece1_possible_next_pos:
                            lst.append((r,c))
                        r -= 1
                        c -= 1
                    return lst
            else:
                if piece1.row == piece2.row:
                    if piece1.col < piece2.col:
                        direction = 'east'
                    if piece1.col > piece2.col:
                        direction = 'west'
                if piece1.col == piece2.col:
                    if piece1.row < piece2.row:
                        direction = 'south'
                    if piece1.row > piece2.row:
                        direction = 'north'
                if direction == 'north':
                    for pos in piece1_possible_next_pos:
                        if pos[0]<piece1.row:
                            if pos[1] == piece2.col and pos[0]>piece2.row:
                                lst.append(pos)
                    return lst
                if direction == 'south':
                    for pos in piece1_possible_next_pos:
                        if pos[0]>piece1.row:
                            if pos[1] == piece2.col and pos[0] < piece2.row:
                                lst.append(pos)
                    return lst
                if direction == 'east':
                    for pos in piece1_possible_next_pos:
                        if pos[1]>piece1.col:
                            if pos[0] == piece2.row and pos[1]< piece2.col:
                                lst.append(pos)
                    return lst
                if direction == 'west':
                    for pos in piece1_possible_next_pos:
                        if pos[1]<piece1.col:
                            if pos[0] == piece2.row and pos[1] > piece2.col:
                                lst.append(pos)
                    return lst
            return lst
            

        elif piece1_type == 'Rook':
            if piece1.row == piece2.row:
                if piece1.col < piece2.col:
                    direction = 'east'
                if piece1.col > piece2.col:
                    direction = 'west'
            if piece1.col == piece2.col:
                if piece1.row < piece2.row:
                    direction = 'south'
                if piece1.row > piece2.row:
                    direction = 'north'
            if direction == 'north':
                for pos in piece1_possible_next_pos:
                    if pos[0]<piece1.row:
                        if pos[1] == piece2.col and pos[0]>piece2.row:
                            lst.append(pos)
                return lst
            if direction == 'south':
                for pos in piece1_possible_next_pos:
                    if pos[0]>piece1.row:
                        if pos[1] == piece2.col and pos[0] < piece2.row:
                            lst.append(pos)
                return lst
            if direction == 'east':
                for pos in piece1_possible_next_pos:
                    if pos[1]>piece1.col:
                        if pos[0] == piece2.row and pos[1]< piece2.col:
                            lst.append(pos)
                return lst
            if direction == 'west':
                for pos in piece1_possible_next_pos:
                    if pos[1]<piece1.col:
                        if pos[0] == piece2.row and pos[1] > piece2.col:
                            lst.append(pos)
                return lst


        elif piece1_type == 'Bishop':
            piece1_sum = piece1.row+piece1.col
            piece2_sum = piece2.row+piece2.col
            piece1_wierd_sum = piece1.row + self.inverse_col(piece1.col)
            piece2_wierd_sum = piece2.row + self.inverse_col(piece2.col)
            if piece1_sum == piece2_sum:
                if piece1.row < piece2.row:
                    r = piece1.row + 1
                    c = piece1.col - 1
                    while r < piece2.row and c > piece2.col:
                        if (r,c) in piece1_possible_next_pos:
                            lst.append((r,c))
                        r += 1
                        c -= 1
                    return lst
                if piece1.row > piece2.row:
                    r = piece1.row - 1
                    c = piece1.col + 1
                    while r > piece2.row and c < piece2.col:
                        if (r,c) in piece1_possible_next_pos:
                            lst.append((r,c))
                        r -= 1
                        c += 1
                    return lst
            if piece1_wierd_sum == piece2_wierd_sum:
                if piece1.row < piece2.row:
                    r = piece1.row + 1
                    c = piece1.col + 1
                    while r < piece2.row and c < piece2.col:
                        if (r,c) in piece1_possible_next_pos:
                            lst.append((r,c))
                        r += 1
                        c += 1
                    return lst
                if piece1.row > piece2.row:
                    r = piece1.row - 1
                    c = piece1.col - 1
                    while r > piece2.row and c > piece2.col:
                        if (r,c) in piece1_possible_next_pos:
                            lst.append((r,c))
                        r -= 1
                        c -= 1
                    return lst
        else:
            return lst
    #not quite done
    def results_in_check(self, piece, r, c):
        piece_pos = (piece.row, piece.col)
        king = self.get_king(piece.color)
        king_pos = (king.row, king.col)
        #if piece_pos == king_pos:
            #print('piece is king')
        #print('king at: (%i,%i)'%(king.row,king.col))
        op = BLACK
        if piece.color == BLACK:
            op = WHITE
        op_pieces = self.get_pieces(op)
        for op_piece in op_pieces:
            line = self.get_line_ignoring_pieces(op_piece, king)
            op_piece_pos = (op_piece.row, op_piece.col)
            #if len(line)>0:
                #print('op_piece at (%i,%i). Line is'%(op_piece.row,op_piece.col))
                #print(line)
                #print('trying to move to (%i,%i)'%(r,c))
            pieces_in_line = []
            for pos in line:
                row, col = pos
                piece_at_pos = self.board.get_piece(row,col)
                if piece_at_pos != None and piece_at_pos.color == piece.color:
                    pieces_in_line.append(piece_at_pos)
            if piece_pos == king_pos and ((r,c) in line or (r,c) in self.possible_next_pos(op_piece)):
                if (r,c) != op_piece_pos:
                    #print('     But the king can not move into check')
                    return True
            elif piece_pos in line and not((r,c) in line) and len(pieces_in_line) < 2:
                if (r,c) != op_piece_pos:
                    #print('     But piece is pinned')
                    return True
            elif len(line) != 0 and len(pieces_in_line) == 0  and (r,c) not in line:
                if piece_pos != king_pos:
                    r1,r2 = piece_pos
                    #print('     But move does not block or deffend attack on King from (%i,%i)'%(r1,r2))
                    return True
            elif len(line) == 0 and self.is_danger_to2(op_piece, king) and (r,c)!=op_piece_pos:
                if piece_pos!=king_pos:
                    #print('     But move doesn\'t deffend king')
                    return True
        return False
                
                


    def results_in_kill(self, piece, move):
        pass


    def select(self, pos):
        r,c = pos
        if self.selected == None:
            piece = self.board.get_piece(r,c)
            if piece != None and piece.color == self.turn:
                self.selected = piece
                print('--------------------')
                print('piece at (%i,%i) has be choosen'%(piece.row,piece.col))
        elif self.selected != None:
            print(pos)
            valid_moves = self.get_valid_moves(self.selected)
            piece_row = self.selected.row
            piece_col = self.selected.col
            move = (r-piece_row,c-piece_col)
            results_in_check = self.results_in_check(self.selected, r, c)
            if move in valid_moves and not(results_in_check):
                self.move(self.selected,r,c)
                print('piece has been moved to (%i,%i)'%(r,c))
                self.selected = None
                if self.turn == WHITE:
                    print('it is blacks turn')
                    self.turn = BLACK
                    print('checking if black has lost')
                    lost = self.check_mate(self.turn)
                    #stale = self.stale_mate(self.turn)
                    print('Has black lost: %r'%lost)
                    if lost:#other player has won the game or stalemate
                        self.reset()
                        #pass
                else:
                    print('it is whites turn')
                    self.turn = WHITE
                    print('checking if white has lost')
                    lost = self.check_mate(self.turn)
                    #stale = self.stale_mate(self.turn)
                    print('Has white lost: %r'%lost)
                    if lost:#other player has won the game or stalemate
                        self.reset()
                        #pass
                print('--------------------')
            else:
                self.selected = None



    

