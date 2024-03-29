import pygame
import sys
from random import randrange, choice

SIZE = WIDTH, HEIGHT = 768, 384

player_score = 0
best_score = 0

pygame.init()
screen = pygame.display.set_mode(SIZE)
icon = pygame.image.load("data/autobots insignia.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Transformers")

FPS = 30
clock = pygame.time.Clock()


# класс звёздочек в главном меню
class Star(pygame.sprite.Sprite):
    image = pygame.image.load('data/other sprites/a star.png')

    def __init__(self, group):
        super().__init__(*group)
        self.image = Star.image
        self.rect = self.image.get_rect()
        self.rect.x = randrange(1, 768)
        self.rect.y = randrange(1, 384)
        self.vx = randrange(1, 4)

    def update(self):
        self.rect = self.rect.move(self.vx, 0)
        self.destroy()

    def destroy(self):
        if self.rect.x > 768:
            self.kill()


# класс кнопки "start" в главном меню
class StartBtn(pygame.sprite.Sprite):
    not_pressed = pygame.image.load('data/other sprites/start btn.png').convert_alpha()
    pressed = pygame.image.load('data/other sprites/start btn pressed.png').convert_alpha()

    def __init__(self):
        super().__init__()
        self.image = StartBtn.not_pressed
        self.rect = self.not_pressed.get_rect()
        self.rect.x = 140
        self.rect.y = 250

        self.is_pressed = False

    def update(self, *args):
        # проверка на нажатие
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image = self.pressed
            self.is_pressed = True


# класс города на заднем фоне в самом уровне
class City(pygame.sprite.Sprite):
    image = pygame.image.load('data/other sprites/bg city.png')

    def __init__(self, group, speed):
        super().__init__(group)
        self.image = City.image
        self.rect = self.image.get_rect()
        self.rect.bottom = 294
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        self.destroy()

    def destroy(self):
        if self.rect.right < 0:
            self.kill()


# класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.cliff_alt_mode = pygame.image.load('data/cliff sprites/cliff alt mode.png').convert_alpha()
        self.alt_mode_on = False
        self.cliff_jump = pygame.image.load('data/cliff sprites/cliff jump.png').convert_alpha()

        # дальше импортирую кадры анимации
        cr0 = pygame.image.load('data/cliff sprites/cliff run00.png').convert_alpha()
        cr1 = pygame.image.load('data/cliff sprites/cliff run01.png').convert_alpha()
        cr2 = pygame.image.load('data/cliff sprites/cliff run02.png').convert_alpha()
        cr3 = pygame.image.load('data/cliff sprites/cliff run03.png').convert_alpha()
        cr4 = pygame.image.load('data/cliff sprites/cliff run04.png').convert_alpha()
        cr5 = pygame.image.load('data/cliff sprites/cliff run05.png').convert_alpha()
        cr6 = pygame.image.load('data/cliff sprites/cliff run06.png').convert_alpha()
        cr7 = pygame.image.load('data/cliff sprites/cliff run07.png').convert_alpha()
        cr8 = pygame.image.load('data/cliff sprites/cliff run08.png').convert_alpha()

        # добавляю их в один список
        self.cliff_run = [cr0, cr1, cr2, cr3, cr4, cr5, cr6, cr7, cr8]

        self.index = 0  # число, указывающее номер кадра на данный момент
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
        self.index += 0.6
        if self.index > len(self.cliff_run):
            self.index = 0
        if self.rect.bottom == 294:
            if self.alt_mode_on:
                self.image = self.cliff_alt_mode
                self.rect.top = 240
            else:
                self.image = self.cliff_run[int(self.index)]
                self.rect.bottom = 294
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


# класс потолка тоннеля
class TunnelCeiling(pygame.sprite.Sprite):
    image = pygame.image.load('data/other sprites/tunnel ceiling.png')

    def __init__(self, x, speed):
        super().__init__()
        self.image = TunnelCeiling.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        self.destroy()

    def destroy(self):
        if self.rect.right < -100:
            self.kill()


# класс стенки тоннеля
class TunnelWall(pygame.sprite.Sprite):
    image = pygame.image.load('data/other sprites/tunnel wall.png')

    def __init__(self, speed):
        super().__init__()
        self.image = TunnelWall.image
        self.rect = self.image.get_rect()
        self.rect.x = randrange(WIDTH + 10, WIDTH + 600)
        self.speed = speed

    def update(self):
        self.rect.left -= self.speed
        self.destroy()

    def destroy(self):
        if self.rect.right < -100:
            self.kill()


# класс врага
class Enemy(pygame.sprite.Sprite):
    image = pygame.image.load('data/other sprites/vehicon steve.png').convert_alpha()

    def __init__(self, speed):
        super().__init__()
        self.image = Enemy.image
        self.rect = self.image.get_rect()
        self.rect.bottom = 294
        self.rect.left = randrange(WIDTH + 100, WIDTH + 700)
        self.speed = speed

    def update(self):
        self.rect.left -= self.speed
        self.destroy()

    def destroy(self):
        if self.rect.right < -100:
            self.kill()


# функция для проверки на столкновения
def collision(sprite, group):
    if pygame.sprite.spritecollide(sprite, group, False):
        return True


# функция для сохранения очков игрока
def save_scores(score):
    global player_score, best_score
    player_score = score

    with open('scores.txt', 'a', encoding='utf-8') as fw:
        fw.write(f"{score}\n")

    with open('scores.txt', 'r', encoding='utf-8') as fr:
        scores = [int(line.rstrip("\n")) for line in fr.readlines()]
    best_score = max(scores)

    with open('scores.txt', 'w', encoding='utf-8') as fc:
        fc.write(f'{player_score}\n{best_score}\n')


# главное меню
def main_menu():
    all_sprites = pygame.sprite.Group()

    star_sprites = pygame.sprite.Group()
    all_sprites.add(star_sprites)

    start_btn = StartBtn()
    st_btn_pressed_time = 0  # момент с нажатия кнопки

    game_title = pygame.image.load('data/other sprites/title.png').convert_alpha()
    game_title_rect = game_title.get_rect()
    game_title_rect.x = 40
    game_title_rect.y = 100

    bg = pygame.image.load('data/backgrounds/space.png')

    pygame.mixer.music.load('bg music/The Transformers (Theme) (128kbps).mp3')
    pygame.mixer.music.play(-1)

    # кол-во звёзд
    n_stars = 300

    for i in range(n_stars):
        star = Star(star_sprites)
        all_sprites.add(star)

    cybertron = pygame.image.load('data/other sprites/Cybertron.png')
    cybertron_rect = cybertron.get_rect()
    cybertron_rect.bottom = HEIGHT
    cybertron_rect.right = WIDTH

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_btn.rect.collidepoint(event.pos):
                    start_btn.update(event)
                    st_btn_pressed_time = pygame.time.get_ticks()

        screen.blit(bg, (0, 0))

        if len(all_sprites.sprites()) < 302:
            star = Star(star_sprites)
            star.rect.x = 0
            all_sprites.add(star)

        all_sprites.draw(screen)
        all_sprites.update()

        screen.blit(cybertron, cybertron_rect)
        screen.blit(game_title, game_title_rect)
        screen.blit(start_btn.image, start_btn.rect)

        if start_btn.is_pressed and 500 < pygame.time.get_ticks() - st_btn_pressed_time < 600:
            pygame.mixer.music.stop()
            return

        pygame.mixer.music.set_volume(1)

        clock.tick(FPS)
        pygame.display.flip()


# уровень
def main_game():
    game_is_active = True
    all_sprites = pygame.sprite.Group()

    bg = pygame.image.load('data/backgrounds/space.png')

    ground = pygame.image.load('data/other sprites/ground.png')
    ground_rect = ground.get_rect()
    ground_rect.bottom = HEIGHT

    city_speed = 1
    bg_sprites = pygame.sprite.Group()
    bg_city = City(all_sprites, city_speed)
    bg_sprites.add(bg_city)

    cliffjumper = pygame.sprite.GroupSingle(Player())

    vehicons = pygame.sprite.Group()
    vehicon_speed = 10

    # потолок и стенка тоннеля - разные группы, т.к столкновение происходит только с потолком
    tunnel_ceilings = pygame.sprite.Group()
    tunnel_walls = pygame.sprite.Group()
    tunnel_speed = 5

    obstacle_appear = pygame.USEREVENT + 1  # событие появления препятсвия
    pygame.time.set_timer(obstacle_appear, 4000)

    score_font = pygame.font.Font("font/FFFFORWA.TTF", 30)
    go_font = pygame.font.Font('font/FFFFORWA.TTF', 50)
    go_scores_font = pygame.font.Font('font/FFFFORWA.TTF', 20)

    number = 0  # число очков
    score_increase = pygame.USEREVENT + 2  # событие увеличения очков
    pygame.time.set_timer(score_increase, 1000)

    pygame.mixer.music.load('bg music/Transformers Cybertron - Theme Song.mp3')
    pygame.mixer.music.play(-1)
    while True:
        if game_is_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT) or \
                        (event.type == pygame.MOUSEBUTTONDOWN and event.button == 3):
                    cliffjumper.sprite.alt_mode_on = not cliffjumper.sprite.alt_mode_on
                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) and \
                        cliffjumper.sprite.rect.bottom == 294:
                    cliffjumper.sprite.gravity = -18
                if event.type == obstacle_appear:
                    if choice(['vehicon', 'vehicon', 'vehicon', 'tunnel']) == 'tunnel':
                        tunnel_wall = TunnelWall(tunnel_speed)
                        tunnel_walls.add(tunnel_wall)
                        tunnel_ceiling = TunnelCeiling(tunnel_wall.rect.x, tunnel_speed)
                        tunnel_ceilings.add(tunnel_ceiling)
                    else:
                        steve = Enemy(vehicon_speed)
                        vehicons.add(steve)
                if event.type == score_increase:
                    number += 1

            screen.blit(bg, (0, 0))
            screen.blit(ground, ground_rect)

            # если герой в режиме автомобиля, то все объекты вокруг него начинают двигаться быстрее
            if cliffjumper.sprite.alt_mode_on:
                city_speed = 3
                tunnel_speed = 18
                vehicon_speed = 23
            # а если в режиме робота - медленнее
            elif not cliffjumper.sprite.alt_mode_on:
                city_speed = 1
                tunnel_speed = 5
                vehicon_speed = 10

            for sprite in bg_sprites.sprites():
                sprite.speed = city_speed  # обновление скорости

                # зацикливание фона
                if sprite.rect.right == WIDTH:
                    city = City(all_sprites, city_speed)
                    city.rect.left = WIDTH
                    bg_sprites.add(city)
                elif sprite.rect.right == WIDTH + 1:
                    city = City(all_sprites, city_speed)
                    city.rect.left = WIDTH + 1
                    bg_sprites.add(city)
                elif sprite.rect.right == WIDTH + 2:
                    city = City(all_sprites, city_speed)
                    city.rect.left = WIDTH + 2
                    bg_sprites.add(city)

            # обновление скорости стенок тоннелей
            for sprite in tunnel_walls.sprites():
                sprite.speed = tunnel_speed

            # обновление скорости потолков тоннелей
            for sprite in tunnel_ceilings.sprites():
                sprite.speed = tunnel_speed

            # обновление скорости врагов
            for sprite in vehicons.sprites():
                sprite.speed = vehicon_speed

            all_sprites.draw(screen)
            all_sprites.update()

            tunnel_walls.draw(screen)
            tunnel_walls.update()
            tunnel_ceilings.draw(screen)
            tunnel_ceilings.update()

            vehicons.draw(screen)
            vehicons.update()

            cliffjumper.draw(screen)
            cliffjumper.update()

            score = score_font.render(str(number), False, (255, 255, 255))
            score_rect = score.get_rect()
            score_rect.x = WIDTH // 2 - score_rect.w // 2
            score_rect.y = 20
            screen.blit(score, score_rect)

            if collision(cliffjumper.sprite, tunnel_ceilings):
                save_scores(number)
                tunnel_walls.empty()
                tunnel_ceilings.empty()
                game_is_active = False
            if collision(cliffjumper.sprite, vehicons):
                vehicons.empty()
                save_scores(number)
                game_is_active = False

            pygame.mixer.music.set_volume(0.8)

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    game_is_active = True

            pygame.mixer.music.set_volume(0.3)

            number = 0
            cliffjumper.sprite.alt_mode_on = False

            go_text = go_font.render("GAME OVER", False, (255, 255, 255))
            go_rect = go_text.get_rect()
            go_rect.x = WIDTH // 2 - go_rect.w // 2
            go_rect.y = 50

            your_score = go_scores_font.render(f"Your score: {player_score}", False, (255, 255, 255))
            your_score_rect = your_score.get_rect()
            your_score_rect.x = WIDTH // 2 - your_score_rect.w // 2
            your_score_rect.y = 160

            best_score_go = go_scores_font.render(f'Best score: {best_score}', False, (255, 255, 255))
            best_score_go_rect = best_score_go.get_rect()
            best_score_go_rect.x = WIDTH // 2 - best_score_go_rect.w // 2
            best_score_go_rect.y = 230

            how_to_restart_text = go_scores_font.render('Press left mouse button to restart', False, (255, 255, 255))
            how_to_restart_text_rect = how_to_restart_text.get_rect()
            how_to_restart_text_rect.x = WIDTH // 2 - how_to_restart_text_rect.w // 2
            how_to_restart_text_rect.y = 310

            screen.fill((9, 11, 33))
            screen.blit(go_text, go_rect)
            screen.blit(your_score, your_score_rect)
            screen.blit(best_score_go, best_score_go_rect)
            screen.blit(how_to_restart_text, how_to_restart_text_rect)

        pygame.display.flip()
        clock.tick(24)


main_menu()
main_game()
pygame.quit()
