import pygame
import random
import math

pygame.init()  # подключение библиотеки

dis_lenght = 640  # длина экрана
dis_width = 1000  # ширина экрана
dis = pygame.display.set_mode((dis_width, dis_lenght))  # размер игрового поля
pygame.display.set_caption("Змейка")  # название

# color = (r, g, b)
green = (160, 225, 160)
green2 = (133, 217, 121)
red = (255, 0, 0)
black = (0, 0, 0)
blue = (0, 0, 255)
blue2 = (66, 170, 255)
yellow = (252, 221, 118)
white = (255, 255, 255)

clock = pygame.time.Clock()
speed_snake = 5
snake_width = 40
moving_snake = snake_width  # "шаг" змейки

x_list = []
y_list = []

for x1 in range(0, int(dis_width / snake_width)):
    x_list.append(x1)

for y1 in range(0, int(dis_lenght / snake_width)):
    y_list.append(y1)


def fon():
    dis.fill(black)
    for y in range(0, dis_lenght, 2 * snake_width):
        for x in range(0, dis_width, 2 * snake_width):
            pygame.draw.rect(dis, green, [x, y, snake_width, snake_width])
            pygame.draw.rect(dis, green2, [x + snake_width, y, snake_width, snake_width])
        for x in range(0, dis_width, 2 * snake_width):
            pygame.draw.rect(dis, green2, [x, y + snake_width, snake_width, snake_width])
            pygame.draw.rect(dis, green, [x + snake_width, y + snake_width, snake_width, snake_width])


def GameO():
    shrift = pygame.font.SysFont('Arial', 50)  # ArialCalibriTimesnewroman
    text = shrift.render("Game Over", True, red)
    place_text = text.get_rect(center=(dis_width / 2, dis_lenght / 2 - 100))
    dis.blit(text, place_text)


def GameRetry():
    pygame.draw.rect(dis, blue2, [dis_width / 2 - 150, dis_lenght / 2 - 150, 300, 300])

    GameO()
    shrift = pygame.font.SysFont('Arial', 50)

    text = shrift.render("Start again?", True, blue)
    place_text = text.get_rect(center=(dis_width / 2, dis_lenght / 2))
    dis.blit(text, place_text)

    text = shrift.render("Yes?", True, blue)
    place_text = text.get_rect(center=(dis_width / 2 - 60, dis_lenght / 2 + 100))
    dis.blit(text, place_text)

    text = shrift.render("No?", True, red)
    place_text = text.get_rect(center=(dis_width / 2 + 80, dis_lenght / 2 + 100))
    dis.blit(text, place_text)

    pygame.draw.rect(dis, black, [dis_width / 2 - 130, dis_lenght / 2 + 60, 130, 80], 2)
    pygame.draw.rect(dis, black, [dis_width / 2 + 20, dis_lenght / 2 + 60, 120, 80], 2)

    pygame.display.update()
    while True:

        for ans in pygame.event.get():
            if ans.type == pygame.MOUSEBUTTONDOWN:
                if ans.button == 1:  # левая кнопка мыши
                    pos = ans.pos
                    if (pos[1] >= dis_lenght / 2 + 50 and pos[1] <= dis_lenght / 2 + 150):
                        if (pos[0] >= dis_width / 2 - 150 and pos[0] <= dis_width / 2):
                            return False
                        if (pos[0] <= dis_width / 2 + 150 and pos[0] >= dis_width / 2):
                            return True
            if ans.type == pygame.QUIT:
                return True
            if ans.type == pygame.KEYDOWN:
                if ans.key == pygame.K_q:
                    return True
                if ans.key == pygame.K_w or ans.key == pygame.K_UP:
                    return False


def Score(val):
    shrift = pygame.font.SysFont('Arial', 50)  # ArialCalibriTimesnewroman
    stroka = "Score: " + str(val)
    text = shrift.render(stroka, True, black)
    place_text = (0, 0)
    dis.blit(text, place_text)


# игра змейка
def game_snake():
    game_over = False  # проигрыш
    close = False  # закрытие игры
    # перемещение змейки
    x1 = round(dis_width / 2 / snake_width) * snake_width  # начальные координаты змейки
    y1 = round(dis_lenght / 2 / snake_width) * snake_width
    x1_change = 0  # изменения/перемещение
    y1_change = 0
    score = 0

    snake_length = 1
    snake_body = []  # тело змейки по координатам

    # еда
    apple_x = random.choice(x_list) * snake_width
    apple_y = random.choice(y_list) * snake_width
    while not close:
        if game_over == True:
            close = GameRetry()
            if (close == False):
                fon()
                game_snake()
                break

        for event in pygame.event.get():  # получаем события, происходящие на экране
            if event.type == pygame.QUIT:  # добавили выход из игры при попытке закрыть приложение
                close = True
            if event.type == pygame.KEYDOWN:  # считывание движения с клавиатуры
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if x1_change != moving_snake:
                        x1_change = -moving_snake
                        y1_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    if y1_change != moving_snake:
                        x1_change = 0
                        y1_change = -moving_snake
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if x1_change != -moving_snake:
                        x1_change = moving_snake
                        y1_change = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if y1_change != -moving_snake:
                        x1_change = 0
                        y1_change = moving_snake
        x1 += x1_change
        y1 += y1_change

        hit = False
        for a in snake_body[:-1]:
            if a[0] == x1 and a[1] == y1:
                hit = True

        # проверки правил
        if x1 >= dis_width or x1 < 0 or y1 >= dis_lenght or y1 < 0 or hit == True:
            game_over = True

        snake_body.append([x1, y1])
        if len(snake_body) > snake_length:
            del snake_body[0]

        if game_over == False:
            fon()
            b = 255
            for a in reversed(snake_body):
                pygame.draw.circle(dis, (0, 0, b), (a[0] + snake_width / 2, a[1] + snake_width / 2),
                                   snake_width / 2)  # отрисовывание змейки по её координатам
                # pygame.draw.rect(dis, blue, [a[0], a[1], snake_width, snake_width])
                b -= math.ceil(255 / (dis_width / snake_width * dis_lenght / snake_width))
                # print(math.ceil(255 / (dis_width / snake_width * dis_lenght / snake_width)))
                if (b < 0):
                    b = 0

            if x1 == apple_x and y1 == apple_y:
                apple_x = random.choice(x_list) * snake_width
                apple_y = random.choice(y_list) * snake_width
                snake_length += 1
                score += 1

                prov = True
                a = 0
                while prov:
                    a += 1
                    if [apple_x, apple_y] in snake_body:
                        apple_x = random.choice(x_list) * snake_width
                        apple_y = random.choice(y_list) * snake_width
                    else:
                        prov = False

            pygame.draw.circle(dis, red, (apple_x + snake_width / 2, apple_y + snake_width / 2),
                               snake_width / 2)  # отрисовывание яблока

        Score(score)
        pygame.display.update()  # обновление экрана с внесёнными изменениями
        clock.tick(speed_snake)  # скорость перемещения змейки
    pygame.quit()  # выход из библиотеки
    quit()


game_snake()
