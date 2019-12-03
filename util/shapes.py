from typing import Tuple, List

from objects import Compass


class Polygon:
    def __init__(self, points: List[Tuple[float, float]]):
        self.points = points
        self.direction = Compass.RIGHT

    def get_points(self, offset_x: float = 0, offset_y: float = 0, direction: Compass.Direction = Compass.RIGHT, scale: float = 1.0) -> List[Tuple[float, float]]:
        if direction is Compass.RIGHT:
            return [(x * scale + offset_x, y * scale + offset_y) for x, y in self.points]

        if direction is Compass.LEFT:
            return [((1 - x) * scale + offset_x, (1 - y) * scale + offset_y) for x, y in self.points]

        if direction is Compass.DOWN:
            return [((1 - y) * scale + offset_x, x * scale + offset_y) for x, y in self.points]

        if direction is Compass.UP:
            return [(y * scale + offset_x, (1 - x) * scale + offset_y) for x, y in self.points]


class ArrowShape(Polygon):
    stock_height = 0.5
    head_width = 0.5

    def __init__(self):
        #  (0, 1 - (1 - self.stock_height)/2)
        super().__init__([(0, (1 - self.stock_height)/2), (1 - self.head_width, (1 - self.stock_height)/2),
                          (1 - self.head_width, 0), (1, 0.5), (1 - self.head_width, 1),
                          (1 - self.head_width, (1 + self.stock_height)/2), (0, (1 + self.stock_height)/2)])


class Shapes:
    ARROW = ArrowShape()