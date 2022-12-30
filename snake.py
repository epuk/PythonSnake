import pygame, sys, time, random
from pygame import mixer

# Настройки сложности
# Легко =  10
# Средне = 25
# Тяжело = 40
# Тяжелее = 60
# Самый сложный = 120
difficulty = 25

# Размер окна
frame_size_x = 720
frame_size_y = 480

# Ошибки
check_errors = pygame.init()
# pygame.init() пример -> (6, 0)
# второе число выдает кол-во ошибок
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')


# Окно
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))
bg = pygame.image.load('bg.png')
bg = pygame.transform.scale(bg, (720, 480))
#pygame.mixer.music.load('music.mp3')
#pygame.mixer.music.play()



#Цвета (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
pink = pygame.Color(255, 20, 147)
dark_pink = pygame.Color(255,105,180)

# Фпс
fps_controller = pygame.time.Clock()


# Объекты игры
snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0


# Гейм овер тупа
def game_over():
    my_font = pygame.font.SysFont('kacstbook', 90)
    game_over_surface = my_font.render('YOU DIED', True, dark_pink)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(white)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, dark_pink, 'kacstbook', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


# Счет
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)
    pygame.display.flip()


# Правила игры
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Запрет змеи на поворот в другую сторону
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Движение змея
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Механизм удлинения змея
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        explosionSound = mixer.Sound('eating.mp3')
        explosionSound.play()

        food_spawn = False
    else:
        snake_body.pop()

    # Спавн еды на карте
    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True

    # Змейка и окно
    game_window.blit(bg, (0, 0))
    for pos in snake_body:
        pygame.draw.rect(game_window, dark_pink, pygame.Rect(pos[0], pos[1], 10, 10))

    # Еда змеи
    pygame.draw.rect(game_window, pink, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Условия окончания игры
    # Выход за границы
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
        deathSound = mixer.Sound('lose.wav')
        deathSound.play()
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
        deathSound = mixer.Sound('lose.wav')
        deathSound.play()
        game_over()
    
        
    # Косание тела змеи
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    show_score(1, dark_pink, 'kacstbook', 20)
    # Обновление игрвого окна
    pygame.display.update()
    # Обновление тела змеи
    fps_controller.tick(difficulty)
