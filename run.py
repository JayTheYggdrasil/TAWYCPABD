from types import SimpleNamespace

import pygame

from game import Game
from objects import Holder, Entity, Arrow, Actor, Wall, Rock, Core
from util.level_creation import range_grid
from util.shapes import Shapes


class DisplayManager:
    def __init__(self, game, cell_size: int = 40):
        pygame.init()
        self.game: Game = game
        self.window: pygame.Surface = pygame.display.set_mode(size=(game.size * cell_size, game.size * cell_size))
        pygame.display.set_caption("TAWYCPA but different")
        self.cell_size = cell_size
        self.game_coords = (0, 0)
        self.focused: Holder = None

    def update_focused(self):
        if pygame.mouse.get_focused():
            pos = pygame.mouse.get_pos()
            relative_pos = (pos[0]-self.game_coords[0], pos[1]-self.game_coords[1])
            x = relative_pos[0] // self.cell_size
            y = relative_pos[1] // self.cell_size
            self.focused = self.game.get_holder(x, y)
        else:
            self.focused = None

    def run(self):
        clock = 0
        running = True
        paused = True
        while running:
            pygame.time.delay(33)

            clock += 1
            if clock % 10 == 0 and not paused:
                self.game.step()

            self.update_focused()
            self.window.fill((0, 0, 0))
            self.window.blit(self.create_display_grid(self.game.get_grid()), self.game_coords)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.focused is not None:
                        self.focused.toggle_active()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                    if event.key == pygame.K_q:
                        self.game.reload_current()
                        paused = True
            pygame.display.update()

    def create_display_grid(self, top_left: Holder):
        surface = pygame.Surface((self.game.size * self.cell_size, self.game.size * self.cell_size))
        for coords, holder in range_grid(top_left, ignore_border=True):
            surface.blit(self.create_surface_from_holder(holder, self.cell_size),
                         (coords.x * self.cell_size, coords.y * self.cell_size))

        return surface

    def create_surface_from_holder(self, holder: Holder, cell_size: int):
        surface = pygame.Surface((cell_size, cell_size))
        surface.fill((0, 0, 0))
        border_width = 2
        inner_surface = pygame.Surface((cell_size - 2*border_width, cell_size - 2*border_width))

        if holder is self.focused:
            inner_surface.fill((0, 200, 0))
        elif holder.is_active():
            inner_surface.fill((50, 50, 50))
        else:
            inner_surface.fill((200, 0, 0))

        surface.blit(inner_surface, (border_width, border_width))

        #  Check if we need to draw an entity too
        if holder.has_child():
            entity: Entity = holder.get_child()

            #  Draw the Wall Object
            if isinstance(entity, Wall):
                pygame.draw.rect(surface, (200, 200, 200),
                                 (border_width, border_width, cell_size - 2*border_width, cell_size - 2*border_width),
                                 border_width*2)

            if isinstance(entity, Rock):
                pygame.draw.rect(surface, (175, 150, 50),
                                 (border_width, border_width, cell_size - 2*border_width, cell_size - 2*border_width),
                                 border_width*2)

            if isinstance(entity, Core):
                pygame.draw.rect(surface, (0, 220, 255),
                                 (border_width, border_width, cell_size - 2*border_width, cell_size - 2*border_width),
                                 border_width*2)

            #  Draw the Arrow object
            if isinstance(entity, Arrow):
                points = Shapes.ARROW.get_points(scale=cell_size, direction=entity.direction)
                pygame.draw.polygon(surface, (0, 200, 255), points)

            #  Draw an Actors index
            if isinstance(entity, Actor):
                font = pygame.font.Font(None, int(cell_size / 1.5))
                text = font.render(str(entity.get_index()), True, (255, 255, 255))
                surface.blit(text,
                             (cell_size//2 - text.get_width()//2, cell_size//2 - text.get_height()//2))
        return surface


if __name__ == '__main__':
    game = Game(25)
    game.load_grid_from_file("rolling_stones_copy")
    display = DisplayManager(game, 30)
    display.run()
