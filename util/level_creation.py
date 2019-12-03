from objects import Holder, Trashcan, Compass
from types import SimpleNamespace
from typing import Tuple


def range_direction(holder: Holder, direction: Compass.Direction, ignore_inactive: bool = True):
    yield holder
    while holder.has_neighbor(direction):
        yield holder.get_neighbor(direction, ignore_inactive=ignore_inactive)
        holder = holder.get_neighbor(direction, ignore_inactive=ignore_inactive)


def range_grid(top_left: Holder, ignore_border: bool = False) -> Tuple[Tuple[int, int], Holder]:
    for h, column_header in enumerate(range_direction(top_left, Compass.RIGHT)):
        for k, holder in enumerate(range_direction(column_header, Compass.DOWN)):
            if ignore_border and isinstance(holder, Trashcan):
                continue
            yield SimpleNamespace(x=h - 1 if ignore_border else h, y=k - 1 if ignore_border else k), holder


def make_grid(height: int, width: int):
    top_left: Holder = Trashcan()
    current: Holder = top_left

    # Construct (most of) the left side border
    lower: Holder = extend(current, height - 1, Compass.DOWN, Trashcan)

    # Construct main play field
    for holder in range_direction(top_left.get_neighbor(Compass.DOWN), Compass.DOWN):
        extend(holder, width - 1, Compass.RIGHT, Holder)

    # Construct the rest of the left side border and finish up
    bottom_left: Holder = Trashcan()
    bottom_left.add_neighbor(Compass.UP, lower)
    lower.add_neighbor(Compass.DOWN, bottom_left)

    bottom_right: Holder = extend(bottom_left, width, Compass.RIGHT, Trashcan)

    top_right: Holder = extend(bottom_right, height, Compass.UP, Trashcan)

    almost_top_left: Holder = extend(top_right, width - 1, Compass.LEFT, Trashcan)

    almost_top_left.add_neighbor(Compass.LEFT, top_left)
    top_left.add_neighbor(Compass.RIGHT, almost_top_left)

    return top_left


def extend(start: Holder, length: int, direction: Compass.Direction, holder_type, do_parallel = True) -> Holder:
    p1, p2 = Compass.get_parallel(direction)

    current = start

    for _ in range(length - 1):
        adding: Holder = holder_type()
        current.add_neighbor(direction, adding)
        #  "~direction" flips the direction 180 degrees IE Up becomes Down, Left becomes Right ect.
        adding.add_neighbor(~direction, current)

        #  Determines if there is a neighboring cell that needs to be included
        do_p1 = do_parallel and current.has_neighbor(p1) and current.get_neighbor(p1).has_neighbor(direction)
        do_p2 = do_parallel and current.has_neighbor(p2) and current.get_neighbor(p2).has_neighbor(direction)

        if do_p1:
            adding.add_neighbor(p1, current.get_neighbor(p1).get_neighbor(direction))
            current.get_neighbor(p1).get_neighbor(direction).add_neighbor(p2, adding)

        if do_p2:
            adding.add_neighbor(p2, current.get_neighbor(p2).get_neighbor(direction))
            current.get_neighbor(p2).get_neighbor(direction).add_neighbor(p1, adding)

        current = current.get_neighbor(direction)

    return current


def print_grid(top_left: Holder):
    for i, left in enumerate(range_direction(top_left, Compass.DOWN)):
        row = ""
        for j, holder in enumerate(range_direction(left, Compass.RIGHT)):
            if isinstance(holder, Trashcan):
                char = str(i) if i > j else str(j)
            else:
                if holder.is_active():
                    char = str(holder.get_child()) if holder.has_child() else " "
                else:
                    char = "▒"
            row += char + (" " * (3 - len(char)))
        print(row)


if __name__ == '__main__':
    top_left: Holder = make_grid(20, 20)
    print_grid(top_left)
