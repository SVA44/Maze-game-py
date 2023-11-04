# cell.py
import pygame
from random import choice

class Cell:
    def __init__(self, x, y, thickness):
        self.x, self.y = x,y
        self.thickness = thickness
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    # draw grid cell walls
    def draw(self, sc, tile):
        x, y = self.x * tile, self.y * tile
        if self['top']:
            pygame.draw.line(sc, pygame.Color('darkgreen'), (x, y), (x + tile, y), self.thickness)
        if self['right']:
            pygame.draw.line(sc, pygame.Color('darkgreen'), (x + tile, y), (x + tile, y + tile), self.thickness)    
        if self['bottom']:
            pygame.draw.line(sc, pygame.Color('darkgreen'), (x + tile, y + tile),(x, y + tile), self.thickness)
        if self['left']:
            pygame.draw.line(sc, pygame.Color('darkgreen'), (x, y + tile), (x, y), self.thickness)