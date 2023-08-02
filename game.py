import pygame, sys, random


def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos - 700))
    return bottom_pipe, top_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes


def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 568:
            screen.blit(pipe_surface, pipe)
        else:
            # Flip pipe if it is top pipe
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -15 or bird_rect.bottom >= 650:
        return False
    return True


def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1,-bird_movement*3,1)
    return new_bird


def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main':
        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center=(216,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 615))
        screen.blit(high_score_surface, high_score_rect)


def set_highscore(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.init()
screen = pygame.display.set_mode((432, 768))

# FPS
clock = pygame.time.Clock()
fps = 120

game_font = pygame.font.Font('04B_19.ttf', 40)
score = 0
high_score = 0

# Gravity
gravity = 0.16
bird_movement = 0

game_active = True

# Background
bg = pygame.image.load('assests/background-night.png').convert()
bg = pygame.transform.scale2x(bg)

# Floor
floor = pygame.image.load('assests/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

# Bird
bird_down = pygame.image.load('assests/yellowbird-downflap.png').convert_alpha()
bird_down = pygame.transform.scale2x(bird_down)
bird_mid = pygame.image.load('assests/yellowbird-midflap.png').convert_alpha()
bird_mid = pygame.transform.scale2x(bird_mid)
bird_up = pygame.image.load('assests/yellowbird-upflap.png').convert_alpha()
bird_up = pygame.transform.scale2x(bird_up)
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center=(100, 384))
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap,200)

# Pipe
pipe_surface = pygame.image.load('assests/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = [250, 300, 350]

# Timer
spawn_pipe = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe, 1700)

# Game over Surface
game_over_surface = pygame.transform.scale2x(pygame.image.load('assests/gameover.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(216,384))

while True:
    for event in pygame.event.get():
        # event Quit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -5
            # Play again
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
                score = 0
        if event.type == spawn_pipe:
            pipe_list.extend(create_pipe())
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()

    screen.blit(bg, (0, 0))

    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)

        game_active = check_collision(pipe_list)

        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01

        score_display('main')
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = set_highscore(score, high_score)
        score_display('game_over')

    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0

    pygame.display.update()

    clock.tick(fps)
