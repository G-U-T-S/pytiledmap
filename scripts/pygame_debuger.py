import pygame


class Debuger:
    def __init__(self, font_size=20):
        self.font = pygame.font.SysFont('arial', font_size)

        self.surface = pygame.display.get_surface()
        self.surface_width = self.surface.get_width()
        self.surface_height = self.surface.get_height()


    def debug_text(
        self, info='No Text', pos=(10,10),
        text_color=(0,0,0), bg_color=(255,255,255)
    ):
        debug_text = self.font.render(f'{info}', True, text_color, bg_color)
        self.surface.blit(debug_text, pos)


    def show_grid(self, tile_size=32, grid_color=(255,255,255)):
        for x in range(round(self.surface_width/tile_size)):
            pygame.draw.line(
                self.surface, grid_color,
                (x*tile_size, 0), (x*tile_size, self.surface_height)
            )

        for y in range(round(self.surface_height/tile_size)):
            pygame.draw.line(
                self.surface, grid_color,
                (0, y*tile_size), (self.surface_width, y*tile_size)
            )


    def show_collision_box(self, rect, rect_color=(255, 0, 0)):
        pygame.draw.rect(self.surface, rect_color, rect, 2)

