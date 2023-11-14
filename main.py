# main.py

import pygame, sys, os
from maze import Maze
from player import Player
from clock import Clock
from game import Game
from ghost import Ghost
from coin import Coin

pygame.init()
pygame.font.init()
pygame.mixer.init() # add sound

# Sounds dir
s = 'sound'

# Background music
music = pygame.mixer.music.load(os.path.join(s, 'arcade_wave.mp3'))

# Complete maze congratulation music
congrads = pygame.mixer.Sound(os.path.join(s, 'fantasy_success.wav'))

# Coin grabbing sound
coin_collecting = pygame.mixer.Sound(os.path.join(s, 'coin_collecting.wav'))
class Main():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("impact", 30)
        self.message_color = pygame.Color("cyan")
        self.running = True
        self.score = 0
        self.game_over = False
        self.ghost_collision = False
        self.result = "Win"
        self.FPS = pygame.time.Clock()
    
    def instructions(self):
        instructions1 = self.font.render('Use', True, self.message_color)
        instructions2 = self.font.render('Arrow Keys', True, self.message_color)
        instructions3 = self.font.render('to Move', True, self.message_color)
        self.screen.blit(instructions1,(655,300))
        self.screen.blit(instructions2,(610,331))
        self.screen.blit(instructions3,(630,362))

    # draws all configs; maze, player, instructions, and time
    def _draw(self, maze, tile, player, ghost, game, clock, coins):
        # draw maze
        [cell.draw(self.screen, tile) for cell in maze.grid_cells]
        # add a goal point to reach
        game.add_goal_point(self.screen)
        # draw every player movement
        player.draw(self.screen)
        player.update()
        # draw ghost movement
        ghost.draw(self.screen)
        ghost.update(tile, maze.grid_cells, maze.thickness)
        # draw coins
        for coin in coins:
            coin.draw(self.screen) 
        # instructions, clock, winning message
        self.instructions()
        if self.game_over:
            clock.stop_timer()
            self.screen.blit(game.message(self.result),(610,120))
        else:
            clock.update_timer()
        # display current score
        self.screen.blit(self.font.render("Score: " + str(self.score), True, self.message_color), (620,240))
        # display timer
        self.screen.blit(clock.display_timer(), (625,200))
        pygame.display.flip()
    
    # main game loop
    def main(self, frame_size, tile):
        cols, rows = frame_size[0] // tile, frame_size[-1] // tile
        maze = Maze(cols, rows)
        game = Game(maze.grid_cells[-1], tile)
        player = Player(tile // 3, tile // 3)
        coins = []
        for cell in maze.grid_cells:
            coin_cell = Coin(cell.x * tile + 5 * tile // 12, cell.y * tile + 5 * tile // 12)
            coins.append(coin_cell)
        clock = Clock()
        ghost = Ghost(tile // 3, -2 * tile // 3 + (frame_size[0] // tile) * tile, clock)
        maze.generate_maze()
        clock.start_timer()
        pygame.mixer.music.play(-1)
        while self.running:
            self.screen.fill("gray")
            self.screen.fill( pygame.Color("darkslategray"), (603, 0, 752, 752))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # if keys were pressed still
            if event.type == pygame.KEYDOWN:
                if not self.game_over:
                    if event.key == pygame.K_LEFT:
                        player.left_pressed = True
                    if event.key == pygame.K_RIGHT:
                        player.right_pressed = True
                    if event.key == pygame.K_UP:
                        player.up_pressed = True
                    if event.key == pygame.K_DOWN:
                        player.down_pressed = True
                    player.check_move(tile, maze.grid_cells, maze.thickness)
            # if pressed key released
            if event.type == pygame.KEYUP:
                if not self.game_over:
                    if event.key == pygame.K_LEFT:
                        player.left_pressed = False
                    if event.key == pygame.K_RIGHT:
                        player.right_pressed = False
                    if event.key == pygame.K_UP:
                        player.up_pressed = False
                    if event.key == pygame.K_DOWN:
                        player.down_pressed = False
                    player.check_move(tile, maze.grid_cells, maze.thickness)
            player_loc = [player.x, player.y]
            
            # detect player collision and trigger a lose game
            if (ghost.collide_player(player_loc)):
                self.ghost_collision = True
                self.result = "Lose"
            
            # detect coin collection and trigger a sound
            coin_grabbed = None
            for coin in coins:
                if coin.collide_player(player_loc):
                    pygame.mixer.Sound.play(coin_collecting)
                    coin_grabbed = coin
            if coin_grabbed:
                self.score += 10
                coins.remove(coin_grabbed)
            if game.is_game_over(player, self.ghost_collision):
                # played only once right after the player complete the game
                if self.game_over is False:
                    pygame.mixer.Sound.play(congrads)
                    self.game_over = True
                    # stop all player movement
                    player.left_pressed = False
                    player.right_pressed = False
                    player.up_pressed = False
                    player.down_pressed = False
                    # stop all ghost movement
                    ghost.current_direction = None
            self._draw(maze, tile, player, ghost, game, clock, coins)
            self.FPS.tick(60)                                   

if __name__ == "__main__":
    window_size = (602, 602)
    screen = (window_size[0] + 150, window_size[-1])
    tile_size = 30
    screen = pygame.display.set_mode(screen)
    pygame.display.set_caption("Maze")

    game = Main(screen)
    game.main(window_size, tile_size)
    