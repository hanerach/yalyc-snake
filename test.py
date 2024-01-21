import pygame
import random

# Инициализация окна игры
pygame.init()

# Установка размеров окна
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Игра Змейка")

# Установка цветов
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Установка скорости змейки
snake_speed = 15

# Инициализация начальных координат змейки
x1 = width / 2
y1 = height / 2

# Инициализация изменений координат
x1_change = 0
y1_change = 0

# Инициализация длины змейки
snake_list = []
length_of_snake = 1

# Создание случайного положения пищи
food_x = round(random.randrange(0, width - 10) / 10.0) * 10.0
food_y = round(random.randrange(0, height - 10) / 10.0) * 10.0


# Функция отображения змейки
def show_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(window, black, [x[0], x[1], 10, 10])


# Главный игровой цикл
game_over = False
while not game_over:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x1_change = -10
                y1_change = 0
            elif event.key == pygame.K_RIGHT:
                x1_change = 10
                y1_change = 0
            elif event.key == pygame.K_UP:
                y1_change = -10
                x1_change = 0
            elif event.key == pygame.K_DOWN:
                y1_change = 10
                x1_change = 0

    # Обновление координат змейки
    x1 += x1_change
    y1 += y1_change

    # Ограничение движения змейки в пределах окна
    if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
        game_over = True

    # Очистка окна
    window.fill(white)

    # Отрисовка пищи
    pygame.draw.rect(window, red, [food_x, food_y, 10, 10])

    # Обновление списка координат змейки
    snake_head = []
    snake_head.append(x1)
    snake_head.append(y1)
    snake_list.append(snake_head)
    if len(snake_list) > length_of_snake:
        del snake_list[0]

    # Проверка столкновения змейки с самой собой
    for x in snake_list[:-1]:
        if x == snake_head:
            game_over = True

    # Отображение змейки
    show_snake(snake_list)

    # Обновление экрана
    pygame.display.update()

    # Проверка, съела ли змейка пищу
    if x1 == food_x and y1 == food_y:
        # Создание нового положения пищи
        food_x = round(random.randrange(0, width - 10) / 10.0) * 10.0
        food_y = round(random.randrange(0, height - 10) / 10.0) * 10.0
        # Увеличение длины змейки
        length_of_snake += 1

    # Установка скорости обновления экрана
    pygame.time.Clock().tick(snake_speed)

# Освобождение ресурсов pygame
pygame.quit()
