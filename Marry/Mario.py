import pygame
import random
import os

pygame.init()

# экран
width = 800
heigth = 600
size = width, heigth
screen = pygame.display.set_mode((width, heigth))
clock = pygame.time.Clock()
FPS = 60

# шрифт
font_path = 'mario_font.ttf'
font_large = pygame.font.Font(font_path, 48)
font1_large = pygame.font.Font(font_path, 36)
font_small = pygame.font.Font(font_path, 24)

# появление

spawn_delay = 2000
DECREASE_BASE = 1.01
last_spawn_time = pygame.time.get_ticks()

# ФИНАЛЬНОЕ ОКНО
game_over = False
retry_text = font_small.render('ПОПРОБУЙ СНОВА',
                               True, (255, 255, 255))
retry_rect = retry_text.get_rect()
retry_rect.midtop = (width // 2, heigth // 2)

# результат
score = 0
# надпись результата
lvel = ''

# загружаем картинки
ground_image = pygame.image.load('ground marry.png')
ground_image = pygame.transform.scale(ground_image, (804, 60))
GROUND_H = ground_image.get_height()

enemy_image = pygame.image.load('goomba (2).png')
enemy_image = pygame.transform.scale(enemy_image, (80, 80))

enemy_dead_image = pygame.image.load('goomba_dead.png')
enemy_dead_image = pygame.transform.scale(enemy_dead_image, (80, 80))

player_image = pygame.image.load('marry.png')
player_image = pygame.transform.scale(player_image, (80, 80))

fon_image = pygame.image.load('fon marry.png')
fon_image = pygame.transform.scale(fon_image, (width, heigth))

window = pygame.display.set_mode((width, heigth))
pygame.display.set_caption("Мэрри - супер игра")


# объекты
class Play:
    """Класс игрового объекта. Переопределяется в наследниках."""
    def __init__(self, image):
        """Инициализация объекта."""
        self.image = image
        self.rect = self.image.get_rect()
        self.y_speed = 0
        self.x_speed = 0
        self.speed = 5
        self.speed1 = 5
        self.speed2 = 7
        self.speed3 = 10

        self.is_out = False
        self.is_dead = False
        self.jump_speed = -12
        self.gravity = 0.4
        self.is_grounded = False

    def handle_input(self):
        """Обработка ввода пользователя. Переопределяется в наследниках."""
        pass

    def kill(self, dead_image):
        """Убивает объект. Переопределяется в наследниках."""
        self.image = dead_image
        self.is_dead = True
        self.x_speed = -self.x_speed
        self.y_speed = self.jump_speed

    def update(self):
        # движение
        """Обновление состояния объекта. Переопределяется в наследниках."""
        self.rect.x += self.x_speed
        self.y_speed += self.gravity
        self.rect.y += self.y_speed

        if self.is_dead:
            # проверка на жизнь
            if self.rect.top > heigth - GROUND_H:
                self.is_out = True
        else:
            # движение по горизонтали
            self.handle_input()

            if self.rect.bottom > heigth - GROUND_H:
                self.is_grounded = True
                self.y_speed = 0
                self.rect.bottom = heigth - GROUND_H

    # отрисовка поверхности
    def draw(self, surface):
        """Отрисовка объекта на поверхности. Переопределяется в наследниках."""
        surface.blit(self.image, self.rect)


# класс грибков
class Goomba(Play):
    """Класс грибка. Переопределяет методы родителя."""
    def __init__(self):
        """Инициализация грибка."""
        super().__init__(enemy_image)
        self.spawn()

    # появление грибков
    def spawn(self):
        """Появление грибка. Переопределяется в наследниках."""
        if score <= 10:
            direction = random.randint(0, 1)
        if score >= 10 and score <= 20:
            direction = random.randint(0, 1)
        if score >= 20:
            direction = random.randint(0, 1)
        if direction == 0:
            self.x_speed = -self.speed1
            self.rect.bottomleft = (width, 0)
        else:
            if score <= 10:
                self.x_speed = self.speed1
            elif score >= 10 and score <= 20:
                self.x_speed = self.speed2
            elif score >= 20:
                self.x_speed = self.speed3

            self.rect.bottomright

    def update(self):
        """Обновление состояния грибка. Переопределяется в наследниках."""
        super().update()
        if self.x_speed > 0 and self.rect.left > width or \
                self.x_speed < 0 and self.rect.right < 0:
            self.is_out = True


class Player(Play):
    """Класс игрока. Переопределяет методы родителя."""

    def __init__(self):
        """Инициализация игрока."""
        super().__init__(player_image)
        self.respawn()

    def handle_input(self):
        """Обработка ввода пользователя. Переопределяется в наследниках."""
        self.x_speed = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_speed = -self.speed
        elif keys[pygame.K_a]:
            self.x_speed = -self.speed
        elif keys[pygame.K_RIGHT]:
            self.x_speed = self.speed
        elif keys[pygame.K_d]:
            self.x_speed = self.speed

        if self.is_grounded and keys[pygame.K_UP]:
            self.is_grounded = False
            self.jump()
        if self.is_grounded and keys[pygame.K_w]:
            self.is_grounded = False
            self.jump()

    def respawn(self):
        """Возрождение Марио. Переопределяется в наследниках."""
        self.is_out = False
        self.is_dead = False
        self.rect.midbottom = (width // 2, heigth)

    def jump(self):
        """Прыжок Марио. Переопределяется в наследниках."""
        self.y_speed = self.jump_speed


# запись результатов текущих в текстовый файл
SCORE_FILE = 'score_data.txt'


def save_score(score):
    """Сохранение результата в файл."""
    with open(SCORE_FILE, 'w') as f:
        f.write(str(score))


def load_score():
    """Загрузка результата из файла."""
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, 'r') as f:
            return int(f.read())
    return 0


goombas = []

running = True
gamemode = "menu"
while running:
    if gamemode == "game":
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if player.is_out:
                    score = 0
                    lvel = ''
                    finish_delay = 2000
                    last_spawn_time = pygame.time.get_ticks()
                    player.respawn()
                    goombas.clear()

        clock.tick(FPS)

        screen.fill((248, 24, 128))
        screen.blit(ground_image, (0, heigth - GROUND_H))

        score_surface = font_large.render(str(score),
                                          True, (255, 255, 255))
        level_surface = font1_large.render(lvel,
                                           True, (255, 255, 255))
        score_rect = score_surface.get_rect()
        level_rect = level_surface.get_rect()

        if player.is_out:
            score_rect.midbottom = (width // 2, heigth // 2)

            screen.blit(retry_text, retry_rect)
            save_score(score)
        else:
            now = pygame.time.get_ticks()
            elapsed = now - last_spawn_time

            if elapsed > spawn_delay:
                last_spawn_time = pygame.time.get_ticks()
                goombas.append(Goomba())

            player.update()
            player.draw(screen)

            for goomba in list(goombas):
                if goomba.is_out:
                    goombas.remove(goomba)
                else:
                    goomba.update()
                    goomba.draw(screen)

                    if not player.is_dead and not goomba.is_dead and \
                            player.rect.colliderect(goomba.rect):
                        if player.rect.bottom - player.y_speed < goomba.rect.top:
                            goomba.kill(enemy_dead_image)
                            player.jump()
                            score += 1
                            if score >= 0 and score <= 10:
                                lvel = 'LEVEL 1'
                                spawn_delay = 2000 / (DECREASE_BASE ** score)
                            elif score > 10 and score <= 20:
                                lvel = 'LEVEL 2'
                                spawn_delay = 2000 / (DECREASE_BASE ** score)
                            elif score >= 21:
                                lvel = 'LEVEL HARD'
                                spawn_delay = 2000 / (DECREASE_BASE ** score)
                            spawn_delay = 2000 / (DECREASE_BASE ** score)
                        else:
                            player.kill(player_image)

            # отрисовка результата
            score_rect.midtop = (width // 2, 5)
            level_rect.midtop = (width // 2, 80)

        screen.blit(score_surface, score_rect)
        screen.blit(level_surface, level_rect)
        pygame.display.flip()
    elif gamemode == "menu":
        for i in pygame.event.get():
            if i.type == pygame.MOUSEBUTTONDOWN:
                gamemode = "game"
                player = Player()
            if i.type == pygame.QUIT:
                running = False

        screen.blit(fon_image, (0, 0))
        pygame.display.flip()

quit()