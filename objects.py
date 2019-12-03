from typing import Dict, Tuple


class Compass:
    class Direction:
        def __init__(self, name):
            self.name = name

        def __str__(self):
            return self.name

        def __invert__(self):
            if self is Compass.UP:
                return Compass.DOWN
            if self is Compass.DOWN:
                return Compass.UP
            if self is Compass.LEFT:
                return Compass.RIGHT
            if self is Compass.RIGHT:
                return Compass.LEFT

    UP = Direction("up")
    DOWN = Direction("down")
    LEFT = Direction("left")
    RIGHT = Direction("right")

    @staticmethod
    def from_str(item):
        if item == "up":
            return Compass.UP
        if item == "down":
            return Compass.DOWN
        if item == "left":
            return Compass.LEFT
        if item == "right":
            return Compass.RIGHT

    @staticmethod
    def get_parallel(direction: Direction) -> Tuple[Direction, Direction]:
        if direction is Compass.UP or direction is Compass.DOWN:
            return Compass.LEFT, Compass.RIGHT
        else:
            return Compass.UP, Compass.DOWN


class Holder:
    def __init__(self):
        self.neighbors: Dict[Compass.Direction, Holder] = dict()
        self.entity: Entity = None
        self.active: bool = True

    def add_neighbor(self, direction: Compass.Direction, holder):
        self.neighbors[direction] = holder

    def get_neighbor(self, direction: Compass.Direction, ignore_inactive: bool = False):
        if self.has_neighbor(direction):
            neighbor: Holder = self.neighbors[direction]
            if neighbor.is_active() or ignore_inactive:
                return neighbor
            return neighbor.get_neighbor(direction)
        else:
            return None

    def has_neighbor(self, direction: Compass.Direction):
        return direction in self.neighbors

    def is_active(self) -> bool:
        return self.active

    def set_active(self, active: bool):
        self.active = active

    def toggle_active(self):
        self.set_active(not self.is_active())

    def is_empty(self) -> bool:
        return self.entity is None

    def clear(self):
        self.entity: Entity = None

    def get_child(self):
        return self.entity

    def set_child(self, entity):
        self.entity: Entity = entity

    def remove_child(self):
        if self.has_child():
            self.get_child().clear_parent()
        self.clear()

    def has_child(self) -> bool:
        return not self.is_empty()


class Trashcan(Holder):
    def is_active(self) -> bool:
        return True

    def is_empty(self) -> bool:
        return True

    def set_child(self, entity):
        pass


class Entity:
    pushable = False

    def __init__(self):
        self.parent: Holder = None

    def put_into(self, holder: Holder):
        holder.set_child(self)
        self.set_parent(holder)

    def set_parent(self, holder: Holder):
        self.parent = holder

    def get_parent(self) -> Holder:
        return self.parent

    def has_parent(self):
        return self.parent is not None

    def remove_parent(self):
        if self.has_parent():
            self.get_parent().clear()
        self.clear_parent()

    def clear_parent(self):
        self.parent = None

    def __str__(self):
        return "e"


class Actor(Entity):
    def __init__(self, index: int):
        super().__init__()
        self.index = index

    def get_index(self) -> int:
        return self.index

    def set_index(self, index: int):
        self.index = index

    def __str__(self):
        return "a"


class Arrow(Actor):
    pushable = True

    def __init__(self, direction: Compass.Direction, index: int):
        super().__init__(index)
        self.direction: Compass.Direction = direction

    def __str__(self):
        if self.direction is Compass.UP:
            return "↑"
        if self.direction is Compass.DOWN:
            return "↓"
        if self.direction is Compass.LEFT:
            return "←"
        if self.direction is Compass.RIGHT:
            return "→"


class Wall(Entity):
    def __str__(self):
        return "W"


class Rock(Entity):
    pushable = True

    def __str__(self):
        return "R"


class Core(Entity):
    pushable = True

    def __str__(self):
        return "R"
