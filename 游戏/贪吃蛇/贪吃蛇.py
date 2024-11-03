import pygame
import random
from pygame.locals import *
import time
from collections import deque

pygame.mixer.init()
pygame.mixer.music.load("Project_1.flac")
pygame.mixer.music.play(-1)

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("贪吃蛇")

colors = {
    "black": (0, 0, 0),
    "grad": (0, 255, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "pink": (255, 165, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "Sea": (0, 255, 255),
    "yellow": (255, 255, 0),
    "purple": (128, 0, 128),
    "orange": (255, 165, 0),
    "gray": (128, 128, 128),
    "brown": (165, 42, 42),
    "cyan": (0, 255, 255)
}

class SnakeGame:
    def __init__(self):
        self.snake_block = 10
        self.snake_speed = 15
        self.snake_list = []
        self.snake_length = 1
        self.x1 = screen_width / 2
        self.y1 = screen_height / 2
        self.x1_change = 0
        self.y1_change = 0
        self.foodx = round(random.randrange(0, screen_width - self.snake_block) / 10.0) * 10.0
        self.foody = round(random.randrange(0, screen_height - self.snake_block) / 10.0) * 10.0
        self.score = 0
        self.font_style = pygame.font.SysFont(None, 50)
        self.score_font = pygame.font.SysFont(None, 35)
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.game_close = False
    
    # def get_user_color(self):
    #     color = input("Enter the color of the snake: ")
    #     return colors[color]
    # def get_user_snake_speed(self):
    #     speed = input("Enter the speed of the snake: ")
    #     return int(speed)
    def show_score(self, color):
        score = self.score_font.render("--Score: " + str(self.score), True, color)
        screen.blit(score, [0, 0])

    def draw_snake(self):
        for x in self.snake_list:
            pygame.draw.rect(screen, colors["white"], [x[0], x[1], self.snake_block, self.snake_block])

    def game_over_message(self):
        my_msg = self.font_style.render("Game Over , Your Score is " + str(self.score) + "(^_^)", True, colors["white"])
        screen.blit(my_msg, [screen_width / 6, screen_height / 3])
        pygame.display.update()
        time.sleep(3)
        pygame.quit()
        quit()

    ##AI
    def get_ai_move(self):
        head = (self.x1 // self.snake_block, self.y1 // self.snake_block)
        food = (self.foodx // self.snake_block, self.foody // self.snake_block)
        queue = deque([head])
        visited = set()
        parent = {head: None}
        found = False
        
        while queue and not found:
            current = queue.popleft()
            if current == food:
                found = True
                break
            for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_pos = (current[0] + direction[0], current[1] + direction[1])
                if next_pos not in visited and 0 <= next_pos[0] < screen_width // self.snake_block and 0 <= next_pos[1] < screen_height // self.snake_block:
                    if next_pos not in [tuple(segment[:2]) for segment in self.snake_list]:
                        visited.add(next_pos)
                        parent[next_pos] = current
                        queue.append(next_pos)
        
        if found:
            path = []
            step = food
            while step != head:
                path.append(step)
                step = parent[step]
            path.reverse()
            if path:
                next_move = path[0]
                return (next_move[0] - head[0]) * self.snake_block, (next_move[1] - head[1]) * self.snake_block
        return self.x1_change, self.y1_change

    def main(self):
        while not self.game_over:
            while self.game_close:
                screen.fill(colors["black"])
                self.game_over_message()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.game_over = True
                            self.game_close = False
                        elif event.key == pygame.K_c:
                            self.__init__()
                            self.main()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.x1_change = -self.snake_block
                        self.y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        self.x1_change = self.snake_block
                        self.y1_change = 0
                    elif event.key == pygame.K_UP:
                        self.y1_change = -self.snake_block
                        self.x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        self.y1_change = self.snake_block
                        self.x1_change = 0

            if self.x1 >= screen_width or self.x1 < 0 or self.y1 >= screen_height or self.y1 < 0:
                self.game_close = True
            self.x1 += self.x1_change
            self.y1 += self.y1_change
            screen.fill(colors["black"])
            pygame.draw.rect(screen, colors["red"], [self.foodx, self.foody, self.snake_block, self.snake_block])
            self.snake_head = [self.x1, self.y1]
            self.snake_list.append(self.snake_head)
            if len(self.snake_list) > self.snake_length:
                del self.snake_list[0]
            for x in self.snake_list[:-1]:
                if x == self.snake_head:
                    self.game_close = True
            self.draw_snake()
            self.show_score(colors["white"])
            pygame.display.update()

            ##AI
            self.x1_change, self.y1_change = self.get_ai_move()

            if self.x1 == self.foodx and self.y1 == self.foody:
                self.foodx = round(random.randrange(0, screen_width - self.snake_block) / 10.0) * 10.0
                self.foody = round(random.randrange(0, screen_height - self.snake_block) / 10.0) * 10.0
                self.snake_length += 1
                self.score += 10
            self.clock.tick(self.snake_speed)
        pygame.quit()
        quit()

game = SnakeGame()
game.main()