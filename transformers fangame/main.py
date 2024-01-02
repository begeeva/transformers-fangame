import pygame
import sys
from random import randrange


SIZE = WIDTH, HEIGHT = 768, 384

pygame.init()
screen = pygame.display.set_mode(SIZE)
running = True

fps = 30
clock = pygame.time.Clock()


class Star(pygame.sprite.Sprite):
    image = pygame.image.load('images/other sprites/a star.png')

    def __init__(self, group):
        super().__init__(*group)
        self.image = Star.image
        self.rect = self.image.get_rect()
        self.rect.x = randrange(1, 768)
        self.rect.y = randrange(1, 384)
        self.vx = randrange(1, 5)
        self.vy = randrange(-5, 5)

    def update(self):
        self.rect = self.rect.move(self.vx, 0)
        self.destroy()

    def destroy(self):
        if self.rect.x > 768:
            self.kill()


class StartBtn(pygame.sprite.Sprite):
    not_pressed = pygame.image.load('images/other sprites/start btn.png').convert_alpha()
    pressed = pygame.image.load('images/other sprites/start btn pressed.png').convert_alpha()

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


class City(pygame.sprite.Sprite):
    image = pygame.image.load('images/other sprites/bg city.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = City.image
        self.rect = self.image.get_rect()
        self.rect.bottom = 294

    def update(self):
        self.rect.x -= 1
        self.destroy()

    def destroy(self):
        if self.rect.right < 0:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        cr0 = pygame.image.load('images/cliff sprites/cliff run00.png').convert_alpha()
        cr1 = pygame.image.load('images/cliff sprites/cliff run01.png').convert_alpha()
        cr2 = pygame.image.load('images/cliff sprites/cliff run02.png').convert_alpha()
        cr3 = pygame.image.load('images/cliff sprites/cliff run03.png').convert_alpha()
        cr4 = pygame.image.load('images/cliff sprites/cliff run04.png').convert_alpha()
        cr5 = pygame.image.load('images/cliff sprites/cliff run05.png').convert_alpha()
        cr6 = pygame.image.load('images/cliff sprites/cliff run06.png').convert_alpha()
        cr7 = pygame.image.load('images/cliff sprites/cliff run07.png').convert_alpha()
        cr8 = pygame.image.load('images/cliff sprites/cliff run08.png').convert_alpha()
        self.cliff_jump = pygame.image.load('images/cliff sprites/cliff jump.png').convert_alpha()
        self.cliff_run = [cr0, cr1, cr2, cr3, cr4, cr5, cr6, cr7, cr8]
        self.index = 0
        self.image = self.cliff_run[self.index]
        self.rect = self.image.get_rect()
        self.rect.left = 70
        self.rect.bottom = 294
        self.gravity = 0

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()

    def animation(self):
        self.index += 0.9
        if self.index >= len(self.cliff_run):
            self.index = 0
        if self.rect.bottom == 294:
            self.image = self.cliff_run[int(self.index)]
        elif self.rect.bottom < 294:
            self.image = self.cliff_jump

    def apply_gravity(self):
        self.gravity += 1
        self.rect.bottom += self.gravity
        if self.rect.bottom >= 294:
            self.rect.bottom = 294
            self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 294:
            self.gravity -= 18


def terminate():
    pygame.quit()
    sys.exit()


def main_menu():
    all_sprites = pygame.sprite.Group()

    star_sprites = pygame.sprite.Group()
    all_sprites.add(star_sprites)

    st_btn_sprite = pygame.sprite.GroupSingle()
    start_btn = StartBtn(st_btn_sprite)
    st_btn_pressed_time = 0

    game_title = pygame.image.load('images/other sprites/title.png').convert_alpha()
    game_title_rect = game_title.get_rect()
    game_title_rect.x = 40
    game_title_rect.y = 100

    bg = pygame.image.load('images/backgrounds/space.png')

    pygame.mixer.music.load('sounds/The Transformers (Theme) (128kbps).mp3')
    pygame.mixer.music.play(-1)

    n_stars = 500

    for i in range(n_stars):
        star = Star(star_sprites)
        all_sprites.add(star)

    cybertron = pygame.image.load('images/other sprites/Cybertron.png')
    cybertron_rect = cybertron.get_rect()
    cybertron_rect.bottom = HEIGHT
    cybertron_rect.right = WIDTH

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_btn.rect.collidepoint(event.pos):
                    start_btn.update(event)
                    st_btn_pressed_time = pygame.time.get_ticks()

        screen.blit(bg, (0, 0))

        if len(all_sprites.sprites()) < 502:
            star = Star(star_sprites)
            star.rect.x = 0
            all_sprites.add(star)

        all_sprites.draw(screen)
        all_sprites.update()

        screen.blit(cybertron, cybertron_rect)
        screen.blit(game_title, game_title_rect)
        screen.blit(start_btn.image, start_btn.rect)
        start_btn.update()

        if start_btn.is_pressed and 300 < pygame.time.get_ticks() - st_btn_pressed_time < 400:
            pygame.mixer.music.stop()
            return
        clock.tick(fps)
        pygame.display.flip()


def main_game():
    all_sprites = pygame.sprite.Group()

    bg = pygame.image.load('images/backgrounds/space.png')

    ground = pygame.image.load('images/other sprites/ground.png')
    ground_rect = ground.get_rect()
    ground_rect.bottom = HEIGHT

    bg_city = City(all_sprites)

    cliffjumper = pygame.sprite.GroupSingle()
    player = Player()
    cliffjumper.add(player)

    pygame.mixer.music.load('sounds/Transformers Cybertron - Theme Song (Extended).mp3')
    pygame.mixer.music.play(-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        screen.blit(bg, (0, 0))
        screen.blit(ground, ground_rect)

        if bg_city.rect.right == WIDTH:
            city = City(all_sprites)
            city.rect.left = WIDTH

        all_sprites.draw(screen)
        all_sprites.update()

        cliffjumper.draw(screen)
        cliffjumper.update()

        pygame.display.flip()
        clock.tick(18)


main_menu()
main_game()
pygame.quit()
