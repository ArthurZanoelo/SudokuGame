import math
import pygame
from sudoku_generator import SudokuGenerator
from cell import Cell
from constants import *

class Board:
    def __init__(self, width: int, height: int, difficulty: str):
        """
        Initializes a Sudoku board.

        Parameters:
        - width (int): The width of the board.
        - height (int): The height of the board.
        - difficulty (str): The difficulty level of the Sudoku board ("easy", "medium", or "hard").
        """
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.difficulty = difficulty

        if self.difficulty == "easy":
            removed_cells = 30
        elif self.difficulty == "medium":
            removed_cells = 40
        elif self.difficulty == "hard":
            removed_cells = 50

        sudoku_board = SudokuGenerator(NUM_SQUARES**2, removed_cells)
        # Solve the board and make a copy
        sudoku_board.fill_values()
        self.solved_board = [row[:] for row in sudoku_board.get_board()]
        # Remove cells and make a copy
        sudoku_board.remove_cells()
        self.original_board = [row[:] for row in sudoku_board.get_board()]
        # Use the modified original_board for sudoku_numbers
        self.sudoku_numbers = sudoku_board.get_board()
        self.cells = [[Cell(self.sudoku_numbers[row][col], row, col, self.screen)
                       for col in range(NUM_SQUARES**2)]
                      for row in range(NUM_SQUARES**2)]
        self.clicked_cell = None

    def draw(self) -> None:
        """
        Draws the Sudoku board on the screen.
        """
        self.screen.fill(BACKGROUND_COLOR)
        # Draws the lines of the board
        if NUM_SQUARES != 0:
            for i in range(1, NUM_SQUARES):
                # Vertical lines
                pygame.draw.line(self.screen, LINE_COLOR,
                                 (i * self.width / (NUM_SQUARES), 0),
                                 (i * self.width / (NUM_SQUARES), self.height - MARGIN),
                                 LINE_WIDTH)
            for i in range(1, NUM_SQUARES + 1):  # +1 to account for the bottom line
                # Horizontal lines
                pygame.draw.line(self.screen, LINE_COLOR,
                                 (0, i * (self.height - MARGIN) / (NUM_SQUARES)),
                                 (self.width, i * (self.height - MARGIN) / (NUM_SQUARES)),
                                 LINE_WIDTH)

        # Draws the cells
        for row in self.cells:
            for cell in row:
                cell.draw()
                # Draws the selected cell red outline
                if self.clicked_cell is not None:
                    selected_row, selected_col = self.clicked_cell
                    pygame.draw.rect(self.screen, SELECTED_CELL_COLOR,
                                     (selected_col * cell.CELL_WIDTH,
                                      selected_row * cell.CELL_HEIGHT,
                                      cell.CELL_WIDTH, cell.CELL_HEIGHT), width=5)

        # Quit button
        quit_box = pygame.Rect(self.width/2 - 50, self.height/2 + 225, 100, 50)
        pygame.draw.rect(self.screen, TEXT_COLOR, quit_box)
        quit = BUTTON_FONT.render("Exit", True, BUTTON_COLOR)
        quit_rect = quit.get_rect()
        quit_rect.center = (self.width/2, self.height/2 + 250)
        self.screen.blit(quit, quit_rect)
        # Restart button
        restart_box = pygame.Rect(self.width/2 - 175, self.height/2 + 225, 100, 50)
        pygame.draw.rect(self.screen, TEXT_COLOR, restart_box)
        restart = BUTTON_FONT.render("Restart", True, BUTTON_COLOR)
        restart_rect = restart.get_rect()
        restart_rect.center = (self.width/2 - 125, self.height/2 + 250)
        self.screen.blit(restart, restart_rect)
        # Reset button
        reset_box = pygame.Rect(self.width/2 + 75, self.height/2 + 225, 100, 50)
        pygame.draw.rect(self.screen, TEXT_COLOR, reset_box)
        reset = BUTTON_FONT.render("Reset", True, BUTTON_COLOR)
        reset_rect = reset.get_rect()
        reset_rect.center = (self.width/2 + 125, self.height/2 + 250)
        self.screen.blit(reset, reset_rect)

        pygame.display.flip()  # Updates the screen

    def select(self, row: int, col: int) -> None:
        """
        Selects the cell at the given row and column.

        Parameters:
        - row (int): The row of the cell to select.
        - col (int): The column of the cell to select.
        """
        self.clicked_cell = (row, col)

    def click(self, x: float, y: float) -> tuple:
        """
        Converts screen coordinates to row and column indices.

        Parameters:
        - x (float): The x-coordinate of the mouse click.
        - y (float): The y-coordinate of the mouse click.

        Returns:
        - A tuple (row, col) representing the coordinates of the clicked cell.
          Returns None if the click is outside the board.
        """
        if 0 <= x <= self.width and 0 <= y <= self.height - MARGIN:
            row = math.floor(y / ((self.height - MARGIN) / NUM_SQUARES**2))
            col = math.floor(x / (self.width / NUM_SQUARES**2))
            return row, col
        else:
            return None

    def clear(self) -> None:
        """
        Clears the value of the selected cell.
        """
        if self.clicked_cell:
            row, col = self.clicked_cell
            self.cells[row][col].set_cell_value(0)
            self.cells[row][col].set_sketched_value(0)

    def sketch(self, value: int) -> None:
        """
        Sketches the given value in the selected cell.

        Parameters:
        - value (int): The value to sketch.
        """
        if self.clicked_cell:
            row, col = self.clicked_cell
            self.cells[row][col].set_sketched_value(value)

    def place_number(self, value: int) -> None:
        """
        Sets the value of the selected cell to the sketched value.

        Parameters:
        - value (int): The value to place in the selected cell.
        """
        if self.clicked_cell:
            row, col = self.clicked_cell
            if self.cells[row][col].sketched_value != 0:
                self.cells[row][col].set_cell_value(self.cells[row][col].sketched_value)
            else:
                self.cells[row][col].set_cell_value(value)

    def reset_to_original(self) -> None:
        """
        Resets the board to its original cell values.
        """
        self.cells = [[Cell(self.original_board[row][col], row, col, self.screen)
                       for col in range(NUM_SQUARES**2)]
                      for row in range(NUM_SQUARES**2)]
        # Update self.sudoku_numbers with the values from the new cells
        self.update_board()

    def is_full(self) -> bool:
        """
        Returns a Boolean value indicating whether the board is full or not.

        Returns:
        - True if the board is full, False otherwise.
        """
        return not bool(self.find_empty())

    def update_board(self) -> None:
        """
        Updates the sudoku_numbers with the values in self.cells.
        """
        for row in range(NUM_SQUARES**2):
            for col in range(NUM_SQUARES**2):
                self.sudoku_numbers[row][col] = self.cells[row][col].value

    def find_empty(self) -> tuple:
        """
        Finds an empty cell and returns its row and column as a tuple (row, col).

        Returns:
        - A tuple (row, col) representing the coordinates of an empty cell.
          Returns None if no empty cell is found.
        """
        for row in range(NUM_SQUARES**2):
            for col in range(NUM_SQUARES**2):
                if self.cells[row][col].value == 0:
                    return row, col
        return None

    def check_board(self) -> bool:
        """
        Checks if the current board is the same as the original board.

        Returns:
        - True if the boards are the same, False otherwise.
        """
        return self.sudoku_numbers == self.solved_board

    def move_with_arrow_keys(self, direction: tuple) -> None:
        """
        Moves the selection with arrow keys.

        Parameters:
        - direction (tuple): A tuple (delta_row, delta_col) indicating the direction of movement.
        """
        if self.clicked_cell:
            row, col = self.clicked_cell
            # Modulo to wrap around the board from bottom to top and right to left
            new_row = (row + direction[0]) % NUM_SQUARES**2
            new_col = (col + direction[1]) % NUM_SQUARES**2
            self.select(new_row, new_col)
