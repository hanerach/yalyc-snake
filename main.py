import os
import random
import sqlite3
import sys
import pygame

# инициализация групп спрайтов
particle_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
food_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
head_group = pygame.sprite.Group()
tail_group = pygame.sprite.Group()


# функция загрузки изображения
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


# инициализация окна pygame
pygame.init()
# размеры экрана
screen_size = WIDTH, HEIGHT = (600, 600)
screen = pygame.display.set_mode(screen_size)
# ограничение скорости обновления экрана
FPS = 6
clock = pygame.time.Clock()


# функция для закрытия окна
def terminate():
    pygame.quit()
    sys.exit()


# функция вызова стартскрина для ввода имени
def name_input_screen():
    intro_text = ["Добро пожаловать в Змейку",
                  "",
                  "Введите имя:",
                  "",
                  '',
                  "Продолжить"]
    # отображение фона
    fon = pygame.transform.scale(load_image('backgrounds/main_menu_background.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    # инициализация шрифта
    font = pygame.font.Font(None, 30)
    text_coord = 150
    # список для хранения кнопок и соответсвующих им координат
    buttons = []
    # цикл рендера текста
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 150
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        buttons.append([*intro_rect, line])

    user_text = ''

    while True:
        for event in pygame.event.get():
            # если закрывают окно, то прекращаем работу
            if event.type == pygame.QUIT:
                terminate()
            # если пользователь нажимает на мышку, то определяем координаты нажатия и проверяем попадают ли они
            # в координаты кнопки
            elif event.type == pygame.MOUSEBUTTONDOWN:
                coords = event.pos
                for i in buttons:
                    if i[0] <= coords[0] <= i[0] + i[2] and i[1] <= coords[1] <= i[1] + i[3]:
                        if i[4] == intro_text[-1]:
                            return user_text if user_text else 'Unknown'
            # ввод текста
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
        # рисуем поле для ввода
        pygame.draw.rect(screen, 'orange', (150, 260, 200, 25))
        text_surface = font.render(user_text, True, "black")

        # рендеринг согласно вводу мени пользователя
        screen.blit(text_surface, (155, 265, 200, 25))

        pygame.display.flip()
        clock.tick(FPS)


# функция для стартскрина с выбором уровня
def level_select_screen(user_name: str):
    intro_text = ["Добро пожаловать в Змейку,",
                  f"{user_name}",
                  "Выбор уровня:",
                  "",
                  "  Поле с границами",
                  "  Поле со стенками внутри",
                  "",
                  "Таблица лидеров"]
    # рисуем фон
    fon = pygame.transform.scale(load_image('backgrounds/main_menu_background.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    # инициализация шрифта
    font = pygame.font.Font(None, 30)
    text_coord = 150
    # список для хранения кнопок и их координат
    buttons = []
    # рендер текста
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 150
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        buttons.append([*intro_rect, line])

    while True:
        for event in pygame.event.get():
            # если окно закрывают, то прекращаем работу программы
            if event.type == pygame.QUIT:
                terminate()
            # если пользователь нажимает на мышку, то определяем координаты нажатия и проверяем попадают ли они
            # в координаты кнопки
            elif event.type == pygame.MOUSEBUTTONDOWN:
                coords = event.pos
                for i in buttons:
                    if i[0] <= coords[0] <= i[0] + i[2] and i[1] <= coords[1] <= i[1] + i[3]:
                        if i[4] == intro_text[4]:
                            return 'levels/lvl_medium.txt'
                        elif i[4] == intro_text[5]:
                            return 'levels/lvl_hard.txt'
                        elif i[4] == intro_text[7]:
                            return "lb"

        pygame.display.flip()
        clock.tick(FPS)


# функция для отображения таблицы лидеров
def leaderboard():
    # читаем данные из бд
    data = cur.execute("""SELECT name, count, diff FROM statistic""").fetchall()
    lb_text = ["Имя             Количество             Сложность"]
    # форматирование текста с данными
    for j in data:
        temp = f'{j[0].ljust(25, " ")}{str(j[1]).ljust(26, " ")}{j[2]}'
        lb_text.append(temp)
    # фон
    fon = pygame.transform.scale(load_image('backgrounds/leaderboard_background.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    # шрифт
    font = pygame.font.Font('data/CoreSans.ttf', 25)
    screen.blit(font.render("Нажмите в любом месте для выхода",
                            1, pygame.Color('white')), (120, 550))
    text_coord = 50
    # рендер текста с данными
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
            # если окно закрывают, то прекращаем работу
            if event.type == pygame.QUIT:
                terminate()
            # если нажимают на мышку, то выходим из таблицы лидеров
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return

        pygame.display.flip()
        clock.tick(FPS)


# загрузка уровня
def load_level(filename: str):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# инициализация текстур для спрайтов и окружения
tile_images = {
    'wall': load_image('textures/wall.png'),
    'empty': load_image('textures/water.png')
}

head_image = load_image('textures/image17 (2).png')
tail_image = load_image('textures/tail.png')
food_image = load_image('textures/apple.png')

# размеры клетки
tile_width = tile_height = 50

# прямоугольник экрана для проверки вылета партиклов за его пределы
screen_rect = (0, 0, WIDTH, HEIGHT)
# гравитация для партиклов сбора яблок, чем больше, тем быстрее летят частицы
GRAVITY = 20


# класс частиц
class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("textures/star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos: tuple, dx: int, dy: int):
        super().__init__(particle_group)
        # распоковываем координаты из кортежа
        pos_x, pos_y = pos
        # рандомно выбираем картинку частицы (перед __init__ сгенерировали разные размеры частиц)
        self.image = random.choice(self.fire)
        # прямоугольник где отображать частицы
        self.rect = self.rect = self.image.get_rect().move(
            tile_width * pos_x + 8, tile_height * pos_y + 7)
        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect_x, self.rect_y = pos

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


# класс яблок (еды)
class Food(pygame.sprite.Sprite):
    def __init__(self, pos_x: int, pos_y: int):
        super().__init__(all_sprites, food_group)
        # инициализируем текстуру
        self.image = food_image
        # прямоугольник, в котором отображать яблоко
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 5, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def spawn(self, y: int, x: int):
        # меняем координаты и прямоугольник спавна
        self.pos = (x, y)
        self.rect = self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 5,
                                                           tile_width * self.pos[1] + 5)


# класс клетки
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type: str, pos_x: int, pos_y: int):
        super().__init__(tiles_group, all_sprites)
        # инициализируем текстуру
        self.image = tile_images[tile_type]
        # прямоугольник для отображения клетки
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


# класс головы
class Head(pygame.sprite.Sprite):
    def __init__(self, pos_x: int, pos_y: int, sheet, columns=5, rows=2):
        super().__init__(head_group, all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        # инициализация текстуры
        #self.image = head_image

        # прямоугольник в котором спавнить спрайт
        #self.rect = self.image.get_rect().move(
            #tile_width * pos_x + 8, tile_height * pos_y + 7)
        # координаты
        self.pos = (pos_x, pos_y)
        # список для хранения координат хвоста
        self.tail_coords = []
        # список для хранения экземпляров хвоста
        self.tail_list = []

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def move(self, x: int, y: int):
        # добавляем координаты до передвежения
        self.tail_coords.insert(0, self.pos)
        # меняем координаты на новые, то бишь двигаемся
        self.pos = x, y
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 8,
                                               tile_width * self.pos[1] + 7)
        # если просходит коллизия с яблоком
        if pygame.sprite.spritecollideany(self, food_group):
            # создаём экземпляр хвоста
            tail = Tail(*self.tail_coords[-1])
            # добавляем этот экземпляр в список
            self.tail_list.append(tail)
            # генерируем новое яблоко
            generate_food(level_map, self.tail_coords)
            # возвращаем позицию для проверки из вне, была коллизия или нет
            return self.pos
        # если нет коллизии, то удаляем последний элемент, так как прибавления длины нет
        else:
            self.tail_coords.pop()

        # двигаем каждый экземпляр хвоста
        for i in range(len(self.tail_list)):
            self.tail_list[i].move(self.tail_coords[i])
        # если коллизия с хвостом, то возвращаем True для определения проигрыша
        if pygame.sprite.spritecollideany(self, tail_group):
            return True


# класс хвоста
class Tail(pygame.sprite.Sprite):
    def __init__(self, pos_x: int, pos_y: int):
        super().__init__(tail_group, all_sprites)
        # инициализация картинки
        self.image = tail_image
        # где спавнить
        self.rect = self.rect = self.image.get_rect().move(
            tile_width * pos_x + 8, tile_height * pos_y + 7)
        self.pos = (pos_x, pos_y)

    def move(self, pos: tuple):
        # меняем позицию
        self.pos = pos
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 8,
                                               tile_width * self.pos[1] + 7)


# иниицализируем яблоко
food = Food(5, 7)


# функция создания еды
def generate_food(level, tail_coords):
    # рандомные координаты
    x, y = random.randint(1, 10), random.randint(0, 10)
    # если координаты выпали на тело змеи или на стену, то перевыбираем
    while level[y][x] != '.' or (x, y) in tail_coords:
        x, y = random.randint(1, 10), random.randint(0, 10)
    # спавним еду
    food.spawn(y, x)


# генерация уровня
def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            # читаем файл уровня и понимаем какие объекты на каком месте стоят
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Head(x, y, head_image)
                level[y] = level[y][:x] + '.' + level[y][x + 1:]
    # вернем игрока, а также размер поля в клетках и сгенирируем яблоко
    generate_food(level, [(0, 0)])
    return new_player, x, y


# функция передвежения головы
def move(hero, movement: str):
    x, y = hero.pos
    # понимаем в какую сторону повернулась змея, и вызываем метод головы для изменения координат
    if movement == 'up':
        if y > 0 and level_map[y - 1][x] == '.':
            return hero.move(x, y - 1)
        else:
            return True
    if movement == 'down':
        if y > 0 and level_map[y + 1][x] == '.':
            return hero.move(x, y + 1)
        else:
            return True
    if movement == 'left':
        if x > 0 and level_map[y][x - 1] == '.':
            return hero.move(x - 1, y)
        else:
            return True
    if movement == 'right':
        if y > 0 and level_map[y][x + 1] == '.':
            return hero.move(x + 1, y)
        else:
            return True


# функция преращения игры
def game_over():
    screen.fill('black')
    font = pygame.font.Font(None, 30)
    screen.blit(font.render("Вы проиграли. Нажмите в любом месте для продолжения",
                            1, pygame.Color('red')), (15, 300, 100, 100))
    while True:
        # ждём действия
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


# подлючаем бд и создаём курсор для взаимодействия с ней
con = sqlite3.connect('data/game_stat.db')
cur = con.cursor()
# начальные экраны и таблица лидеров
user_name = name_input_screen()
while level_select_screen(user_name) == 'lb':
    leaderboard()
# определяем какой уровень выбрал игрок
level = level_select_screen(user_name)
level_map = load_level(level)
hero, max_X, max_y = generate_level(level_map)
# переменные для персонажа
lose = None
dest = 'down'

running = True
# основной цикл программы
while running:
    points = len(tail_group)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            # смена направления движения
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if dest != 'down':
                    dest = 'up'

            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if dest != 'up':
                    dest = 'down'

            if event.key == pygame.K_LEFT or event.key == pygame.K_a:

                if dest != 'right':
                    dest = 'left'

            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if dest != 'left':
                    dest = 'right'

            if event.key == pygame.K_q:
                running = False
    # lose - если True, то проигрыш, если tuple, то было столкновение с яблоком и нужно отобразить партиклы
    hero.update()
    if lose is not True:
        lose = move(hero, dest)

    if type(lose) == tuple:
        particle_count = 5
        # возможные скорости
        numbers = range(-5, 6)
        for _ in range(particle_count):
            Particle(hero.pos, random.choice(numbers), random.choice(numbers))
    # рисуем все спрайты
    screen.fill(pygame.Color('Black'))
    particle_group.update()
    tiles_group.draw(screen)
    tail_group.draw(screen)
    head_group.draw(screen)
    food_group.draw(screen)
    particle_group.draw(screen)
    # прекращаем работу программы
    if lose is True:
        running = False
    else:
        # ведём счёт яблок
        font = pygame.font.Font(None, 30)
        screen.blit(font.render(f"Ваш счёт:{points}",
                                1, pygame.Color('green')), (250, 20, 100, 100))

    clock.tick(FPS)
    pygame.display.flip()
# добавляем попытку в базу данных
if level == 'levels/lvl_hard.txt':
    diff = 'hard'
else:
    diff = 'medium'
cur.execute('INSERT INTO statistic (name, count, diff) VALUES (?, ?, ?)', (user_name, points, diff))
con.commit()
# экран проигрыша
game_over()
# таблица лидеров
leaderboard()
pygame.quit()
