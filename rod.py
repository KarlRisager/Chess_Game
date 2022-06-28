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
    print(game.check_check_mate(BLACK))
    choice_made = False

                if piece1.row == piece2.row:
                    if direction == 'east':
                        pass
                    if direction == 'west':
                        pass
                if piece1.col == piece2.col:
                    if direction == 'north':
                        pass
                    if direction == 'south':
                        pass

 #def pawn_to_queen(self):
        '''Makes all the pawns, that have reached the other side of the boead, queens'''
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

print('line_clear: %r'% line_clear)
            print('line_in_danger: %r'%line_in_danger)
            print('king is unmoved: %r'%king.unmoved)
            print('rook is unmoved: %r'%rook.unmoved)