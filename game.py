from typing import List

from objects import Actor, Trashcan, Arrow, Holder, Compass, Wall, Rock, Core
from util.actions import push
from util.level_creation import make_grid, range_grid


def index_sort(actor: Actor):
    return actor.get_index()


class Game:
    def __init__(self, size: int):
        self.size = size
        self.set_empty_grid()
        self.actors: List[Actor] = []
        self.step_index = 0
        self.current_level = "level1"

    def set_empty_grid(self):
        self.actors = []
        self.step_index = 0
        self.grid = make_grid(self.size + 2, self.size + 2)
        self.holders: List[Holder] = [[None for j in range(self.size)] for i in range(self.size)]
        for coords, holder in range_grid(self.grid, ignore_border=True):
            self.holders[coords.x][coords.y] = holder

    def load_grid_from_file(self, filename):
        self.current_level = filename
        level = open("levels/" + filename)
        self.size = int(level.readline().strip())
        self.set_empty_grid()
        for entry in level:
            tokens = entry.strip().split(" ")
            if tokens[0] == '':
                continue
            x = int(tokens[0])
            y = int(tokens[1])
            holder: Holder = self.get_holder(x, y)
            entity = None
            #  <x> <y> arrow <up|down|left|right> <index>
            if tokens[2] == "arrow":
                entity = Arrow(Compass.from_str(tokens[3]), int(tokens[4]))
                self.actors.append(entity)
            if tokens[2] == "wall":
                entity = Wall()
            if tokens[2] == "rock":
                entity = Rock()
            if tokens[2] == "core":
                entity = Core()

            if entity is not None:
                entity.put_into(holder)

    def reload_current(self):
        self.load_grid_from_file(self.current_level)

    def get_holder(self, x, y):
        try:
            return self.holders[x][y]
        except IndexError:
            return None

    def get_grid(self):
        return self.grid

    def step(self):
        self.garbage_collect()
        self.reindex()
        #  Make sure there are actors
        if len(self.actors) == 0:
            return
        #  Execute respective actions
        if self.step_index >= len(self.actors):
            self.step_index = 0
        actor: Actor = self.actors[self.step_index]
        if isinstance(actor, Arrow):
            push(actor, actor.direction)
        self.step_index += 1

    def reindex(self):
        self.actors.sort(key=index_sort)
        for i, actor in enumerate(self.actors):
            actor.set_index(i)

    def garbage_collect(self):
        #  removes all actors in trashcans or without a parent
        self.actors[:] = \
            [actor for actor in self.actors if actor.has_parent() and not isinstance(actor.parent, Trashcan)]

