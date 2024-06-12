"""
This class is responsible to store all the information about the present state of a chess game.
It will also be responsible to determine whether a particular move is valid during the current state of the game.
It will also keep a move log.
"""

class GameState():
    def __init__(self):
        """
        The board variable is a 8x8 2d list and each character of the list represent the piece of the chess.
        The first character represent he color of the piece 'b'(black) or 'w'(white).
        The second character represent the type of the piece:
            K - king, Q - queen, R - rook, N - knight, B - bishop, p - Pawn.
        "--" represent the empty space in the board.
        """

        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.moveFunctions = {"p": self.getAllPawnMoves, "R": self.getAllRookMoves, "N": self.getAllKnightMoves, "B": self.getAllBishopMoves,
                              "Q": self.getAllQueenMoves, "K": self.getAllKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = ()
        self.currentCastlingRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                               self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)]


    #Updating the board through board variable by getting starting and ending position.
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--' #Emptying the square of the frst click.
        self.board[move.endRow][move.endCol] = move.pieceMoved #Moving the piece to the second position.
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        if move.ispawnPromotion:
            x = input("Which piece you wanna convert your pawn into : \nR - Rook\nB - Bishop\nN - Knight\nQ - Queen\nEnter your piece keyword: ")
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + x

        # EnPassantMove

        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--'

        #update Enpassantpossible

        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()

        #castle move

        if move.isCastleMove:
            if move.endCol - move.startCol == 2: #kingside castle move
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1] #moves the rook to it's new square
                self.board[move.endRow][move.endCol+1] = '--' #erase old rook
            else: #queenside castle move
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2] #moves the rook to it's new square
                self.board[move.endRow][move.endCol-2] = '--' #erase old rook

        #update castling rights - whenever it is a rook or king move
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                               self.currentCastlingRights.wqs, self.currentCastlingRights.bqs))

    def undoMove(self):
        if len(self.moveLog) > 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

        #undo Enpassant

        if move.isEnpassantMove:
            self.board[move.endRow][move.endCol] = "--"
            self.board[move.startRow][move.endCol] = move.pieceCaptured
            self.enpassantPossible = (move.endRow, move.endCol)

        # undo a 2 move pawn advance
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ()

        #undo castle rights

        self.castleRightsLog.pop() #get rid of the new castle rights from the move we are undoing
        self.currentCastlingRights = self.castleRightsLog[-1] #set the current castle rights to the last one in the list

        #undo the casle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: #kingside catling

                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                self.board[move.endRow][move.endCol-1] = '--'

            else: #queenside Castling
                self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = '--'

    def updateCastleRights(self, move):

        '''
        Update the castle rights given the move
        '''
        if move.pieceCaptured == "wR":
            if move.end_col == 0: #left rook
                self.currentCastlingRights.wqs = False
            elif move.end_col == 7: #right rook
                self.currentCastlingRights.wks = False
        elif move.pieceCaptured == "bR":
            if move.end_col == 0: #left rook
                self.currentCastlingRights.bqs = False
            elif move.end_col == 7: #right rook
                self.currentCastlingRights.bks = False

        if move.pieceMoved == 'wK':
            self.currentCastlingRights.wqs = False
            self.currentCastlingRights.wks = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRights.bqs = False
            self.currentCastlingRights.bks = False
        elif move.pieceMoved == 'wR':
            if move.start_row == 7:
                if move.start_col == 0: #left rook
                    self.currentCastlingRights.wqs = False
                elif move.start_col == 7: #right rook
                    self.currentCastlingRights.wks = False
        elif move.pieceMoved == 'bR':
            if move.start_row == 0:
                if move.start_col == 0: #left rook
                    self.currentCastlingRights.bqs = False
                elif move.start_col == 7: #right rook
                    self.currentCastlingRights.bks = False
            

    def getValidMoves(self):

        """
        All moves considering checks.
        """
        # advanced algorithm
        moves = []
        self.in_check, self.pins, self.checks = self.checkForPinsAndChecks()

        if self.whiteToMove:
            king_row = self.whiteKingLocation[0]
            king_col = self.whiteKingLocation[1]
        else:
            king_row = self.blackKingLocation[0]
            king_col = self.blackKingLocation[1]
        if self.in_check:
            if len(self.checks) == 1:  # only 1 check, block the check or move the king
                moves = self.getAllPossibleMoves()
                # to block the check you must put a piece into one of the squares between the enemy piece and your king
                check = self.checks[0]  # check information
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col]
                valid_squares = []  # squares that pieces can move to
                # if knight, must capture the knight or move your king, other pieces can be blocked
                if piece_checking[1] == "N":
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i)  # check[2] and check[3] are the check directions
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:  # once you get to piece and check
                            break
                # get rid of any moves that don't block check or move king
                for i in range(len(moves) - 1, -1, -1):  # iterate through the list backwards when removing elements
                    if moves[i].pieceMoved[1] != "K":  # move doesn't move king so it must block or capture
                        if not (moves[i].endRow, moves[i].endCol) in valid_squares:  # move doesn't block or capture piece
                            moves.remove(moves[i])
            else:  # double check, king has to move
                self.getAllKingMoves(king_row, king_col, moves)
        else:  # not in check - all moves are fine
            moves = self.getAllPossibleMoves()
            if self.whiteToMove:
                self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
            else:
                self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        if len(moves) == 0:
            if self.inCheck():
                self.checkmate = True
            else:
                # TODO stalemate on repeated moves
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        return moves

    '''
    Determine if the current player is in check
    '''
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])


    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False


    def getAllPossibleMoves(self):
        moves = []
        for r in range(8):
            for c in range(8):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    try:
                        self.moveFunctions[piece](r, c, moves)
                    except KeyError:
                        pass

        return moves


    def checkForPinsAndChecks(self):
        pins = []  # squares pinned and the direction its pinned from
        checks = []  # squares where enemy is applying a check
        in_check = False
        if self.whiteToMove:
            enemy_color = "b"
            ally_color = "w"
            start_row = self.whiteKingLocation[0]
            start_col = self.whiteKingLocation[1]
        else:
            enemy_color = "w"
            ally_color = "b"
            start_row = self.blackKingLocation[0]
            start_col = self.blackKingLocation[1]
        # check outwards from king for pins and checks, keep track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            direction = directions[j]
            possible_pin = ()  # reset possible pins
            for i in range(1, 8):
                end_row = start_row + direction[0] * i
                end_col = start_col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != "K":
                        if possible_pin == ():  # first allied piece could be pinned
                            possible_pin = (end_row, end_col, direction[0], direction[1])
                        else:  # 2nd allied piece - no check or pin from this direction
                            break
                    elif end_piece[0] == enemy_color:
                        enemy_type = end_piece[1]
                        # 5 possibilities in this complex conditional
                        # 1.) orthogonally away from king and piece is a rook
                        # 2.) diagonally away from king and piece is a bishop
                        # 3.) 1 square away diagonally from king and piece is a pawn
                        # 4.) any direction and piece is a queen
                        # 5.) any direction 1 square away and piece is a king
                        if (0 <= j <= 3 and enemy_type == "R") or (4 <= j <= 7 and enemy_type == "B") or (
                                i == 1 and enemy_type == "p" and (
                                (enemy_color == "w" and 6 <= j <= 7) or (enemy_color == "b" and 4 <= j <= 5))) or (
                                enemy_type == "Q") or (i == 1 and enemy_type == "K"):
                            if possible_pin == ():  # no piece blocking, so check
                                in_check = True
                                checks.append((end_row, end_col, direction[0], direction[1]))
                                break
                            else:  # piece blocking so pin
                                pins.append(possible_pin)
                                break
                        else:  # enemy piece not applying checks
                            break
                else:
                    break  # off board
        # check for knight checks
        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        for move in knight_moves:
            end_row = start_row + move[0]
            end_col = start_col + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == "N":  # enemy knight attacking a king
                    in_check = True
                    checks.append((end_row, end_col, move[0], move[1]))
        return in_check, pins, checks


    def getAllPawnMoves(self, r, c, moves):

        """
        Get all the rook moves for the rook located at row, col and add the moves to the list.
        """

        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:
            move_amount = -1
            start_row = 6
            enemy_color = "b"
        else:
            move_amount = 1
            start_row = 1
            enemy_color = "w"

        if self.board[r+move_amount][c] == "--": #1 square pawn advance
            if not piece_pinned or pin_direction == (move_amount, 0):
                moves.append(Move((r, c), (r + move_amount, c), self.board))
                if r == start_row and self.board[r + 2 * move_amount][c] == "--": #2 square pawn advance
                    moves.append(Move((r, c), (r + 2 * move_amount, c), self.board))
        if c - 1 >= 0: #capture to the left
            if not piece_pinned or pin_direction == (move_amount, -1):
                if self.board[r + move_amount][c - 1][0] == enemy_color:
                    moves.append(Move((r, c), (r + move_amount, c - 1), self.board))
                if (r + move_amount, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + move_amount, c - 1), self.board, isEnpassantMove = True))
        if c + 1 <= 7: #capture to the right
            if not piece_pinned or pin_direction == (move_amount, +1):
                if self.board[r + move_amount][c +1][0] == enemy_color:
                    moves.append(Move((r, c), (r + move_amount, c + 1), self.board))
                if (r + move_amount, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + move_amount, c + 1), self.board, isEnpassantMove = True))


    def getAllRookMoves(self, r, c, moves):

        """
        Get all the rook moves for the rook located at row, col and add the moves to the list.
        """

        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != "Q": #can't remove queen from pin on rook moves, only remove it on bishop moves
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
        enemy_color = "b" if self.whiteToMove else "w"
        for direction in directions:
            for i in range(1, 8):
                end_row = r + direction[0] * i
                end_col = c + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # check for possible moves only in boundaries of the board
                    if not piece_pinned or pin_direction == direction or pin_direction == (-direction[0], -direction[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":  # empty space is valid
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:  # capture enemy piece
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                            break
                        else:  # friendly piece
                            break
                else:  # off board
                    break


    def getAllKnightMoves(self, r, c, moves):
        """
        Get all the knight moves for the knight located at row col and add the moves to the list.
        """

        piece_pinned = False
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break

        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
                        # up/left up/right right/up right/down down/left down/right left/up left/down
        ally_color = "w" if self.whiteToMove else "b"
        for move in knight_moves:
            end_row = r + move[0]
            end_col = c + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                if not piece_pinned:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color:  # so its either enemy piece or empty square
                        moves.append(Move((r, c), (end_row, end_col), self.board))


    def getAllBishopMoves(self, r, c, moves):
        """
        Get all the bishop moves for the bishop located at row col and add the moves to the list.
        """

        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))  # diagonals: up/left up/right down/right down/left
        enemy_color = "b" if self.whiteToMove else "w"
        for direction in directions:
            for i in range(1, 8):
                end_row = r + direction[0] * i
                end_col = c + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # ch2eck if the move is on board
                    if not piece_pinned or pin_direction == direction or pin_direction == (-direction[0], -direction[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":  # empty space is valid
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:  # capture enemy piece
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                            break
                        else:  # friendly piece
                            break
                else:  # off board
                    break


    def getAllQueenMoves(self, row, col, moves):
        """
        Get all the queen moves for the queen located at row col and add the moves to the list.
        """
        self.getAllBishopMoves(row, col, moves)
        self.getAllRookMoves(row, col, moves)


    def getAllKingMoves(self, row, col, moves):
        """
        Get all the king moves for the king located at row col and add the moves to the list.
        """
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        ally_color = "w" if self.whiteToMove else "b"
        for i in range(8):
            end_row = row + row_moves[i]
            end_col = col + col_moves[i]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:  # not an ally piece - empty or enemy
                    # place king on end square and check for checks
                    if ally_color == "w":
                        self.whiteKingLocation = (end_row, end_col)
                    else:
                        self.blackKingLocation = (end_row, end_col)
                    in_check, pins, checks = self.checkForPinsAndChecks()
                    if not in_check:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    # place king back on original location
                    if ally_color == "w":
                        self.whiteKingLocation = (row, col)
                    else:
                        self.blackKingLocation = (row, col)
                        
    def getCastleMoves(self, r, c, moves):
        '''
        Generate all valid castle moves for the king at (r, c) and add them to the list of moves.
        '''
        if self.squareUnderAttack(r, c):
            return #can't castle while in check
        if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.getQuennsideCastleMoves(r, c, moves)
        
    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove = True))
    
    def getQuennsideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMove = True))

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move():

    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False):

        #Getting row and column value of starting and ending position of the square.
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol] #Storing the particular piece present in the square.
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.ispawnPromotion = (self.endRow == 0 and self.pieceMoved == 'wp') or (self.endRow == 7 and self.pieceMoved == 'bp')
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
        self.isCastleMove = isCastleMove

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        """
        Overriding the equals method.
        """
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    #Mapping python location values to it's real notation.
    rowsToRanks = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}
    colsToFiles = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}


    #Getting real chess notation of every move.
    def getChessNotation(self):
        return self.getRanks(self.startRow, self.endRow) + self.getRanks(self.endRow, self.endCol)

    def getRanks(self, r, c):
        return self.rowsToRanks[r] + self.colsToFiles[c]


