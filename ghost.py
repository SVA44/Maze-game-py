# ghost.py
import pygame
import math
import random

class Ghost:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.player_size = 10
        self.rect = pygame.Rect(self.x, self.y, self.player_size, self.player_size)
        self.color = (198, 40, 40)
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.velX = 0
        self.velY = 0
        self.speed = 4

    # get current cell position of the ghost
    def get_current_cell(self, x, y, grid_cells):
        for cell in grid_cells:
            if cell.x == x and cell.y == y:
                return cell
    
    # drawing ghost to the screen 
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
    
    # calculate distance between 2 positions
    def distance(self, a_pos, b_pos):
        a = pow(abs(a_pos[0] - b_pos[0]), 2)
        b = pow(abs(a_pos[1] - b_pos[1]), 2)
        return math.sqrt(a + b)
    
    # finds shortest path to target position without going through walls
    def next_move(self, tile, grid_cells, thickness, target):
        current_cell_x, current_cell_y = self.x // tile, self.y // tile
        current_cell = self.get_current_cell(current_cell_x, current_cell_y, grid_cells)
        current_cell_abs_x, current_cell_abs_y = current_cell_x * tile, current_cell_y * tile
        current_move = None
        closest_distance = math.inf

        # check left path
        left_pos = [self.x - self.speed, self.y]
        if (current_cell.walls['left'] == False) or (self.x > current_cell_abs_x + thickness):
            current_distance = self.distance(target, left_pos)
            if closest_distance > current_distance:
                closest_distance = current_distance
                current_move = "left"
        

       # check right path
        right_pos = [self.x + self.speed, self.y]
        if (current_cell.walls['right'] == False) or (self.x < current_cell_abs_x + tile -(self.player_size + thickness)):
            current_distance = self.distance(target, right_pos)
            if closest_distance > current_distance:
                closest_distance = current_distance
                current_move = "right"

        # check top path
        top_pos = [self.x, self.y - self.speed]
        if (current_cell.walls['top'] == False) or (self.y > current_cell_abs_y + thickness):
            current_distance = self.distance(target, top_pos)
            if closest_distance > current_distance:
                closest_distance = current_distance
                current_move = "top"
        
        # check down path
        down_pos = [self.x, self.y + self.speed]
        if (current_cell.walls['bottom'] == False) or (self.y < current_cell_abs_y + tile - (self.player_size + thickness)):
            current_distance = self.distance(target, down_pos)
            if closest_distance > current_distance:
                closest_distance = current_distance
                current_move = "down"
        return current_move
    
    
    # updates ghost position while moving
    def update(self, next_move):
        self.velX = 0
        self.velY = 0
        if next_move == "left":
            self.velX = -self.speed
        if next_move == "right":
            self.velX = self.speed
        if next_move == "top":
            self.velY = -self.speed
        if next_move == "down":
            self.velY = self.speed
        self.x += self.velX
        self.y += self.velY  
        self.rect = pygame.Rect(int(self.x), int(self.y), self.player_size, self.player_size)
