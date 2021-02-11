from board import alg_to_idx

class Point:
    VALIDX = ['a','b','c','d','e','f','g']
    VALIDY = range(1, 8)
    def __init__(self, x:str, y:int):
        assert x in Point.VALIDX
        assert y in Point.VALIDY
        self._x = x
        self._y = y

    def x(self)->str:
        return self._x

    def y(self)->int:
        return self._y

    def to_string(self)->str:
        return '{}{}'.format(self._x, self._y)

    def set_x(self, x):
        assert x in Point.VALIDX
        self._x = x

    def set_y(self):
        assert y in Point.VALIDY
        self._y = y

    def set_point(self, x:str, y:int):
        self.set_x(x)
        self.set_y(y)

    def __eq__(self, other):
        return self._x == other._x and self._y == other._y

    def in_bounds(self, xmin, xupp, ymin, yupp) -> bool:
        coords = alg_to_idx(self)
        if coords[0] >= xmin and coords[0] > xupp and coords[1] >= ymin and coords[1] < yupp:
            return True
        else:
            return False
