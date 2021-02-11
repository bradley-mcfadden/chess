import board
import piece
import point

class History:
    def __init__(self, source: point.Point, dest: point.Point, board: board.Board, prev: History, killed: piece.Piece, mt: Piece.MoveType):
        self._board = board
        self._from = source
        self._to = dest
        self._killed_piece = killed
        self._mt = mt

        self._next: History = None
        self._prev: History = prev

    def set_next(self, next: History):
        self._next = next

    # Resets board to pervious move
    def undo_last(self) -> History:
        prev: History = self._prev
        if not prev:
            raise Exception("Undo caled when at first move.")
       
        mtype: piece.MoveType = prev.mt()

        if mtype == piece.MoveType.NORMAL: # handle normal moves
            pass
        elif mtype == piece.MoveType.DOUBLESTEP: # handle doublestep
            pass
        elif mtype == piece.MoveType.ENPASSANT: # handle enpassant
            pass
        elif mtype == piece.MoveType.CASTLE: # handle castling
            pass
        elif mtype == piece.MoveType.PROMOTION: # handle pawn promotion
            pass

        return prev

    # Advances board to next move (if there is one)
    def redo_move(self) -> History:
        next_: History = self._next
        if not next_:
            raise Exception("Redo called when at latest change.")

        mtype: piece.MoveType = next_.mt()

        if mtype == piece.MoveType.NORMAL: # handle normal moves
            pass
        elif mtype == piece.MoveType.DOUBLESTEP: # handle doublestep
            pass
        elif mtype == piece.MoveType.ENPASSANT: # handle enpassant
            pass
        elif mtype == piece.MoveType.CASTLE: # handle castling
            pass
        elif mtype == piece.MoveType.PROMOTION: # handle pawn promotion
            pass
        return next

    def from_(self) -> point.Point:
        return self._from

    def to(self) -> point.Point:
        return self._to

    def killed_piece(self) -> piece.Piece:
        return self._killed_piece

    def mt(self) -> piece.MoveType:
        return self._mt

    def next_(self) -> History:
        return self._next

    def prev(self) -> History:
        return self._prev