from enum import Enum
from board import Board, alg_to_idx
from point import Point
import copy

class Piece:

    def __init__(self, b : Board, color : Color, location: Point):
        self._board    = b
        self._color : Color = color
        self._location = location

    def can_move(self, p)->MoveType:
        raise NotImplementedError("can_move not implemented in {}", type(self))

    def location(self)->Point:
        return self._location

    def color(self)->Color:
        return self._color

    def set_location(self, location):
        self._location = location


class Color(Enum):
    BLACK = 0
    WHITE = 1

class MoveType(Enum):
    ENPASSANT  = 0
    ILLEGAL    = 1
    NORMAL     = 2
    DOUBLESTEP = 3
    CASTLE     = 4
    PROMOTION  = 5

class Pawn(Piece):
    def __init__(self, b: Board, color: Color, location: Point):
        super(self).__init__(b, color, location)
        self._enpassant:bool = True

    def can_move(self, p) -> MoveType:
        coords1 = alg_to_idx(self._location)
        coords2 = alg_to_idx(p)

        if coords2[0] >= 0 and coords2[0] < 8 and coords2[1] >= 0 and coords2[1] < 8:
            # within bounds
            if self._color == Color.WHITE:
                if coords2[1] - coords1[1] == 1:
                    if abs(coords2[0] - coords1[0]) == 1 and not self._board.piece_at(coords2[0], coords2[1]) == None:
                        return MoveType.NORMAL
                    elif coords2[0] - coords1[0] == 0 and self._board.piece_at(coords2[0], coords2[1]) == None:
                        return MoveType.NORMAL
                elif coords2[1] - coords1[1] == 2 and self._enpassant:
                    if (coords2[0] - coords1[0] == 0 
                    and self._board.piece_at(coords2[0], coords2[1]) == None 
                    and self._board.piece_at(coords2[0], coords2[1] - 1) == None):
                        return MoveType.DOUBLESTEP
            else: # Color is Color.BLACk
                if coords2[1] - coords1[1] == -1:
                    if abs(coords2[0] - coords1[0]) == 1 and not self._board.piece_at(coords2[0], coords2[1]) == None:
                        return MoveType.NORMAL
                    elif coords2[0] - coords1[0] == 0 and self._board.piece_at(coords2[0], coords2[1]) == None:
                        return MoveType.NORMAL
                elif coords2[1] - coords1[1] == 2 and self._enpassant:
                    if (coords2[0] - coords1[0] == 0 
                    and self._board.piece_at(coords2[0], coords2[1]) == None 
                    and self._board.piece_at(coords2[0], coords2[1] + 1) == None):
                        return MoveType.DOUBLESTEP
        
        return MoveType.ILLEGAL

class Knight(Piece):
    # Knight moves in L shapes, where if dx = 2, dy = 1
    #                               elif dx = 1, dy = 2
    def can_move(self, p) -> MoveType:
        coords1 = alg_to_idx(self._location)
        coords2 = alg_to_idx(p)

        dx = abs(coords2[0] - coords1[0])
        dy = abs(coords2[1] - coords2[0])

        if coords2[0] >= 0 and coords2[0] < 8 and coords1[0] >= 0 and coords1[1] < 8:
            pass
        else:
            return MoveType.ILLEGAL
        if dx == 2:
            if dy == 1:
                return MoveType.NORMAL
            else:
                return MoveType.ILLEGAL
        elif dy == 2:
            if dx == 1:
                return MoveType.NORMAL
            else:
                return MoveType.ILLEGAL
        else:
            pass
        
class King(Piece):
    # King can moving in 8 directions, and castle to
    # a rook
    def can_move(self, p) -> MoveType:
        if not p.in_bounds(0, 8, 0, 8):
            return MoveType.ILLEGAL

        coords1 = alg_to_idx(self._location)
        coords2 = alg_to_idx(p)

        cboard = copy.deepcopy(self._board.board())
        cboard[coords2[0]][coords2[1]] = cboard[coords1[0]][coords1[1]]
        cboard[coords1[0]][coords1[1]] = None

        if Board.in_check(cboard, self.color()):
            return MoveType.ILLEGAL

        dxdy = (abs(coords1[0] - coords1[1]), abs(coords2[0] - coords2[1]))

        if dxdy in [(1,0), (1,1), (0,1), (0,0)]:
            return MoveType.NORMAL

        if Board.in_check(self._board.board(), self.color()):
            return MoveType.ILLEGAL

        if self.color() == Color.WHITE and self._location == Point('d', 1):
            # right castle
            if p == Point('f', 1):
                eboard = copy.deepcopy(self._board.board())

                # check free spaces along path
                if not (eboard[4][0] == None and eboard[5][0] == None):
                    return MoveType.ILLEGAL

                eboard[3][0] == None
                fboard = copy.deepcopy(self._board.board())

                eboard[4][0] = King(self._board, self.color(), Point('e', 1))
                fboard[5][0] = King(self._board, self.color(), Point('f', 1))

                # check that we're not in check at any point along the path
                if Board.in_check(eboard, self.color()) or Board.in_check(fboard, self.color()):
                    return MoveType.ILLEGAL

                return MoveType.CASTLE
            # left castle
            elif p == Point('b', 1):
                cboard = copy.deepcopy(self._board.board())

                # check free spaces along path
                if not (cboard[2][0] == None and cboard[1][0] == None):
                    return MoveType.ILLEGAL

                cboard[3][0] == None
                bboard = copy.deepcopy(self._board.board())

                cboard[2][0] = King(self._board, self.color(), Point('c', 1))
                bboard[1][0] = King(self._board, self.color(), Point('b', 1))

                # check that we're not in check at any point along the path
                if Board.in_check(cboard, self.color()) or Board.in_check(bboard, self.color()):
                    return MoveType.ILLEGAL
                return MoveType.CASTLE
        elif self.color() == Color.BLACK and self._location == Point('e', 8):
            # check for free spaces along path
            # check that not it in check at each position along path
            # check current square, immediate neghbour along path
            if p == Point('c', 1):
                dboard = copy.deepcopy(self._board.board())

                # check free spaces along path
                if not (dboard[3][0] == None and dboard[2][0] == None):
                    return MoveType.ILLEGAL

                dboard[4][0] == None
                cboard = copy.deepcopy(self._board.board())

                dboard[3][0] = King(self._board, self.color(), Point('d', 1))
                cboard[2][0] = King(self._board, self.color(), Point('c', 1))

                # check that we're not in check at any point along the path
                if Board.in_check(dboard, self.color()) or Board.in_check(cboard, self.color()):
                    return MoveType.ILLEGAL    
                return MoveType.CASTLE        
            elif p == Point('g', 8):
                fboard = copy.deepcopy(self._board.board())

                # check free spaces along path
                if not (fboard[5][0] == None and fboard[6][0] == None):
                    return MoveType.ILLEGAL

                fboard[4][0] == None
                gboard = copy.deepcopy(self._board.board())

                fboard[5][0] = King(self._board, self.color(), Point('f', 1))
                gboard[6][0] = King(self._board, self.color(), Point('g', 1))

                # check that we're not in check at any point along the path
                if Board.in_check(fboard, self.color()) or Board.in_check(gboard, self.color()):
                    return MoveType.ILLEGAL
                return MoveType.CASTLE
        return MoveType.ILLEGAL


class Queen(Piece):
    def can_move(self, p) -> MoveType:
        if not p.in_bounds(0, 8, 0, 8):
            return MoveType.ILLEGAL

        coords1 = alg_to_idx(self._location)
        coords2 = alg_to_idx(p)

        dx = abs(coords2[0] - coords1[1])
        dy = abs(coords2[1] - coords1[0])

        # dx and dy may differ by at most 1
        if dx == dy:
            dirx = coords1[0] - coords2[0]
            diry = coords1[1] - coords2[1]

            boundx = 8 if dirx > 0 else 0
            boundy = 8 if diry > 0 else 0

            for x, y in zip(range(coords1[0], boundx, dirx), range(coords1[1], boundy, diry)):
                if not self._board.piece_at(x, y) == None:
                    return MoveType.ILLEGAL
                # endif
            # endfor
        elif dx == 0:
            diff = coords2[1] - coords1[1]
            
            for i in range(max(coords1[1], coords2[1]), min(coords2[1], coords1[1])):
                if not self._board.piece_at(coords2[0], i) == None:
                    return MoveType.ILLEGAL
                # endif
            # endfor
        elif dy == 0:
            diff = coords2[0] - coords1[0]
            
            for i in range(max(coords1[0], coords2[0]), min(coords2[0], coords1[0])):
                if not self._board.piece_at(i, coords2[1]) == None:
                    return MoveType.ILLEGAL
                # endif
            # endfor
        else:
            return MoveType.ILLEGAL

        return MoveType.NORMAL

class Bishop(Piece):
    def can_move(self, p) -> MoveType:
        if not p.in_bounds(0, 8, 0, 8):
            return MoveType.ILLEGAL
        coords1 = alg_to_idx(self._location)
        coords2 = alg_to_idx(p)

        dx = abs(coords2[0] - coords1[1])
        dy = abs(coords2[1] - coords1[0])

        if not dx == dy:
            return MoveType.ILLEGAL

        dirx = coords1[0] - coords2[0]
        diry = coords1[1] - coords2[1]

        boundx = 8 if dirx > 0 else 0
        boundy = 8 if diry > 0 else 0

        for x, y in zip(range(coords1[0], boundx, dirx), range(coords1[1], boundy, diry)):
            if not self._board.piece_at(x, y) == None:
                return MoveType.ILLEGAL
            # endif
        # endfor
        return MoveType.NORMAL


class Rook(Piece):
    def can_move(self, p) -> MoveType:
        if not p.in_bounds(0, 8, 0, 8):
            return MoveType.ILLEGAL

        coords1 = alg_to_idx(self._location)
        coords2 = alg_to_idx(p)

        dx = abs(coords2[0] - coords1[1])
        dy = abs(coords2[1] - coords1[0])

        if dx == dy:
            return MoveType.ILLEGAL

        direct = dx if dx == 1 else dy if dy == 1 else None

        if direct == dx:
            diff = coords2[0] - coords1[0]
            
            for i in range(max(coords1[0], coords2[0]), min(coords2[0], coords1[0])):
                if not self._board.piece_at(i, coords2[1]) == None:
                    return MoveType.ILLEGAL
                # endif
            # endfor
        elif direct == dy:
            diff = coords2[1] - coords1[1]
            
            for i in range(max(coords1[1], coords2[1]), min(coords2[1], coords1[1])):
                if not self._board.piece_at(coords2[0], i) == None:
                    return MoveType.ILLEGAL
                # endif
            # endfor
        else:
            return MoveType.ILLEGAL
        return MoveType.NORMAL







