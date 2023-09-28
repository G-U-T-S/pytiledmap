import time

import pygame

from scripts import classes as clss
from scripts import pygame_debuger as pg_dbg


class Editor:
    def __init__(
        self,
        screen_size=(1024, 640),
        map_size=(480,640),
        tile_size=(32,32),
        draw_region_color=(0,0,0),
        bg_color=(145, 169, 179),
        grid_color=(255,255,255),
        tab_color=(74, 87, 94)
    ):

        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption('Tilemap Editor')
        icon = pygame.image.load('images/icon.png').convert_alpha()
        pygame.display.set_icon(icon)
        self.font = pygame.font.SysFont('arial', 15)
        self.running = True

        self.screen_surface_width = screen_size[0]
        self.screen_surface_height = screen_size[1]

        self.draw_region_color = draw_region_color
        self.bg_color = bg_color
        self.grid_color = grid_color

        self.map_size = map_size
        self.tile_size = tile_size

        self.start_screen()

        self.grid_list = self.create_grid()
        self.surface_list = self.create_surfaces()
        self.tiles_list = self.load_tileset()
        self.buttons = self.create_buttons()

        self.eraser_surf = clss.GenericSurf(
            pos=(0,0),
            size=(self.tile_size[0], self.tile_size[1]),
            color=self.draw_region_color
        )
        self.top_tab = clss.GenericSurf(
            pos=(0, 0),
            size=(self.screen_surface_width, 32),
            color=tab_color
        )
        self.lateral_tab = clss.GenericSurf(
            pos=(self.screen_surface_width-(3*32), 0),
            size=(3*32,self.screen_surface_height),
            color=tab_color
        )

        self.tileset_index = 0
        self.direction = pygame.math.Vector2()
        self.clock = pygame.time.Clock()

        self.active_grid = True
        self.holding_pencil = False
        self.holding_eraser = False
        self.active_popup = False

        self.popup_list = {
            'pop_file_error': clss.Popup.Alert(
                pos=(self.screen_surface_width//2, self.screen_surface_height//2-30),
                text='Oops! Arquivo não encontrado.'
            ),
            'pop_save': clss.Popup.YesNo(text='Salvar?'),
            'pop_trash': clss.Popup.YesNo(text='Reiniciar Desenho?'),
            'pop_file': clss.Popup.TextInput(text='Digite o caminho do arquivo:')
        }


    def load_tileset(self, file_path='images/tile_set.png'):
        tileset = pygame.image.load(file_path).convert_alpha()
        width = tileset.get_width()
        height = tileset.get_height()
        temp_list = []
        x = y = index = 0
        h = 1
        for _ in range((width//self.tile_size[0])*(height//self.tile_size[1])):
            try:
                img = tileset.subsurface(
                    (x*self.tile_size[0], y*self.tile_size[1],
                     self.tile_size[0], self.tile_size[1])).convert_alpha()
                img = pygame.transform.scale(img, (32,32))

                temp_list.append(
                    [img,
                     pygame.Rect(
                         self.screen_surface_width-(2*32),
                         h*32, 32, 32),
                     index
                    ])
                index += 1
                x += 1
                h += 1.3
            except Exception:
                x += 1

            if x % (width//self.tile_size[0]) == 0 and x != 0:
                y += 1
                x = 0

        return temp_list


    def create_buttons(self):
        temp_dict = {}
        buttons = ['btn_save', 'btn_file', 'btn_trash', 'btn_dropper', 'btn_config']
        sheet = pygame.image.load('images/buttons.png').convert_alpha()
        h = 0
        for x in range(5):
            img = sheet.subsurface(x*32, 0, 32, 32)
            temp_dict[f'{buttons[x]}'] = clss.Button(
                                img=img,
                                pos=(h*32,0)
                            )
            h += 1.5

        return temp_dict


    def create_surfaces(self):
        temp_list = []
        for y in range(round(self.map_size[1]/self.tile_size[1])):
            for x in range(round(self.map_size[0]/self.tile_size[0])):
                temp_list.append(
                    [(x, y),
                     clss.GenericSurf(
                         pos=(x*self.tile_size[0], y*self.tile_size[1]),
                         size=(self.tile_size[0], self.tile_size[1]),
                         color=self.draw_region_color),
                     -1
                    ]
                )

        return temp_list


    def create_grid(self):
        temp_list = []
        for x in range(round(self.screen_surface_width/self.tile_size[0])):
            temp_list.append(pygame.draw.line(
                    self.screen, self.grid_color,
                    (x*self.tile_size[0], 0),
                    (x*self.tile_size[0],self.screen_surface_height)
                )
            )

        for y in range(round(self.screen_surface_height/self.tile_size[1])):
             temp_list.append(pygame.draw.line(
                    self.screen, self.grid_color,
                    (0, y*self.tile_size[1]),
                    (self.screen_surface_width, y*self.tile_size[1])
                )
            )

        return temp_list


    def show_grid(self):
        for x in range(len(self.grid_list)):
            pygame.draw.rect(self.screen, self.grid_color, self.grid_list[x])


    def move_surfaces(self, direction):
        if direction.x > 0\
        and self.surface_list[1][1].rect.x < self.screen_surface_width:
            for x in range(len(self.surface_list)):
                self.surface_list[x][1].rect.x += self.tile_size[0]

        elif direction.x < 0\
        and self.surface_list[-1][1].rect.x > 0:
            for x in range(len(self.surface_list)):
                self.surface_list[x][1].rect.x -= self.tile_size[0]

        if direction.y > 0\
        and self.surface_list[-1][1].rect.y > 0:
            for x in range(len(self.surface_list)):
                self.surface_list[x][1].rect.y -= self.tile_size[1]

        elif direction.y < 0\
        and self.surface_list[1][1].rect.y < self.screen_surface_height:
            for x in range(len(self.surface_list)):
                self.surface_list[x][1].rect.y += self.tile_size[1]


    def draw_menus(self):
        self.screen.blit(self.lateral_tab.image, self.lateral_tab.rect)
        y = 0
        for tile in self.tiles_list:
            self.screen.blit(
                tile[0],
                tile[1]
            )
            y += 1.3
        self.screen.blit(self.top_tab.image, self.top_tab.rect)
        for btn in self.buttons:
            self.screen.blit(self.buttons[btn].image, self.buttons[btn].rect)


    def save(self, dir='levels.txt'):
        with open(dir, 'w+') as arq:
            arq.write('level=[')
            x = 0
            for tile in editor.surface_list:
                if x >= editor.map_size[0]//editor.tile_size[0]:
                    arq.write('\n')
                    x = 0
                arq.write(f'{str(tile[2])},')
                x += 1
            arq.write(']')


    def start_screen(self):
        self.screen.fill(self.bg_color)

        title_font = pygame.font.SysFont('arial', 40)
        title = title_font.render('TILEMAP EDITOR', True, 'white')
        self.screen.blit(
            title,
            (self.screen_surface_width//2-title.get_width()//2, 80)
        )

        btn_next = clss.custom_button(
            size=(300, 50),
            color='blue',
            pos=(self.screen_surface_width//2-150,
                 self.screen_surface_height//2 + 150),
            text='Prosseguir',
            text_color='white'
        )
        self.screen.blit(
            btn_next['surf'],
            btn_next['rect']
        )

        pygame.display.flip()
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    wait = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_next['rect'].collidepoint(event.pos):
                        wait = False
                    else:
                        pass


    def main_loop(self):
        choice = False
        while self.running:
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        if self.active_grid:
                            self.active_grid = False
                        else:
                            self.active_grid = True

                    elif event.key == pygame.K_e:
                        pos = pygame.mouse.get_pos()
                        for x in range(len(self.surface_list)):
                            if self.surface_list[x][1].rect.collidepoint(pos):
                                self.tileset_index = self.surface_list[x][2]

                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_w:
                        self.direction.y = 1
                    elif event.key == pygame.K_s:
                        self.direction.y = -1
                    if event.key == pygame.K_a:
                        self.direction.x = -1
                    elif event.key == pygame.K_d:
                        self.direction.x = 1

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        self.direction.y = 0
                    if event.key == pygame.K_a or event.key == pygame.K_d:
                        self.direction.x = 0

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 5 and self.tiles_list[0][1].y < 0:
                        for index, _ in enumerate(self.tiles_list):
                            self.tiles_list[index][1].y += 64

                    elif event.button == 4\
                    and self.tiles_list[-1][1].bottom > self.screen_surface_height:
                        for index, _ in enumerate(self.tiles_list):
                                self.tiles_list[index][1].y -= 64

                    elif event.button == 1:
                        pos = pygame.mouse.get_pos()

                        tile = False
                        for x in range(len(self.tiles_list)):
                            if self.tiles_list[x][1].collidepoint(pos):
                                self.tileset_index = self.tiles_list[x][2]
                                tile = True
                                break

                        button = False
                        for btn in self.buttons:
                            if self.buttons[btn].rect.collidepoint(pos):
                                button = True

                                if btn == 'btn_save':
                                    self.running, choice = self.popup_list[
                                                            'pop_save'].spawn()
                                    if choice:
                                        self.save()

                                elif btn == 'btn_file':
                                    self.running, choice, file_path = self.popup_list[
                                                            'pop_file'].spawn()
                                    if choice:
                                        try:
                                            self.tiles_list = self.load_tileset(
                                                                        file_path)
                                        except Exception:
                                            self.popup_list['pop_file_error'].spawn()

                                elif btn == 'btn_trash':
                                    self.running, choice = self.popup_list[
                                                            'pop_trash'].spawn()
                                    if choice:
                                        for surf in self.surface_list:
                                            surf[1].image = self.eraser_surf.image
                                            surf[2] = -1


                        #ensures that you do not draw on
                        #the surface by clicking on a tile
                        if not tile and not button:
                            pos = pygame.mouse.get_pos()
                            for x in range(len(self.surface_list)):
                                if self.surface_list[x][1].rect.collidepoint(pos):
                                    self.surface_list[x][1].image = self.tiles_list[
                                                                    self.tileset_index][0]
                                    self.surface_list[x][2] = self.tileset_index
                                    self.holding_pencil = True
                                    break


                    elif event.button == 3:
                        pos = pygame.mouse.get_pos()
                        for x in range(len(self.surface_list)):
                            if self.surface_list[x][1].rect.collidepoint(pos):
                                self.surface_list[x][1].image = self.eraser_surf.image
                                self.surface_list[x][2] = 0
                                self.holding_eraser = True
                                break

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.holding_pencil = False
                    elif event.button == 3:
                        self.holding_eraser = False


            self.screen.fill(self.bg_color)

            self.move_surfaces(self.direction)

            for x in range(len(self.surface_list)):
                self.screen.blit(self.surface_list[x][1].image,
                                 self.surface_list[x][1].rect)

            if self.holding_pencil:
                pos = pygame.mouse.get_pos()
                for x in range(len(self.surface_list)):
                    if self.surface_list[x][1].rect.collidepoint(pos):
                        self.surface_list[x][1].image = self.tiles_list[
                                                                self.tileset_index][0]
                        self.surface_list[x][2] = self.tileset_index
            elif self.holding_eraser:
                pos = pygame.mouse.get_pos()
                for x in range(len(self.surface_list)):
                    if self.surface_list[x][1].rect.collidepoint(pos):
                        self.surface_list[x][1].image = self.eraser_surf.image
                        self.surface_list[x][2] = 0

            if self.active_grid:
                self.show_grid()

            # debuger.debug_text(choice, pos=(10,50))

            self.draw_menus()

            pygame.display.flip()


if __name__ == '__main__':
    editor = Editor()
    #-------Temporaly--------#
    debuger = pg_dbg.Debuger()
    #------------------------#
    editor.main_loop()

    pygame.quit()
