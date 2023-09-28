import pygame


class GenericSurf(pygame.sprite.Sprite):
    def __init__(self, pos, img=False, size=(32,32), color=(0,0,0)):
        super().__init__()
        if img:
            self.image = pygame.image.load(img)
        else:
            self.image = pygame.Surface(size)
            self.image.fill(color)

        self.rect = self.image.get_rect(topleft=pos)


class Button(pygame.sprite.Sprite):
    def __init__(self, img, pos):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect(topleft=pos)


def custom_button(size, pos, color, text, text_color):
    font = pygame.font.SysFont('arial', 15)
    button_dict = {
        'surf': pygame.Surface(size),
        'rect': pygame.Rect(pos, size),
        'text': font.render(text, True, text_color)
    }
    button_dict['surf'].fill(color)
    button_dict['surf'].blit(
        button_dict['text'],
        ((button_dict['surf'].get_width()//2-button_dict['text'].get_width()//2),
          button_dict['surf'].get_height()//2-button_dict['text'].get_height()//2)
    )
    return button_dict


class Popup:
    class Alert:
        def __init__(
            self, pos=(0,0), size=(300, 100), text='', font_size=15,
            text_color='black', label_offset=(0, 0),
            bg_color=(194, 194, 194)
        ):
            self.screen = pygame.display.get_surface()

            self.surface = {
                'surf': pygame.Surface(size),
                'rect': pygame.Rect(pos, size)
            }
            self.surface['surf'].fill(bg_color)
            self.surface['rect'].center = pos

            self.font = pygame.font.SysFont('arial', font_size)
            self.label = self.font.render(text, True, text_color)
            self.surface['surf'].blit(
                self.label,
                ((self.surface['surf'].get_width()//2-self.label.get_width()//2)+label_offset[0],
                 (self.surface['surf'].get_height()//2-self.label.get_height()//2)+label_offset[1])
            )


        def spawn(self):
            self.screen.blit(self.surface['surf'], self.surface['rect'])
            pygame.draw.rect(
                self.screen,
                'blue',
                self.surface['rect'],
                4
            )
            pygame.display.flip()
            wait = True
            while wait:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN\
                    or event.type == pygame.KEYDOWN:
                        wait = False


    class YesNo:
        def __init__(
        self, size=(230,100),
        button_yes_size=(80,30), button_yes_color=(0,0,255), button_yes_offset=(20,-50),
        button_no_size=(80,30), button_no_color=(0,0,255), button_no_offset=(-105,-50),
        text='', font_size=15, text_color='black', button_text_color='white',
        label_offset=(0,-25), bg_color=(194, 194, 194)
        ):
            self.screen = pygame.display.get_surface()

            self.surface = {
                'surf': pygame.Surface(size),
                'width': size[0],
                'height': size[1],
                'rect': pygame.Rect(
                    (self.screen.get_width()//2,
                     self.screen.get_height()//2),
                    (size))
            }
            self.surface['surf'].fill(bg_color)
            self.surface['rect'].centerx = self.screen.get_width()//2
            self.surface['rect'].centery = self.screen.get_height()//2

            self.button_yes = custom_button(
                size=button_yes_size,
                pos=(self.screen.get_width()//2 -95,self.screen.get_height()//2),
                color=button_yes_color,
                text='SIM',
                text_color=button_text_color
            )
            self.surface['surf'].blit(
                self.button_yes['surf'],
                (button_yes_offset[0],
                 self.surface['height']+button_yes_offset[1])
            )
            self.button_no = custom_button(
                size=button_no_size,
                pos=(self.screen.get_width()//2 +10,self.screen.get_height()//2),
                color=button_no_color,
                text='NÃO',
                text_color=button_text_color
            )
            self.surface['surf'].blit(
                self.button_no['surf'],
                (self.surface['width']+button_no_offset[0],
                 self.surface['height']+button_no_offset[1])
            )

            self.font = pygame.font.SysFont('arial', font_size)
            label = self.font.render(text, True, text_color)
            label_centerx = label.get_width()//2
            label_centery = label.get_height()//2
            self.surface['surf'].blit(
                label,
                ((self.surface['width']//2-label_centerx)+label_offset[0],
                 (self.surface['height']//2-label_centery)+label_offset[1])
            )

            self.clock = pygame.time.Clock()


        def spawn(self):
            self.screen.blit(self.surface['surf'], self.surface['rect'])
            pygame.display.flip()
            wait = running = True
            choice = False
            while wait:
                self.clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        wait = False

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()

                        if not self.surface['rect'].collidepoint(pos):
                            wait = False

                        if self.button_yes['rect'].collidepoint(pos):
                            running = True
                            choice = True
                            wait = False

                        elif self.button_no['rect'].collidepoint(pos):
                            running = True
                            choice = False
                            wait = False


            return (running, choice)


    class TextInput:
        def __init__(self, size=(400,200),
        button_confirm_size=(80,30), button_confirm_color=(0,0,255),
        button_confirm_offset=(20,-50),button_cancel_size=(80,30),
        button_cancel_color=(0,0,255), button_cancel_offset=(-105,-50),
        text='', font_size=15, text_color='black', label_offset=(0,-70),
        bg_color=(194, 194, 194)
        ):

            self.screen = pygame.display.get_surface()
            self.surface = {
                'surf': pygame.Surface(size),
                'width': size[0],
                'height': size[1],
                'rect': pygame.Rect((self.screen.get_width()//2,
                                     self.screen.get_height()//2),
                                     (size))
            }
            self.surface['surf'].fill(bg_color)
            self.surface['rect'].centerx = self.screen.get_width()//2
            self.surface['rect'].centery = self.screen.get_height()//2
            self.font = pygame.font.SysFont('arial', font_size)

            self.button_confirm = custom_button(
                size=button_confirm_size,
                pos=(self.screen.get_width()//2 -180,self.screen.get_height()//2 +50),
                color=button_confirm_color,
                text ='Confirmar',
                text_color='white'
            )
            self.button_confirm['offset'] = button_confirm_offset

            self.button_cancel = custom_button(
                size=button_cancel_size,
                pos=(self.screen.get_width()//2 +90,self.screen.get_height()//2 +50),
                color=button_cancel_color,
                text ='Cancelar',
                text_color='white'
            )
            self.button_cancel['offset'] = button_cancel_offset

            self.label = self.font.render(text, True, text_color)
            self.label_offset = label_offset
            self.label_centerx = self.label.get_width()//2
            self.label_centery = self.label.get_height()//2
            self.surface['surf'].blit(
                self.label,
                ((self.surface['width']//2-self.label_centerx)+self.label_offset[0],
                 (self.surface['height']//2-self.label_centery)+self.label_offset[1])
            )

            self.clock = pygame.time.Clock()


        def spawn(self):
            file_path = ''
            base_font = pygame.font.Font(None, 32)
            user_text = ''

            input_surface = pygame.Surface((300,32))
            input_surface.fill((28, 107, 232))
            input_rect = pygame.Rect(
                (self.screen.get_width()//2-150,self.screen.get_height()//2-20, 300,32)
            )

            wait = running = True
            choice = active = False
            while wait:
                self.clock.tick(60)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        wait = False

                    elif event.type == pygame.KEYDOWN and active:
                        if event.key == pygame.K_BACKSPACE:
                            user_text = user_text[:-1]
                        elif event.key == 13:
                            choice = True
                            wait = False
                        else:
                            user_text += event.unicode

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        active = bool(input_rect.collidepoint(event.pos))
                        if active:
                            input_surface.fill((66, 132, 237))
                        else:
                            input_surface.fill((28, 107, 232))

                        if not self.surface['rect'].collidepoint(event.pos):
                            running = True
                            wait = False

                        if self.button_confirm['rect'].collidepoint(event.pos):
                            running = True
                            choice = True
                            wait = False

                        elif self.button_cancel['rect'].collidepoint(event.pos):
                            running = True
                            choice = False
                            wait = False

                self.surface['surf'].fill((194, 194, 194))
                self.surface['surf'].blit(
                    input_surface,
                    ((self.surface['width']//2-155,self.surface['height']//2-20),(300,32))
                )
                text_surface = base_font.render(user_text, True, (255, 255, 255))
                self.surface['surf'].blit(
                    text_surface,
                    (50, self.surface['height']//2-15)
                )
                self.surface['surf'].blit(
                    self.label,
                    ((self.surface['width']//2-self.label_centerx)+self.label_offset[0],
                     (self.surface['height']//2-self.label_centery)+self.label_offset[1])
                )
                self.surface['surf'].blit(
                    self.button_confirm['surf'],
                    (self.button_confirm['offset'][0],
                     self.surface['height']+self.button_confirm['offset'][1])
                )
                self.surface['surf'].blit(
                    self.button_cancel['surf'],
                    (self.surface['width']+self.button_cancel['offset'][0],
                     self.surface['height']+self.button_cancel['offset'][1])
                )
                self.screen.blit(self.surface['surf'], self.surface['rect'])

                # SISTEMA QUE FAZ A FRASE IR PARA A ESQUERDA QUANDO CHEGAR NO FINAL

                pygame.display.flip()

            file_path = str(user_text)
            return (running, choice, file_path)

