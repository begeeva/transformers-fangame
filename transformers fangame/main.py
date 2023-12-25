import pygame
import sys
import os


SIZE = WIDTH, HEIGHT = 768, 384

pygame.init()
screen = pygame.display.set_mode(SIZE)
running = True

fps = 30
clock = pygame.time.Clock()


def load_image(dir, name, colorkey=None):
    fullname = os.path.join(f'images/{dir}', name)

    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


class StartBtn(pygame.sprite.Sprite):
    not_pressed = load_image('sprites', 'start btn.png')
    pressed = load_image('sprites', 'start btn pressed.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = StartBtn.not_pressed
        self.rect = self.not_pressed.get_rect()
        self.rect.x = 140
        self.rect.y = 250

        self.is_pressed = False

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image = self.pressed
            self.is_pressed = True


def main_menu():
    all_sprites = pygame.sprite.Group()

    st_btn_sprite = pygame.sprite.GroupSingle()
    start_btn = StartBtn(st_btn_sprite)
    all_sprites.add(st_btn_sprite)

    game_title = pygame.sprite.Sprite()
    game_title.image = load_image('sprites', 'title.png')
    game_title.rect = game_title.image.get_rect()
    game_title.rect.x = 40
    game_title.rect.y = 100
    all_sprites.add(game_title)

    bg = load_image('backgrounds', 'main menu bg.png')
    screen.blit(bg, (0, 0))
    st_btn_pressed_time = 0

    pygame.mixer.music.load('sounds/The Transformers (Theme) (128kbps).mp3')
    pygame.mixer.music.play(-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_btn.rect.collidepoint(event.pos):
                    start_btn.update(event)
                    st_btn_pressed_time = pygame.time.get_ticks()
        all_sprites.draw(screen)
        if start_btn.is_pressed and 300 < pygame.time.get_ticks() - st_btn_pressed_time < 400:
            pygame.mixer.music.stop()
            return
        clock.tick(fps)
        pygame.display.flip()


def main_game():
    pygame.mixer.music.load('sounds/Transformers Cybertron - Theme Song (Extended).mp3')
    pygame.mixer.music.play(-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.fill((0, 0, 0))
        clock.tick(fps)
        pygame.display.flip()


main_menu()
main_game()
pygame.quit()
