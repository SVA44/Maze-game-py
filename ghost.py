# ghost.py
import pygame
import math
import random

class Ghost:
    def __init__(self, x, y, player_x, player_y, clock):
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
        self.speed = 1
        self.player_loc = [player_x, player_y]
        self.current_direction = random.choice(['right','left','top','bottom'])
        self.new_direction = self.current_direction
        self.turn_timer = 0
        self.turn_flag = False
        self.clock = clock

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
    # detect player presence
    def saw_player(self):
        return

    @property
    # get opposite direction
    def opposite_move(self):
        opposites = {'right': 'left', 'left':'right','top':'bottom', 'bottom': 'top'}
        return opposites[self.current_direction]
    
    # list all possible moves
    def availableMoves(self, tile, grid_cells, thickness):
        current_cell_x, current_cell_y = self.x // tile, self.y // tile
        current_cell = self.get_current_cell(current_cell_x, current_cell_y, grid_cells)
        f = lambda move:self.check_move(tile, grid_cells,thickness, move)
        possible_directions = list(filter(f, current_cell.exits))
        return possible_directions
    
    # verify ghost move
    def check_move(self, tile, grid_cells, thickness, move):
        current_cell_x, current_cell_y = self.x // tile, self.y // tile
        current_cell = self.get_current_cell(current_cell_x, current_cell_y, grid_cells)
        current_cell_abs_x, current_cell_abs_y = current_cell_x * tile, current_cell_y * tile

        player_cell_x , player_cell_y = self.player_loc[0] // tile, self.player_loc[1] // tile
        player_cell = self.get_current_cell(player_cell_x, player_cell_y, grid_cells)

        if move == "left":
            if current_cell.walls['left']:
                if player_cell != current_cell:
                    return False
                if self.x <= current_cell_abs_x + thickness:
                    return False
        if move == "right":
            if current_cell.walls['right']:
                if player_cell != current_cell:
                    return False
                if self.x >= current_cell_abs_x + tile -(self.player_size + thickness):
                    return False 
        if move == "top":
            if current_cell.walls['top']:
                if player_cell != current_cell:
                    return False
                if self.y <= current_cell_abs_y + thickness:
                    return False
        if move == "bottom":
            if current_cell.walls['bottom']:
                if player_cell != current_cell:
                    return False
                if self.y >= current_cell_abs_y + tile - (self.player_size + thickness):
                    return False
        return True
    
    # change direction of the ghost
    def change_direction(self, tile, grid_cells, thickness):
        current_cell_x, current_cell_y = self.x // tile, self.y // tile
        current_cell = self.get_current_cell(current_cell_x, current_cell_y, grid_cells)
        f = lambda move:self.check_move(tile, grid_cells,thickness, move)
        possible_directions = list(filter(f, current_cell.exits))
        change_direction = random.choice(possible_directions)
        self.turn_timer = self.clock.elapsed_time
        return change_direction
    
    # updates ghost position while moving
    def update(self, tile, grid_cells, thickness):
        self.velX = 0
        self.velY = 0
        moves = self.availableMoves(tile, grid_cells,thickness * 4)
        opposite = self.opposite_move
        if ( self.current_direction in moves and ( len(moves) == 1 or random.randrange( 0,1000 ) <= 999.9 ) ):
            pass
        elif ( self.current_direction not in moves and len(moves) == 1 ):
            self.new_direction = moves[0]   # maybe u-turn
            self.turn_flag = True
        else:  # more than 1 exit
            if (opposite in moves):
                moves.remove(opposite)
            self.new_direction = random.choice(moves)
            self.turn_flag = True
        
        if self.turn_flag and self.clock.elapsed_time - self.turn_timer >= 0:
            self.turn_timer = self.clock.elapsed_time
            self.turn_flag = False
            self.current_direction = self.new_direction
            
        if self.current_direction == "left":
            self.velX = -self.speed
        if self.current_direction == "right":
            self.velX = self.speed
        if self.current_direction == "top":
            self.velY = -self.speed
        if self.current_direction == "bottom":
            self.velY = self.speed
        self.x += self.velX
        self.y += self.velY  
        self.rect = pygame.Rect(int(self.x), int(self.y), self.player_size, self.player_size)
