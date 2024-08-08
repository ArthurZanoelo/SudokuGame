import pygame
import sys
from board import Board
from constants import *

pygame.init()

def display_image(screen, image_path: str, width: int, height: int) -> None:
    """
    Display an image on the screen.

    Args:
        screen (pygame.Surface): The game screen.
        image_path (str): Path to the image file.
        width (int): Width to scale the image.
        height (int): Height to scale the image.
    """
    background_image = pygame.image.load(image_path)
    scaled_image = pygame.transform.scale(background_image, (width, height))
    screen.blit(scaled_image, (0, 0))
    pygame.display.flip()

def start_menu(screen: pygame.Surface) -> str:
    """
    Display the start menu and return the selected difficulty.

    Args:
        screen (pygame.Surface): The game screen.

    Returns:
        str: Selected difficulty ("easy", "medium", or "hard").
    """
    display_image(screen, 'sudoku_img.jpg', 600, 600)
    # Top black box
    title_text_box = pygame.Rect(200, 100, 200, 70)
    pygame.draw.rect(screen, 'Black', title_text_box)
    title_text_font = pygame.font.Font(None, 70)
    title_text = title_text_font.render('Sudoku', False, 'White')
    title_text_rect = title_text.get_rect(center=title_text_box.center)
    # Middle black box
    start_text_font = pygame.font.Font(None, 50)
    start_text_box = pygame.Rect(125, 350, 350, 50)
    pygame.draw.rect(screen, 'Black', start_text_box)
    start_text = start_text_font.render('Select Game Mode:', False, 'White')
    start_text_rect = start_text.get_rect(center=start_text_box.center)

    # Difficulty buttons
    button_width, button_height = 130, 50
    button_spacing = (screen.get_width() - 3 * button_width) / 4
    easy_button = pygame.Rect(button_spacing, 500, button_width, button_height)
    medium_button = pygame.Rect(2 * button_spacing + button_width, 500, button_width, button_height)
    hard_button = pygame.Rect(3 * button_spacing + 2 * button_width, 500, button_width, button_height)

    start_menu = True
    difficulty = None
    while start_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if easy_button.collidepoint(x, y):
                    difficulty = "easy"
                    start_menu = False
                elif medium_button.collidepoint(x, y):
                    difficulty = "medium"
                    start_menu = False
                elif hard_button.collidepoint(x, y):
                    difficulty = "hard"
                    start_menu = False
                    
        # Draw the text and buttons
        screen.blit(title_text, title_text_rect)
        screen.blit(start_text, start_text_rect)
        pygame.draw.rect(screen, 'Black', easy_button)
        pygame.draw.rect(screen, 'Black', medium_button)
        pygame.draw.rect(screen, 'Black', hard_button)

        easy_text = start_text_font.render('Easy', False, 'White')
        easy_text_rect = easy_text.get_rect(center=easy_button.center)
        screen.blit(easy_text, easy_text_rect)
        
        medium_text = start_text_font.render('Medium', False, 'White')
        medium_text_rect = medium_text.get_rect(center=medium_button.center)
        screen.blit(medium_text, medium_text_rect)
        
        hard_text = start_text_font.render('Hard', False, 'White')
        hard_text_rect = hard_text.get_rect(center=hard_button.center)
        screen.blit(hard_text, hard_text_rect)

        pygame.display.flip()

    return difficulty

def display_game_over(screen: pygame.Surface, width: int, height: int) -> None:
    """
    Display the game over screen.

    Args:
        screen (pygame.Surface): The game screen.
        width (int): Width of the screen.
        height (int): Height of the screen.
    """
    display_image(screen, 'sudoku_img.jpg', 600, 600)
    
    game_over_text_font = pygame.font.Font(None, 70)
    game_over_text = game_over_text_font.render('Game Over', False, 'Red')
    game_over_rect = game_over_text.get_rect(center=(width / 2, height / 2))
    screen.blit(game_over_text, game_over_rect)

    restart_button = pygame.Rect(width / 2 - 50, height / 2 + 50, 100, 50)
    pygame.draw.rect(screen, 'Black', restart_button)
    restart_text_font = pygame.font.Font(None, 30)
    restart_text = restart_text_font.render('Restart', False, 'White')
    restart_text_rect = restart_text.get_rect(center=restart_button.center)
    screen.blit(restart_text, restart_text_rect)

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if restart_button.collidepoint(x, y):
                    waiting_for_input = False
                    main() # Restart the program


def display_game_won(screen: pygame.Surface, width: int, height: int) -> None:
    """
    Display the game won screen.

    Args:
        screen (pygame.Surface): The game screen.
        width (int): Width of the screen.
        height (int): Height of the screen.
    """
    display_image(screen, 'sudoku_img.jpg', 600, 600)
    
    game_won_text_font = pygame.font.Font(None, 70)
    game_won_text = game_won_text_font.render('You Won!', False, 'Green')
    game_won_rect = game_won_text.get_rect(center=(width / 2, height / 2))
    screen.blit(game_won_text, game_won_rect)

    exit_button = pygame.Rect(width / 2 - 50, height / 2 + 50, 100, 50)
    pygame.draw.rect(screen, 'Black', exit_button)
    exit_text_font = pygame.font.Font(None, 30)
    exit_text = exit_text_font.render('Exit', False, 'White')
    exit_text_rect = exit_text.get_rect(center=exit_button.center)
    screen.blit(exit_text, exit_text_rect)

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if exit_button.collidepoint(x, y):
                    sys.exit()

def main():
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption('Sudoku')

    difficulty = start_menu(screen)
    if difficulty is None:
        sys.exit()

    board = Board(600, 600, difficulty)
    running = True
    game_over = False
    game_won = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    x, y = pygame.mouse.get_pos()
                    clicked_cell = board.click(x, y)
                    if clicked_cell:
                        board.select(clicked_cell[0], clicked_cell[1])
                    # Check for button clicks
                    quit_box = pygame.Rect(board.width / 2 - 50, board.height / 2 + 225, 100, 50)
                    if quit_box.collidepoint(x, y):
                        sys.exit()
                    reset_box = pygame.Rect(board.width / 2 + 75, board.height / 2 + 225, 100, 50)
                    if reset_box.collidepoint(x, y):
                        board.reset_to_original()
                    restart_box = pygame.Rect(board.width / 2 - 175, board.height / 2 + 225, 100, 50)
                    if restart_box.collidepoint(x, y):
                        running = False
                        main() # Restart the program
                            
            elif event.type == pygame.KEYDOWN:
                # Sketch the number in the cell
                if pygame.K_1 <= event.key <= pygame.K_9:
                    number_pressed = int(pygame.key.name(event.key))
                    board.sketch(number_pressed)
                elif event.key == pygame.K_RETURN:  # lock in the number
                    row, col = board.clicked_cell
                    if board.cells[row][col].number_pressed:
                        board.place_number(number_pressed)
                        board.update_board() # Update the 2D array sudoku_numbers
                # Delete the number in the cell with the delete key
                elif event.key == pygame.K_DELETE:
                    board.clear()
                # Arrow key movement around the board
                elif event.key == pygame.K_UP:
                    board.move_with_arrow_keys((-1, 0))
                elif event.key == pygame.K_DOWN:
                    board.move_with_arrow_keys((1, 0))
                elif event.key == pygame.K_LEFT:
                    board.move_with_arrow_keys((0, -1))
                elif event.key == pygame.K_RIGHT:
                    board.move_with_arrow_keys((0, 1))

        # Game States
        if board.check_board():
            display_game_won(screen, board.width, board.height)
            game_won = True

        if board.is_full() and not board.check_board():
            display_game_over(screen, board.width, board.height)
            game_over = True
            
        if not game_over and not game_won:
            board.draw()
            pygame.display.flip()

if __name__ == "__main__":
    main()