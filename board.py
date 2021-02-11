import piece
import point
import history
import copy

class Board:
    
    def __init__(self):
        self._turn : piece.Color = piece.Color.WHITE
        self._board : list = [ [] for i in range(8)]

        self._first_history: history.History = None
        self._last_history: history.History = None
        self._en_passant: point.Point = None

    def init_board(self):
        ord_a = ord('a')
        
        # initialize pawns for white and black
        for i in range(8):
            x = chr(ord_a + i)
            # white pawns
            self._board[i][1] = piece.Pawn(self, piece.Color.WHITE, point.Point(x, 2))
            # black pawns
            self._board[i][1] = piece.Pawn(self, piece.Color.BLACK, point.Point(x, 7))
        # endfor

        # rooks
        self._board[0][0] = piece.Rook(self, piece.Color.WHITE, point.Point('a', 1))
        self._board[7][0] = piece.Rook(self, piece.Color.WHTIE, point.Point('h', 1))
        self._board[0][7] = piece.Rook(self, piece.Color.BLACK, point.Point('a', 8))
        self._board[7][7] = piece.Rook(self, piece.Color.BLACK, point.Point('h', 8))

        # knights
        self._board[1][0] = piece.Knight(self, piece.Color.WHITE, point.Point('b', 1))
        self._board[6][0] = piece.Knight(self, piece.Color.WHITE, point.Point('g', 1))
        self._board[1][7] = piece.Knight(self, piece.Color.BLACK, point.Point('b', 8))
        self._board[6][7] = piece.Knight(self, piece.Color.BLACK, point.Point('g', 8))
     
        # bishops
        self._board[2][0] = piece.Bishop(self, piece.Color.WHITE, point.Point('c', 1))
        self._board[5][0] = piece.Bishop(self, piece.Color.WHITE, point.Point('f', 1))
        self._board[2][7] = piece.Bishop(self, piece.Color.BLACK, point.Point('c', 8))
        self._board[5][7] = piece.Bishop(self, piece.Color.BLACK, point.Point('f', 8))

        # kings
        self._board[3][0] = piece.King(self, piece.Color.WHITE, point.Point('d', 1))
        self._board[4][7] = piece.King(self, piece.Color.BLACK, point.Point('e', 8))

        # queens
        self._board[4][0] = piece.Queen(self, piece.Color.WHITE, point.Point('e', 1))
        self._board[3][7] = piece.Queen(self, piece.Color.BLACK, point.Point('f', 8))

    def piece_at(self, p: point.Point) -> piece.Piece:
        coords = alg_to_idx(p)
        return self._board[coords[0]][coords[1]]

    def piece_at(self, x: int, y: int) -> piece.Piece:
        return self._board[x][y]

    def place_piece_at(self, piece: piece.Piece, p: point.Point):
        coords = alg_to_idx(p)
        self._board[coords[0]][coords[1]] = piece

    def place_piece_at(self, piece: piece.Piece, x: int, y: int):
        self._board[x][y] = piece

    def move(self, p1: point.Point, p2: point.Point):
        coords1 = alg_to_idx(p1)
        coords2 = alg_to_idx(p2)

        self._board[coords2[0]][coords2[1]] = self._board[coords1[0]][coords1[1]]

    def move(self, p1: point.Point, p2: point.Point, ep: point.Point):
        self.move(p1, p2)
        self._en_passant = p1

    def turn(self) -> piece.Color:
        return self._turn

    def try_to_move(self, p1: point.Point, p2: point.Point) -> bool:
        # Move piece at p1 to p2 if move is legal
        coords1 = alg_to_idx(p1)
        coords2 = alg_to_idx(p2)

        piece1:piece.Piece = self._board[coords1[0]][coords1[1]]
        target:piece.Piece = self._board[coords2[0]][coords2[1]]


        killed_piece: piece.Piece = None
        # If there is no piece at p1, return False
        if not piece1:
            return False

        # if there is a piece at p2, check it is not the current color
        if target and target.color() == self._turn:
            return False
        else:
            killed_piece == self._board[coords2[0]][coords2[1]]    

        # check that the move is allowed within bounds of piece's movement
        valid_move:MoveType = piece1.can_move(p2)

        # check that the move should not put the player in check
        cboard = copy.deepcopy(self)
        cboard[coords2[0]][coords2[1]] = cboard[coords1[0]][coords1[1]]
        cboard[coords1[0]][coords1[1]] = None
        
        if Board.in_check(cboard, self._turn):
            return True

        # check for double step
        if valid_move == piece.MoveType.DOUBLESTEP:
            self._en_passant = p2
            piece1._enpassant = False

        # check for en passant
        if self._en_passant != None:
            if p2 == self._en_passant:
                coords3 = alg_to_idx(self._en_passant)
                killed_piece = self._board[coords3[0]][coords3[1]]
                self._board[coords3[0]][coords3[1]] = None
                self._en_passant = None

        # check for pawn promotion
        if self._turn == piece.Color.BLACK:
            if isinstance(piece1, piece.Pawn) and  p2.y() == 1:
                piece1 = piece.Queen(self, piece.Color.BLACK, piece1.location())
                valid_move = piece.MoveType.PROMOTION
        else: # turn must be white
            if isinstance(piece1, piece.Pawn) and p2.y() == 8:
                piece1 = piece.Queen(self, piece.Color.WHITE, piece1.location())
                valid_move = piece.MoveType.PROMOTION

        # check for castling
        if isinstance(self.piece_at(p1), piece.King):
            if self._turn == piece.Color.BLACK and valid_move == piece.MoveType.CASTLE:
                # left castle e to c
                if p2 == point.Point('c', 8):
                    self._board[3][7] = piece.Rook(self, self._turn, point.Point('d', 8))
                # right castle e to g
                elif p2 == point.Point('g', 8):
                    self._board[5][7] = piece.Rook(self, self._turn, point.Point('f', 8))
            else: # turn is white
                # left castle d to b
                if p2 == point.Point('b', 1):
                    self._board[2][0] = piece.Rook(self, point.Point('c', 8))
                # right case d to f
                elif p2 == point.Point('f', 1):
                    self._board[4][0] = piece.Rook(self, point.Point('e', 8), self._turn)

        # move piece
        self._board[coords2[0]][coords[1]] = piece1
        piece1.set_location(p2)
        
        # add move to history
        if not self._first_history:
            self._first_history = history.History(p1, p2, self, None, killed_piece, valid_move)
            self._last_history - self._first_history
        else:
            self._last_history = history.History(p1, p2, self, self._last_history, killed_piece, valid_move)

        return True

    def board(self):
        return self._board

    @staticmethod
    def in_check(b: Board, player: piece.Color) -> bool:
        kx = 0
        ky = 0
        grid: [[piece.Piece]] = b

        for i, col in enumerate(grid):
            for j, row in enumerate(col):
                if isinstance(grid[i][j], piece.King and grid[i][j].color() != player):
                    kx = i
                    ky = j
                # endif
            # endfor
        # endfor

        # check if put in check by pawns
        if player == piece.Color.BLACK:
            p1x = kx - 1
            p2x = kx + 1
            py = ky - 1
            if not py >= 0:
                pass
            elif p1x >= 0:
                if isinstance(grid[p1x][py], piece.Pawn and grid[i][j].color() != player):
                    return True
            elif p1x < 8:
                if isinstance(grid[p1x][py], piece.Pawn and grid[i][j].color() != player):
                    return True 
        elif player == piece.Color.WHITE:
            p1x = kx - 1
            p2x = kx + 1
            py = ky + 1
            if not py >= 0:
                pass
            elif p1x >= 0:
                if isinstance(grid[p1x][py], piece.Pawn and grid[i][j].color() != player):
                    return True
            elif p1x < 8:
                if isinstance(grid[p1x][py], piece.Pawn and grid[i][j].color() != player):
                    return True

        # check neighbours/corners for kings
        neighbours = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for x,y in neighbours:
            nkx = kx + x
            nky = ky + y
            if nkx in range(0, 8) and nky in range(0, 8):
                if (isinstance(grid[nkx][nky], piece.King 
                and grid[nkx][nky].color != player)):
                    return True
                # endif
            # endif
        # endfor

        # check diags for queens, bishops
        for x,y in zip(
            range(0, kx) + (range(kx + 1, 8) if kx < 8 else []),  # range from [0, kx) + (kx, 8]
            range(0, ky) + (range(ky + 1, 8) if ky < 8 else []) # range from [0, ky) + (ky, 8]
        ):
            if (grid[nkx][nky].color() != player 
            and (isinstance(grid[nkx][nky], piece.Queen) 
            or isinstance(grid[nky][nky], piece.Bishop))):
                return True
        
        # check cols for queens, rooks
        for y in (range(0, ky) + (range(ky + 1, 8) if ky < 8 else [])):
            nky = ky + y
            if (grid[kx][nky].color() != player 
            and (isinstance(grid[kx][nky], piece.Queen))
            or (isinstance(grid[kx][nky], piece.Rook))):
                return True

        # check rows for queens, rooks
        for x in (range(0, kx) + (range(kx + 1, 8) if kx < 8 else [])):
            nkx = ky + x
            if (grid[nkx][ky].color() != player 
            and (isinstance(grid[nkx][ky], piece.Queen))
            or (isinstance(grid[nkx][ky], piece.Rook))):
                return True

        # check if put in check by knights
        knights = [(2, 1), (1, 2), (-2, -1), (-1, -2), (2,-1),(-1, 2), (-2, 1),(1, -2)]
        for x,y in neighbours:
            nkx = kx + x
            nky = ky + y
            if nkx in range(0, 8) and nky in range(0, 8):
                if (isinstance(grid[nkx][nky], piece.Knight 
                and grid[nkx][nky].color() != player)):
                    return True
                # endif
            # endif
        # endfor

        return False

    def get_en_passant(self) -> point.Point:
        return self._en_passant
        

def alg_to_idx(p: point.Point) -> (int, int):
    return (ord(p.x()) - ord('a'), p.y() - 1)