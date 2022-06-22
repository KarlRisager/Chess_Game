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