from typing import List

from objects import Entity, Holder, Compass, Arrow
from util.level_creation import range_direction


def place(entity: Entity, target: Holder):
    entity.remove_parent()
    entity.put_into(target)


def move(entity: Entity, direction: Compass.Direction):
    target = entity.get_parent().get_neighbor(direction)
    place(entity, target)


def push(entity: Entity, direction: Compass.Direction) -> bool:
    neighbor: Holder = entity.get_parent().get_neighbor(direction)
    #  If the neighbor is empty we can move to it
    if neighbor.is_empty():
        move(entity, direction)
        return True

    pushee: Entity = neighbor.get_child()

    #  Checks if there is an arrow facing the wrong way, which blocks our movement
    if isinstance(pushee, Arrow) and pushee.direction is ~direction:
        return False

    #  If the pushee is pushable and can successfully be pushed we can move to it
    if pushee.pushable and push(pushee, direction):
        move(entity, direction)
        return True
    return False
