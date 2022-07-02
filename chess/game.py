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
    
    def change_turn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def op(self, color):
        if color == WHITE:
            return BLACK
        return WHITE
    def remove(self,piece):
        '''Removes piece from board'''
        self.board.dead_pieces.append(piece)
        self.board.pieces.remove(piece)

    def reset_firstmove(self,color):
        pieces = self.get_pieces(color)
        for piece in pieces:
            typo = type(piece).__name__
            if typo == 'Pawn':
                piece.firstmove = False

    def move(self, piece, row, col):
        ''''Moves piece to position (row,col)'''
        MoveLogInstanse = [(piece, (piece.row, piece.col), (row, col))]
        castle = False
        rook = None
        rook_pos_after = (-2,-2)
        color = piece.color
        piece_at_pos = self.board.get_piece(row,col)
        iep,iep_piece = self.is_enpassant(piece,row,col)
        typo = type(piece).__name__
        if col == (piece.col+2):
            rook = self.board.get_piece(row, 7)
            rook_pos_after = (row,col-1)
            castle = True
        if col == (piece.col-2):
            rook_pos_after = (row,col+1)
            rook = self.board.get_piece(row, 0)
            castle = True
        if typo == 'King' and castle:
            MoveLogInstanse.append((rook, (rook.row,rook.col), rook_pos_after))
            self.board.move(rook, rook_pos_after[0], rook_pos_after[1])
        if iep:
            print('En passant')
            MoveLogInstanse.append((iep_piece, (iep_piece.row, iep_piece.col), (-1,-1)))
            self.remove(iep_piece)
        if piece_at_pos != None and piece_at_pos.color != color:
            MoveLogInstanse.append((piece_at_pos, (piece_at_pos.row,piece_at_pos.col), (-1,-1)))
            self.remove(piece_at_pos)
        self.MoveLog.append(MoveLogInstanse)
        self.board.move(piece, row, col)
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
            print(last_moves)
            print(len(self.board.pieces))
            for move in last_moves:
                print('moving it to:')
                print(move[1])
                r, c = move[1]
                if move[2] == (-1,-1):
                    print('adding piece back')
                    self.board.pieces.append(move[0])
                if not(move[0] in self.board.pieces):
                    print('not on board')
                    piece_at = self.board.get_piece(move[0].row, move[0].col)
                    self.remove(piece_at)
                    self.board.pieces.append(move[0])
                print('returning piece at (%i,%i) to (%i,%i)'%(move[0].row,move[0].col,r,c))
                self.move(move[0], r, c)
            print(len(self.board.pieces))
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

    #to do doesn't check if rook is there and if move results in check
    def can_castle(self, color, side):
        if not(self.check_check(color,None)):
            results_in_check = False
            line_clear = True
            line_in_danger = False
            rook = None
            king = self.get_king(color)
            kr,kc = king.row,king.col
            if color == WHITE:
                if side == 'r':
                    line = ((kr,kc+1),(kr,kc+2))
                    for (r,c) in line:
                        if self.board.get_piece(r,c) != None:
                            line_clear = False
                    rook = self.board.get_piece(7,7)
                    line_in_danger = self.pos_in_danger_from(kr,kc+1) or self.pos_in_danger_from(kr,kc+2)
                elif side == 'l':
                    line = ((kr,kc-1),(kr,kc-2), (kr,kc-3))
                    for (r,c) in line:
                        if self.board.get_piece(r,c) != None:
                            line_clear = False
                    rook = self.board.get_piece(7,0)
                    line_in_danger = self.pos_in_danger_from(kr,kc-1) or self.pos_in_danger_from(kr,kc-2) or self.pos_in_danger_from(kr,kc-3)
                print(side)
                if not(line_in_danger) and king.unmoved and rook.unmoved and line_clear:
                    return True
            if color == BLACK:
                if side == 'r':
                    line = ((kr,kc+1),(kr,kc+2))
                    for (r,c) in line:
                        if self.board.get_piece(r,c) != None:
                            line_clear = False
                    rook = self.board.get_piece(0,7)
                    line_in_danger = self.pos_in_danger_from(kr,kc+1) or self.pos_in_danger_from(kr,kc+2)
                elif side == 'l':
                    line = ((kr,kc-1),(kr,kc-2), (kr,kc-3))
                    for (r,c) in line:
                        if self.board.get_piece(r,c) != None:
                            line_clear = False
                    rook = self.board.get_piece(0,0)
                    line_in_danger = self.pos_in_danger_from(kr,kc-1) or self.pos_in_danger_from(kr,kc-2) or self.pos_in_danger_from(kr,kc-3)
                print(side)
                if not(line_in_danger) and king.unmoved and rook.unmoved and line_clear:
                    return True
        return False
    
    def is_enpassant(self, piece, row, col):
        r,c = (piece.row, piece.col)
        if piece.color == WHITE:
            right = self.board.get_piece(r,c+1)
            piece_at_right = self.board.get_piece(r-1,c+1)
            left = self.board.get_piece(r,c-1)
            piece_at_left = self.board.get_piece(r-1,c-1)
            if type(right).__name__ == 'Pawn' and right.firstmove and piece_at_right == None:
                if right.color == BLACK and (row-r,col-c) == (-1,1):
                    return (True,right)
            if type(left).__name__ == 'Pawn' and left.firstmove and piece_at_left == None:
                if left.color == BLACK and (row-r,col-c) == (-1,-1):
                    return  (True,left)
        if piece.color == BLACK:
            right = self.board.get_piece(r,c+1)
            piece_at_right = self.board.get_piece(r+1,c+1)
            left = self.board.get_piece(r,c-1)
            piece_at_left = self.board.get_piece(r+1,c-1)
            if type(right).__name__ == 'Pawn' and right.firstmove and piece_at_right == None:
                if right.color == WHITE and (row-r,col-c) == (1,1):
                    return (True,right)
            if type(left).__name__ == 'Pawn' and left.firstmove and piece_at_left == None:
                if left.color == WHITE and (row-r,col-c) == (1,-1):
                    return (True, left)
        return (False, None)

    #to do
    def en_peasant(self, piece, row, col):
        pass

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
                #for en passant
                right = self.board.get_piece(row,col+1)
                piece_at_right = self.board.get_piece(row-1,col+1)
                left = self.board.get_piece(row,col-1)
                piece_at_left = self.board.get_piece(row-1,col-1)
                if type(right).__name__ == 'Pawn' and right.firstmove and piece_at_right == None:
                    if right.color == BLACK:
                        valid_list.append((-1,1))
                if type(left).__name__ == 'Pawn' and left.firstmove and piece_at_left == None:
                    if left.color == BLACK:
                        valid_list.append((-1,-1))
            if piece.color == BLACK:
                if self.board.get_piece(row+1,col) == None:
                    valid_list.append((1,0))
                if piece.unmoved and self.board.get_piece(row+2,col) == None:
                    valid_list.append((2,0))
                if self.board.get_piece(row+1,col-1)!=None:
                    valid_list.append((1,-1))
                if self.board.get_piece(row+1,col+1)!=None:
                    valid_list.append((1,1))
                # for en passant
                right = self.board.get_piece(row,col+1)
                piece_at_right = self.board.get_piece(row+1,col+1)
                left = self.board.get_piece(row,col-1)
                piece_at_left = self.board.get_piece(row+1,col-1)
                if type(right).__name__ == 'Pawn' and right.firstmove and piece_at_right == None:
                    if right.color == WHITE:
                        valid_list.append((1,1))
                if type(left).__name__ == 'Pawn' and left.firstmove and piece_at_left == None:
                    if left.color == WHITE:
                        valid_list.append((1,-1))
                
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
        op = self.op(color)
        op_pieces = self.get_pieces(op)
        for piece in op_pieces:
            lst.extend(self.possible_next_pos(piece))
        if king_pos in lst:
            return True
        else:
            return False
    def check_mate(self,color):
        return False
        pieces = self.get_pieces(color)
        for piece in pieces:
            pos_next_pos = self.possible_next_pos(piece)
            for (r,c) in pos_next_pos:
                self.move(piece, r, c)
                if not(self.check_check(color, None)):
                    self.unmove()
                    return False
                self.unmove()
        return True
    
    #not working properly yet
    def stale_mate(self, color):
        return False
        pieces = self.get_pieces(color)
        for piece in pieces:
            pos_next_pos = self.possible_next_pos_after_move(piece)
            for (r,c) in pos_next_pos:
                self.move(piece, r, c)
                if not(self.check_check(color, None)):
                    self.unmove()
                    return False
                self.unmove()
        print('stalemate')
        return True


    def pos_in_danger_from(self,color,pos):
        attacking_pieces = self.get_pieces(color)  
        for piece in attacking_pieces:
            if pos in self.possible_next_pos(piece):
                return True
        return False

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
            if self.can_castle(self.selected.color, 'r'):
                valid_moves.append((0,2))
            if self.can_castle(self.selected.color, 'l'):
                valid_moves.append((0,-2))
            move = (r-piece_row,c-piece_col)
            print('attempting to make move: (%i,%i)'% (move[0],move[1]))
            results_in_check = self.results_in_check(self.selected, r, c)
            print(valid_moves)
            if move in valid_moves and not(results_in_check):
                self.move(self.selected,r,c)
                print('piece has been moved to (%i,%i)'%(r,c))
                self.selected = None
                if self.turn == WHITE:
                    print('it is blacks turn')
                    self.turn = BLACK
                    self.reset_firstmove(BLACK)
                    print('checking if black has lost')
                    lost = self.check_mate(self.turn)
                    stale = self.stale_mate(self.turn)
                    print('Has black lost: %r'%lost)
                    if lost or stale:#other player has won the game or stalemate
                        self.reset()
                else:
                    print('it is whites turn')
                    self.turn = WHITE
                    self.reset_firstmove(WHITE)
                    print('checking if white has lost')
                    lost = self.check_mate(self.turn)
                    stale = self.stale_mate(self.turn)
                    print('Has white lost: %r'%lost)
                    if lost or stale:#other player has won the game or stalemate
                        self.reset()
                print('--------------------')
            else:
                self.selected = None



    

