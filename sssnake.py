import pygame
import random
from enum import Enum
from time import sleep


class Color(Enum):
    white = (252, 252, 252)
    black = (0, 0, 0)
    red = (220, 0, 0)
    green = (0, 180, 0)
    blue = (0, 0, 220)


class SssnakeGame:
    # class elements
    speed = 1
    FPS_normal = 30
    FPS_intro = 30
    initial_snake_length = 2
    font_name = "ARCADE.TTF"

    board_width = 800
    board_height = 600

    def __init__(self):
        # initialize pygame & display window
        pygame.init()
        self.game_display = pygame.display.set_mode((self.board_width, self.board_height))
        pygame.display.set_caption("Sssnake")
        pygame.display.set_icon(pygame.image.load("apple_icon.bmp"))

        #  object elements
        self.small_font = pygame.font.Font(self.font_name, 25)  # pygame.font.SysFont(None, 25)
        self.medium_font = pygame.font.Font(self.font_name, 50)
        self.large_font = pygame.font.Font(self.font_name, 80)
        self.clock = pygame.time.Clock()
        self.img_head = pygame.image.load('snake_head.png')
        self.img_apple = pygame.image.load('apple.png')

    def text_object(self, message, color, size):
        if size == "small":
            text_surface = self.small_font.render(message, True, color)
        elif size == "medium":
            text_surface = self.medium_font.render(message, True, color)
        elif size == "large":
            text_surface = self.large_font.render(message, True, color)
        return text_surface, text_surface.get_rect()

    def message_to_screen(self, message, color, size="small", y_displacement=0):
        text_surface, text_rect = self.text_object(message, color, size)
        text_rect.center = (self.board_width / 2), (self.board_height / 2 + y_displacement)
        self.game_display.blit(text_surface, text_rect)

    def score_to_screen(self, message):
        text_surface, text_rect = self.text_object(message, Color.black.value, "small")
        text_rect.topleft = 50, 10
        self.game_display.blit(text_surface, text_rect)

    def game_intro(self):
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        intro = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
            self.game_display.fill(Color.white.value)
            self.message_to_screen("Welcome to Sssnake", Color.green.value, "large", -100)
            self.message_to_screen("Don't run into edges or yourself", Color.black.value, "small", 0)
            self.message_to_screen("Eat the red apples", Color.black.value, "small", 50)
            self.message_to_screen("Press C to play or Q to quit", Color.black.value, "medium", 100)
            pygame.display.update()
            self.clock.tick(self.FPS_normal)

    def event_handler(self, game_exit, block_size, pos_change, direction):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "right":
                    pos_change[0] = -self.speed * block_size
                    pos_change[1] = 0
                    direction = "left"
                if event.key == pygame.K_RIGHT and direction != "left":
                    pos_change[0] = self.speed * block_size
                    pos_change[1] = 0
                    direction = "right"
                if event.key == pygame.K_UP and direction != "down":
                    pos_change[0] = 0
                    pos_change[1] = -self.speed * block_size
                    direction = "up"
                if event.key == pygame.K_DOWN and direction != "up":
                    pos_change[0] = 0
                    pos_change[1] = self.speed * block_size
                    direction = "down"
        return game_exit, direction

    def snake_draw(self, snake_body, block_size, direction):
        if direction == "right":
            head = self.img_head
        elif direction == "left":
            head = pygame.transform.rotate(self.img_head, 180)
        elif direction == "up":
            head = pygame.transform.rotate(self.img_head, 90)
        elif direction == "down":
            head = pygame.transform.rotate(self.img_head, 270)
        self.game_display.blit(head, [snake_body[-1][0], snake_body[-1][1]])
        for snake_piece in snake_body[:-1]:
            self.game_display.fill(Color.green.value, [snake_piece[0], snake_piece[1], block_size, block_size])

    def random_pos(self, object_size):
        return [round(random.randrange(0, (self.board_width - object_size))),
                round(random.randrange(0, (self.board_height - object_size)))]

    def game_loop(self):
        game_exit = False
        game_over = False
        direction = "right"
        snake_block_size = 20
        snake_body = []
        snake_length = self.initial_snake_length
        start_position = [self.board_width / 2, self.board_height / 2]  # x, y
        snake_head = start_position
        pos_change = [self.speed * snake_block_size, 0]  # start moving right, x speed = ...
        apple_size = 50
        apple_pos = self.random_pos(apple_size)

        # main game loop start
        while not game_exit:
            while game_over:
                self.game_display.fill(Color.white.value)
                self.message_to_screen("Game over", Color.red.value, "large", -100)
                self.message_to_screen("Score: %d" % (snake_length - self.initial_snake_length),
                                       Color.black.value, "medium", -20)
                self.message_to_screen("Press C to play again or Q to quit", Color.black.value, "medium", 100)
                pygame.display.update()
                self.clock.tick(self.FPS_normal)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_exit = True
                        game_over = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_exit = True
                            game_over = False
                        if event.key == pygame.K_c:
                            self.game_loop()

            game_exit, direction = self.event_handler(game_exit, snake_block_size, pos_change, direction)

            # MAIN LOGIC
            snake_head[0] += pos_change[0]
            snake_head[1] += pos_change[1]

            # check for collisions
            if snake_head[0] >= self.board_width or snake_head[0] < 0 or \
                    snake_head[1] >= self.board_height or snake_head[1] < 0:
                game_over = True
            for snake_element in snake_body[:-1]:
                if snake_element == snake_head:
                    game_over = True

            # eat apple
            if ((apple_pos[0] <= snake_head[0] < (apple_pos[0] + apple_size)) or \
                (apple_pos[0] <= snake_head[0] + snake_block_size < (apple_pos[0] + apple_size))) \
                    and \
                    ((apple_pos[1] <= snake_head[1] < (apple_pos[1] + apple_size)) or \
                     (apple_pos[1] <= snake_head[1] + snake_block_size < (apple_pos[1] + apple_size))):
                apple_pos = self.random_pos(apple_size)
                snake_length += 1

            snake_body.append(snake_head.copy())
            if len(snake_body) > snake_length:
                del snake_body[0]

            # drawing stuff
            if not game_over:
                self.game_display.fill(Color.white.value)  # clean the game board
                #self.game_display.fill(Color.red.value, [apple_pos[0], apple_pos[1], apple_size, apple_size])
                self.game_display.blit(self.img_apple, [apple_pos[0], apple_pos[1]])
                self.snake_draw(snake_body, snake_block_size, direction)
                self.score_to_screen("%d" % (snake_length - self.initial_snake_length))
                pygame.display.update()  # frame done, render it

                self.clock.tick(self.FPS_normal)  # don't change fps for difficulty, change movement speed
        # main game loop end

        pygame.quit()
        quit()
