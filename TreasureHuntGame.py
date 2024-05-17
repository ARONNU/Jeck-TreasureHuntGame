import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 100

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Treasure Hunt Game")

class TreasureHuntGame:
    def __init__(self, size=5):
        self.size = size
        self.attempts = 10
        self.font = pygame.font.Font(None, 36)
        self.generate_map()
        self.player_row = random.randint(0, self.size - 1)
        self.player_col = random.randint(0, self.size - 1)
        
        # Calculate offsets to center the grid
        self.offset_x = (SCREEN_WIDTH - self.size * TILE_SIZE) // 2
        self.offset_y = (SCREEN_HEIGHT - self.size * TILE_SIZE) // 2

    def generate_map(self):
        self.target_row = random.randint(0, self.size - 1)
        self.target_col = random.randint(0, self.size - 1)

    def display_map(self):
        screen.fill(WHITE)
        for i in range(self.size):
            for j in range(self.size):
                x1, y1 = j * TILE_SIZE + self.offset_x, i * TILE_SIZE + self.offset_y
                x2, y2 = x1 + TILE_SIZE, y1 + TILE_SIZE
                if i == self.target_row and j == self.target_col:
                    pygame.draw.rect(screen, YELLOW, (x1, y1, TILE_SIZE, TILE_SIZE))
                elif i == self.player_row and j == self.player_col:
                    pygame.draw.rect(screen, BLUE, (x1, y1, TILE_SIZE, TILE_SIZE))
                else:
                    pygame.draw.rect(screen, BLACK, (x1, y1, TILE_SIZE, TILE_SIZE), 1)

        self.display_text()

    def display_text(self):
        text = f"Attempts left: {self.attempts}"
        text_surface = self.font.render(text, True, BLACK)
        screen.blit(text_surface, (10, SCREEN_HEIGHT - 40))

    def move_player(self, direction):
        if direction == "w":
            self.player_row = max(0, self.player_row - 1)
        elif direction == "s":
            self.player_row = min(self.size - 1, self.player_row + 1)
        elif direction == "a":
            self.player_col = max(0, self.player_col - 1)
        elif direction == "d":
            self.player_col = min(self.size - 1, self.player_col + 1)
        self.display_map()
        self.check_for_treasure()

    def check_for_treasure(self):
        if self.player_row == self.target_row and self.player_col == self.target_col:
            self.attempts = 10  # Reset attempts for the new round
            self.generate_map()  # Generate a new map for the next round
            self.player_row = random.randint(0, self.size - 1)  # Move player to a random position
            self.player_col = random.randint(0, self.size - 1)
            self.display_map()
        else:
            self.attempts -= 1
            if self.attempts == 0:
                distance_row = self.secant_method(self.player_row, self.target_row, self.player_col)
                distance_col = self.secant_method(self.player_col, self.target_col, self.player_row)
                self.game_over(f"Game over! The treasure was at row {self.target_row} and column {self.target_col}.\nApproximate distance: {round(distance_row + distance_col)}")
            else:
                self.display_map()

    def secant_method(self, guess1, guess2, target):
        while abs(guess1 - guess2) > 0.01:
            next_guess = guess2 - ((guess2 - guess1) / max(0.01, (self.evaluate(guess2, target) - self.evaluate(guess1, target)))) * self.evaluate(guess2, target)
            guess1, guess2 = guess2, next_guess
        return round(guess2) if not math.isnan(guess2) else 0

    def evaluate(self, position, target):
        return abs(position - target) + 0.01

    def game_over(self, message):
        screen.fill(WHITE)
        text_surface = self.font.render(message, True, BLACK)
        screen.blit(text_surface, (10, SCREEN_HEIGHT / 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        exit()

def run_game():
    game = TreasureHuntGame()
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    game.move_player("w")
                elif event.key == pygame.K_s:
                    game.move_player("s")
                elif event.key == pygame.K_a:
                    game.move_player("a")
                elif event.key == pygame.K_d:
                    game.move_player("d")

        game.display_map()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
