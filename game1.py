import pygame
import random

# constants
white = (252, 252, 252)
black = (0, 0, 0)
red = (220, 0, 0)
green = (0, 180, 0)
blue = (0, 0, 220)

speed = 1
FPS = 30

board_width = 800
board_height = 600


# initialize pygame & display window
pygame.init()
game_display = pygame.display.set_mode((board_width, board_height))
pygame.display.set_caption("Snake")

# global objects
font = pygame.font.SysFont(None, 25)
clock = pygame.time.Clock()


def message_to_screen(message, color):
    text_surface = font.render(message, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (board_width/2), (board_height/2)
    game_display.blit(text_surface, text_rect)


def event_handler(game_exit, block_size, pos_change):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and event_handler.previous_event != pygame.K_RIGHT:
                pos_change[0] = -speed * block_size
                pos_change[1] = 0
                event_handler.previous_event = pygame.K_LEFT
            if event.key == pygame.K_RIGHT and event_handler.previous_event != pygame.K_LEFT:
                pos_change[0] = speed * block_size
                pos_change[1] = 0
                event_handler.previous_event = pygame.K_RIGHT
            if event.key == pygame.K_UP and event_handler.previous_event != pygame.K_DOWN:
                pos_change[0] = 0
                pos_change[1] = -speed * block_size
                event_handler.previous_event = pygame.K_UP
            if event.key == pygame.K_DOWN and event_handler.previous_event != pygame.K_UP:
                pos_change[0] = 0
                pos_change[1] = speed * block_size
                event_handler.previous_event = pygame.K_DOWN
    return game_exit


event_handler.previous_event = 0


def snake_draw(snake_body, block_size):
    for snake_piece in snake_body:
        game_display.fill(green, [snake_piece[0], snake_piece[1], block_size, block_size])


def random_pos(object_size):
    return [round(random.randrange(0, (board_width - object_size))),
            round(random.randrange(0, (board_height - object_size)))]


# main game loop
def game_loop():
    game_exit = False
    game_over = False
    pos_change = [0, 0]
    start_position = [board_width / 2, board_height / 2]  # x, y
    snake_head = start_position
    block_size = 20
    snake_body = []
    snake_length = 1
    apple_size = 50
    apple_pos = random_pos(apple_size)

    while not game_exit:
        while game_over:
            game_display.fill(white)
            message_to_screen("Game over (score: %d), press C to play again or Q to quit" % (snake_length - 1), red)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_exit = True
                        game_over = False
                    if event.key == pygame.K_c:
                        game_loop()

        game_exit = event_handler(game_exit, block_size, pos_change)

        # MAIN LOGIC
        snake_head[0] += pos_change[0]
        snake_head[1] += pos_change[1]

        # check for collisions
        if snake_head[0] >= board_width or snake_head[0] < 0 or snake_head[1] >= board_height or snake_head[1] < 0:
            game_over = True
        for snake_element in snake_body[:-1]:
            if snake_element == snake_head:
                game_over = True

        # eat apple
        if ((apple_pos[0] <= snake_head[0] < (apple_pos[0] + apple_size)) or\
            (apple_pos[0] <= snake_head[0] + block_size < (apple_pos[0] + apple_size)))\
            and \
            ((apple_pos[1] <= snake_head[1] < (apple_pos[1] + apple_size)) or\
             (apple_pos[1] <= snake_head[1] + block_size < (apple_pos[1] + apple_size))):
            apple_pos = random_pos(apple_size)
            snake_length += 1

        snake_body.append(snake_head.copy())
        if len(snake_body) > snake_length:
            del snake_body[0]

        # drawing stuff
        if not game_over:
            game_display.fill(white)  # clean the game board
            game_display.fill(red, [apple_pos[0], apple_pos[1], apple_size, apple_size])
            snake_draw(snake_body, block_size)
            pygame.display.update()  # frame done, render it

        clock.tick(FPS)  # don't change fps for difficulty, change movement speed

    pygame.quit()
    quit()


# Start the game
game_loop()
