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
    image = pygame.image.load('images/sprites/a star.png')

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
    not_pressed = pygame.image.load('images/sprites/start btn.png').convert_alpha()
    pressed = pygame.image.load('images/sprites/start btn pressed.png').convert_alpha()

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

    game_title = pygame.image.load('images/sprites/title.png').convert_alpha()
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

    cybertron = pygame.image.load('images/sprites/Cybertron.png')
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
    bg = pygame.image.load('images/backgrounds/space.png')

    ground = pygame.image.load('images/sprites/ground.png')
    ground_rect = ground.get_rect()
    ground_rect.bottom = HEIGHT

    bg_city = pygame.image.load('images/sprites/bg city.png')
    bg_city_rect = bg_city.get_rect()
    bg_city_rect.bottom = 294

    cliff = pygame.Surface((66, 96))
    cliff.fill('red')
    cliff_rect = cliff.get_rect()
    cliff_rect.left = 50
    cliff_rect.bottom = 294

    pygame.mixer.music.load('sounds/Transformers Cybertron - Theme Song (Extended).mp3')
    pygame.mixer.music.play(-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        screen.blit(bg, (0, 0))
        screen.blit(ground, ground_rect)
        screen.blit(bg_city, bg_city_rect)
        screen.blit(cliff, cliff_rect)

        clock.tick(fps)
        pygame.display.flip()


main_menu()
main_game()
pygame.quit()
