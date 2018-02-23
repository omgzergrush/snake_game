import pygame
import random
from settings import *
from enum import Enum

class SssnakeGame:

    def __init__(self):
        # initialize pygame, sound & display window
        pygame.mixer.pre_init(44100, 16, 2, 4096)  # frequency, size, channels, buffersize
        pygame.init()
        self.game_display = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
        pygame.display.set_caption("Sssnake")
        pygame.display.set_icon(pygame.image.load("apple_icon.bmp"))

        #  object elements
        self.small_font = pygame.font.Font(FONT_NAME, 25)  # pygame.font.SysFont(None, 25)
        self.medium_font = pygame.font.Font(FONT_NAME, 50)
        self.large_font = pygame.font.Font(FONT_NAME, 80)
        self.clock = pygame.time.Clock()
        self.img_head = pygame.image.load('snake_head.png')
        self.img_apple = pygame.image.load('apple.png')
        self.sound_apple = pygame.mixer.Sound('bite.wav')
        self.sound_punch = pygame.mixer.Sound('sharp_punch.wav')

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
        text_rect.center = (BOARD_WIDTH / 2), (BOARD_HEIGHT / 2 + y_displacement)
        self.game_display.blit(text_surface, text_rect)

    def score_to_screen(self, message):
        text_surface, text_rect = self.text_object(message, BLACK, "small")
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
            self.game_display.fill(WHITE)
            self.message_to_screen("Welcome to Sssnake", GREEN, "large", -100)
            self.message_to_screen("Don't run into edges or yourself", BLACK, "small", 0)
            self.message_to_screen("Eat the red apples", BLACK, "small", 50)
            self.message_to_screen("Press C to play or Q to quit", BLACK, "medium", 100)
            pygame.display.update()
            self.clock.tick(FPS_NORMAL)

    def event_handler(self, game_exit, block_size, pos_change, direction):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "right":
                    pos_change[0] = -SPEED * block_size
                    pos_change[1] = 0
                    direction = "left"
                if event.key == pygame.K_RIGHT and direction != "left":
                    pos_change[0] = SPEED * block_size
                    pos_change[1] = 0
                    direction = "right"
                if event.key == pygame.K_UP and direction != "down":
                    pos_change[0] = 0
                    pos_change[1] = -SPEED * block_size
                    direction = "up"
                if event.key == pygame.K_DOWN and direction != "up":
                    pos_change[0] = 0
                    pos_change[1] = SPEED * block_size
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
        else:
            assert False
        self.game_display.blit(head, [snake_body[-1][0], snake_body[-1][1]])
        for snake_piece in snake_body[:-1]:
            self.game_display.fill(GREEN, [snake_piece[0], snake_piece[1], block_size, block_size])

    def random_pos(self, object_size):
        return [round(random.randrange(0, (BOARD_WIDTH - object_size))),
                round(random.randrange(0, (BOARD_HEIGHT - object_size)))]

    def game_loop(self):
        game_exit = False
        game_over = False
        direction = "right"
        snake_block_size = 20
        snake_body = []
        snake_length = INITIAL_SNAKE_LENGTH
        start_position = [BOARD_WIDTH / 2, BOARD_HEIGHT / 2]  # x, y
        snake_head = start_position
        pos_change = [SPEED * snake_block_size, 0]  # start moving right, x speed = ...
        apple_size = 50
        apple_pos = self.random_pos(apple_size)

        # main game loop start
        while not game_exit:
            while game_over:
                self.game_display.fill(WHITE)
                self.message_to_screen("Game over", RED, "large", -100)
                self.message_to_screen("Score: %d" % (snake_length - INITIAL_SNAKE_LENGTH),
                                       BLACK, "medium", -20)
                self.message_to_screen("Press C to play again or Q to quit", BLACK, "medium", 100)
                pygame.display.update()
                self.clock.tick(FPS_NORMAL)
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
            if (snake_head[0] >= BOARD_WIDTH or snake_head[0] < 0 or 
                    snake_head[1] >= BOARD_HEIGHT or snake_head[1] < 0):
                game_over = True
            for snake_element in snake_body[:-1]:
                if snake_element == snake_head:
                    game_over = True
            if game_over:
                self.sound_punch.play()

            # eat apple
            if (((apple_pos[0] <= snake_head[0] < (apple_pos[0] + apple_size)) or 
                (apple_pos[0] <= snake_head[0] + snake_block_size < (apple_pos[0] + apple_size))) 
                    and 
                    ((apple_pos[1] <= snake_head[1] < (apple_pos[1] + apple_size)) or 
                     (apple_pos[1] <= snake_head[1] + snake_block_size < (apple_pos[1] + apple_size)))):
                apple_pos = self.random_pos(apple_size)
                snake_length += 1
                # TODO: don't place apples over the snake
                self.sound_apple.play()

            snake_body.append(snake_head.copy())
            if len(snake_body) > snake_length:
                del snake_body[0]

            # drawing stuff
            if not game_over:
                self.game_display.fill(WHITE)  # clean the game board
                #self.game_display.fill(RED, [apple_pos[0], apple_pos[1], apple_size, apple_size])
                self.game_display.blit(self.img_apple, [apple_pos[0], apple_pos[1]])
                self.snake_draw(snake_body, snake_block_size, direction)
                self.score_to_screen("%d" % (snake_length - INITIAL_SNAKE_LENGTH))
                pygame.display.update()  # frame done, render it

                self.clock.tick(FPS_NORMAL)  # don't change fps for difficulty, change movement speed
        # main game loop end

        pygame.quit()
        quit()
