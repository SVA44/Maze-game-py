# coin.py
import pygame
import math

class Coin:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.coin_size = 7.5
        self.rect = pygame.Rect(self.x, self.y, self.coin_size, self.coin_size)
        self.color = (255, 191, 0)

    # calculate distance between 2 positions
    def distance(self, a_pos, b_pos):
        a = pow(abs(a_pos[0] - b_pos[0]), 2)
        b = pow(abs(a_pos[1] - b_pos[1]), 2)
        return math.sqrt(a + b)
    
    # collide with coin
    def collide_player(self, player_loc):
        self.loc = [self.x, self.y]
        return self.distance(self.loc, player_loc) < self.coin_size + 4
    
    # drawing coin to the screen 
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)