import os
import random
import sqlite3
import sys
import pygame

all_sprites = pygame.sprite.Group()
food_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(name: str, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
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


pygame.init()
screen_size = WIDTH, HEIGHT = (600, 600)
screen = pygame.display.set_mode(screen_size)
FPS = 6
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def name_input_screen():
    intro_text = ["Добро пожаловать в Змейку",
                  "",
                  "Введите имя:",
                  "",
                  '',
                  "Продолжить"]

    fon = pygame.transform.scale(load_image('backgrounds/main_menu_background.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 150
    BUTTONS = []
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 150
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        BUTTONS.append([*intro_rect, line])
    user_text = ''

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                coords = event.pos
                for i in BUTTONS:
                    if i[0] <= coords[0] <= i[0] + i[2] and i[1] <= coords[1] <= i[1] + i[3]:
                        if i[4] == intro_text[-1]:
                            return user_text

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

        pygame.draw.rect(screen, 'orange', (150, 260, 200, 25))
        text_surface = font.render(user_text, True, "black")

        # рендеринг согласно вводу мени пользователя
        screen.blit(text_surface, (155, 265, 200, 25))

        pygame.display.flip()
        clock.tick(FPS)


def level_select_screen(user_name: str):
    intro_text = ["Добро пожаловать в Змейку,",
                  f"{user_name}",
                  "Выбор уровня:",
                  "  Пустое поле",
                  "  Поле с границами",
                  "  Поле со стенками внутри",
                  "",
                  "Таблица лидеров"]

    fon = pygame.transform.scale(load_image('backgrounds/main_menu_background.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 150
    BUTTONS = []
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 150
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        BUTTONS.append([*intro_rect, line])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                coords = event.pos
                for i in BUTTONS:
                    if i[0] <= coords[0] <= i[0] + i[2] and i[1] <= coords[1] <= i[1] + i[3]:
                        if i[4] == intro_text[3]:
                            return 'levels/lvl_easy.txt'
                        elif i[4] == intro_text[4]:
                            return 'levels/lvl_medium.txt'
                        elif i[4] == intro_text[5]:
                            return 'levels/lvl_hard.txt'
                        elif i[4] == intro_text[7]:
                            return "lb"

        pygame.display.flip()
        clock.tick(FPS)


def leaderboard():
    data = cur.execute("""SELECT name, count, diff FROM statistic""").fetchall()
    lb_text = ["Имя             Количество             Сложность"]
    for j in data:
        temp = f'{j[0].ljust(25, " ")}{str(j[1]).ljust(26, " ")}{j[2]}'
        lb_text.append(temp)
    fon = pygame.transform.scale(load_image('backgrounds/leaderboard_background.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font('data/CoreSans.ttf', 25)
    screen.blit(font.render("Нажмите в любом месте для выхода",
                            1, pygame.Color('white')), (120, 550))
    text_coord = 50
    for line in lb_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 100
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return

        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename: str):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'wall': load_image('textures/wall.png'),
    'empty': load_image('textures/water.png')
}
player_image = load_image('textures/duck.png')

tile_width = tile_height = 50

food_image = load_image('textures/apple.png')


screen_rect = (0, 0, WIDTH, HEIGHT)
GRAVITY = 10


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("textures/star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


class Food(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, food_group)
        self.image = food_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 5, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def spawn(self, y: int, x: int):
        self.pos = (x, y)
        self.rect = self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 5,
                                               tile_width * self.pos[1] + 5)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 8, tile_height * pos_y + 7)
        self.pos = (pos_x, pos_y)
        self.points = 0

    def move(self, x, y):
        self.pos = x, y
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 8,
                                               tile_width * self.pos[1] + 7)
        if pygame.sprite.spritecollideany(self, food_group):
            generate_food(level_map)
            create_particles((x, y))
            increase(x, y)
            self.points += 1
            score(self.points)


player = None
food = Food(5, 7)


def score(points):
    font = pygame.font.Font(None, 30)
    screen.blit(font.render(f"Ваш счёт:{points}",
                            1, pygame.Color('red')), (10, 100, 100, 100))


def increase(x, y):
    sprite = Player(x, y)
    snake_list.append(sprite)


def create_particles(position: tuple):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))
    all_sprites.update()


def generate_food(level):
    x, y = random.randint(1, 10), random.randint(0, 10)
    while level[y][x] != '.':
        x, y = random.randint(1, 10), random.randint(0, 10)
    food.spawn(y, x)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
                level[y] = level[y][:x] + '.' + level[y][x + 1:]
    # вернем игрока, а также размер поля в клетках
    generate_food(level)
    return new_player, x, y


def move(hero, movement: str):
    x, y = hero.pos
    if movement == 'up':
        if y > 0 and level_map[y - 1][x] == '.':
            hero.move(x, y - 1)
        else:
            return False
    if movement == 'down':
        if y > 0 and level_map[y + 1][x] == '.':
            hero.move(x, y + 1)
        else:
            return False
    if movement == 'left':
        if x > 0 and level_map[y][x - 1] == '.':
            hero.move(x - 1, y)
        else:
            return False
    if movement == 'right':
        if y > 0 and level_map[y][x + 1] == '.':
            hero.move(x + 1, y)
        else:
            return False


def game_over():
    font = pygame.font.Font(None, 30)
    screen.blit(font.render("Вы проиграли. Нажмите в любом месте для выхода",
                            1, pygame.Color('red')), (10, 100, 100, 100))


running = True
con = sqlite3.connect('data/game_stat.db')
cur = con.cursor()
user_name = name_input_screen()
while level_select_screen(user_name) == 'lb':
    leaderboard()
level = level_select_screen(user_name)
level_map = load_level(level)
hero, max_X, max_y = generate_level(level_map)
snake_list = [hero]
length_of_snake = 1
err = None
dest = 'down'
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if dest != 'down':
                    dest = 'up'
                else:
                    err = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if dest != 'up':
                    dest = 'down'
                else:
                    err = False
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if dest != 'right':
                    dest = 'left'
                else:
                    err = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if dest != 'left':
                    dest = 'right'
                else:
                    err = False

            if event.key == pygame.K_q:
                running = False
    if err is not False:
        for i in snake_list:
            err = move(i, dest)
    else:
        game_over()




    screen.fill(pygame.Color('Black'))
    tiles_group.draw(screen)
    player_group.draw(screen)
    food_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
