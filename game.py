import pygame, sys, container, helper

pygame.init()
screen = pygame.display.set_mode((432, 768))
pygame.display.set_caption(container.title)
icon = pygame.image.load(container.midFlap)
pygame.display.set_icon(icon)

# FPS
clock = pygame.time.Clock()

game_font = pygame.font.Font(container.font, 40)
score = 0
high_score = 0

bird_movement = 0

game_active = True

# Background
bg = pygame.image.load(container.background).convert()
bg = pygame.transform.scale2x(bg)

# Floor
floor = pygame.image.load(container.floor).convert_alpha()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

# Bird
bird_down = pygame.image.load(container.downFlap).convert_alpha()
bird_down = pygame.transform.scale2x(bird_down)
bird_mid = pygame.image.load(container.midFlap).convert_alpha()
bird_mid = pygame.transform.scale2x(bird_mid)
bird_up = pygame.image.load(container.upFlap).convert_alpha()
bird_up = pygame.transform.scale2x(bird_up)
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center=(100, 384))
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 200)

# Pipe
pipe_surface = pygame.image.load(container.pipe).convert_alpha()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = [250, 300, 350]

# Timer
spawn_pipe = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe, 1700)

# Game over Surface
game_over_surface = pygame.transform.scale2x(pygame.image.load(container.gameOverScreen).convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(216, 384))

while True:
    for event in pygame.event.get():
        # event Quit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = -4.5
            # Play again
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
                score = 0
        if event.type == spawn_pipe:
            pipe_list.extend(helper.create_pipe(pipe_surface, pipe_height))
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = helper.bird_animation(bird_rect, bird_list, bird_index)

    screen.blit(bg, (0, 0))

    if game_active:
        bird_movement += container.gravity
        rotated_bird = helper.rotate_bird(bird, bird_movement)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)

        game_active = helper.check_collision(pipe_list, bird_rect)

        pipe_list = helper.move_pipe(pipe_list)
        helper.draw_pipe(screen, pipe_list, pipe_surface)
        score += 0.01

        helper.score_display(screen, container.mainGame, game_font, score, high_score)
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = helper.set_high_score(score, high_score)
        helper.score_display(screen, container.gameOver, game_font, score, high_score)

    floor_x_pos -= 1
    helper.draw_floor(screen, floor, floor_x_pos)
    if floor_x_pos <= -432:
        floor_x_pos = 0

    pygame.display.update()

    clock.tick(container.fps)
