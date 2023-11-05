import pygame

pygame.init()

font = pygame.font.SysFont('arial', 20)


class Terminal:
    def show_debug_text(self, info='no text'):
        print(f'{info}')


class Output:
    def show_debug_text(
            self, surface_to_blit, info='No Text', x=10, y=10,
            text_color=(0,0,0), bg_color=(255,255,255)
        ):
            debug_text = font.render(f'{info}', True, text_color, bg_color)
            surface_to_blit.blit(debug_text, (x, y))


    def show_debug_grid(
            self, surface_to_blit, surface_width, surface_height,
            tile_size=32, grid_color=(255,255,255)
        ):
            for x in range(round(surface_width/tile_size)):
                pygame.draw.line(
                    surface_to_blit, grid_color,
                    (x*tile_size, 0), (x*tile_size, surface_height)
                )

            for y in range(round(surface_height/tile_size)):
                pygame.draw.line(
                    surface_to_blit, grid_color,
                    (0, y*tile_size), (surface_width, y*tile_size)
                )


    def show_collision_box(self, surface_to_blit, rect, rect_color=(255, 0, 0)):
            pygame.draw.rect(surface_to_blit, rect_color, rect, 2)


terminal = Terminal()
output = Output()
