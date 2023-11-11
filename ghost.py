# ghost.py
import pygame
import math
import random

class Ghost:
    def __init__(self, x, y, clock):
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
        self.current_direction = random.choice(['right','left','top','bottom'])
        self.prev_direction = self.current_direction
        self.turn_timer = 0
        self.turn = False
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

    # collide with player
    def collide_player(self, player_loc):
        self.loc = [self.x, self.y]
        return self.distance(self.loc, player_loc) < self.player_size + 4
    
    # get opposite direction
    def opposite_move(self, direction):
        opposites = {'right': 'left', 'left':'right','top':'bottom', 'bottom': 'top'}
        return opposites[direction]
    
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


        if move == "left":
            if current_cell.walls['left']:
                
                if self.x <= current_cell_abs_x + thickness:
                    return False
        if move == "right":
            if current_cell.walls['right']:
                
                if self.x >= current_cell_abs_x + tile -(self.player_size + thickness):
                    return False 
        if move == "top":
            if current_cell.walls['top']:
                
                if self.y <= current_cell_abs_y + thickness:
                    return False
        if move == "bottom":
            if current_cell.walls['bottom']:
                
                if self.y >= current_cell_abs_y + tile - (self.player_size + thickness):
                    return False
        
        return True
    # check if ghost is within central of cell
    def central_cell(self, tile, grid_cells, thickness):
        current_cell_x, current_cell_y = self.x // tile, self.y // tile
        current_cell_abs_x, current_cell_abs_y = current_cell_x * tile, current_cell_y * tile

        if self.x <= current_cell_abs_x :
            return False
        if self.x >= current_cell_abs_x + tile -(self.player_size):
            return False
        if self.y <= current_cell_abs_y :
            return False
        if self.y >= current_cell_abs_y + tile - (self.player_size):
            return False
        return True

    
    
    # updates ghost position while moving
    def update(self, tile, grid_cells, thickness):
        self.velX = 0
        self.velY = 0
        possible_moves = self.availableMoves(tile, grid_cells, thickness)
        # check if move is valid, if not then stop moving
        if (not self.check_move(tile, grid_cells, thickness,self.current_direction)):
            self.prev_direction = self.current_direction
            self.current_direction = "stop"
        # after stop moving, change direction to valid ones
        if self.current_direction == "stop":
            if len(possible_moves) == 1:
                self.current_direction = possible_moves[0]
            else:
                if (self.opposite_move(self.prev_direction) in possible_moves):
                    possible_moves.remove(self.opposite_move(self.prev_direction))
                self.current_direction = random.choice(possible_moves)

        # if move to a cell that has more than 2 exits, consider changing direction
        if len(possible_moves) > 2: 
            if self.central_cell(tile, grid_cells, thickness):
                self.prev_direction = self.current_direction
                self.current_direction = "redirecting"
        # redirect direction so that 60% move in a new direction and prevent doing a 180
        if self.current_direction == "redirecting":
            if (self.opposite_move(self.prev_direction) in possible_moves):
                possible_moves.remove(self.opposite_move(self.prev_direction))
            if self.prev_direction in possible_moves:
                if random.randrange(0,100) <= 60:
                    possible_moves.remove(self.prev_direction)
                    self.current_direction = random.choice(possible_moves)
                else:
                    self.current_direction = self.prev_direction
            else:
                    self.current_direction = random.choice(possible_moves)
        
        
            
            
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
