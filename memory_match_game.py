import pygame
import random
import sys

# initialize pygame
pygame.init()

# game settings
GRID_SIZE = 4  # fixed grid size (4x4)
CARD_SIZE = 100  # default card size

# colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# set up display in fullscreen 
screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

# set up font
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 36)

def generate_grid(grid_size):
    """generates the card grid with shuffled pairs."""
    values = list(range(1, (grid_size * grid_size // 2) + 1)) * 2
    random.shuffle(values)
    cards = []
    for row in range(grid_size):
        card_row = []
        for col in range(grid_size):
            card_row.append(values.pop())
        cards.append(card_row)
    return cards

def draw_start_screen():
    """displays the start screen."""
    window.fill(WHITE)
    title = font.render("Memory Match Game", True, BLUE)
    start_message = small_font.render("Press '1' to Start", True, BLACK)

    window.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
    window.blit(start_message, (WIDTH // 2 - start_message.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

def game_loop():
    """main game loop."""
    cards = generate_grid(GRID_SIZE)
    GRID_WIDTH = GRID_SIZE * CARD_SIZE
    GRID_HEIGHT = GRID_SIZE * CARD_SIZE
    OFFSET_X = (WIDTH - GRID_WIDTH) // 2
    OFFSET_Y = (HEIGHT - GRID_HEIGHT) // 2

    flipped = []
    matches = []
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = (x - OFFSET_X) // CARD_SIZE
                row = (y - OFFSET_Y) // CARD_SIZE
                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                    if (row, col) not in flipped and (row, col) not in matches:
                        flipped.append((row, col))

                        if len(flipped) == 2:
                            (row1, col1), (row2, col2) = flipped
                            if cards[row1][col1] == cards[row2][col2]:
                                matches.extend(flipped)
                            pygame.time.wait(500)
                            flipped.clear()

        # draw background
        window.fill(WHITE)

        # draw cards
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = OFFSET_X + col * CARD_SIZE
                y = OFFSET_Y + row * CARD_SIZE
                rect = pygame.Rect(x + 10, y + 10, CARD_SIZE - 20, CARD_SIZE - 20)

                if (row, col) in flipped or (row, col) in matches:
                    pygame.draw.rect(window, GREEN, rect)
                    value_text = font.render(str(cards[row][col]), True, BLACK)
                    text_rect = value_text.get_rect(center=rect.center)
                    window.blit(value_text, text_rect)
                else:
                    pygame.draw.rect(window, GRAY, rect)

        # check win condition
        if len(matches) == GRID_SIZE * GRID_SIZE:
            win_text = font.render("You Win!", True, BLUE)
            restart_message = small_font.render("Press 'R' to Restart or 'Q' to Quit", True, BLACK)

            # position the win text at the center
            window.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, OFFSET_Y + GRID_HEIGHT + 20))

            # position the restart message below the grid
            window.blit(restart_message, (WIDTH // 2 - restart_message.get_width() // 2, OFFSET_Y + GRID_HEIGHT + 70))

            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            waiting = False  # restart the game
                            return
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()

        pygame.display.flip()

def main():
    """main function to run the game."""
    while True:
        draw_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_loop()

main()
