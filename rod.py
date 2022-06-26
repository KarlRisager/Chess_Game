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