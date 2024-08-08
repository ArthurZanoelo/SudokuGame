import pygame
from constants import NUM_SQUARES, MARGIN, NUM_FONT

class Cell:
    """
    Class to represent a cell on the Sudoku board.
    
    Attributes:
    - value (int): The value of the cell.
    - row (int): The row of the cell.
    - col (int): The column of the cell.
    - screen (pygame.Surface): The screen to draw the cell on.
    - sketched_value (int): The sketched value in the cell.
    - CELL_WIDTH (float): The width of the cell.
    - CELL_HEIGHT (float): The height of the cell.
    - number_pressed (bool): Indicates whether a number is pressed in the cell.
    - is_editable (bool): Indicates whether the cell is editable (initially empty).
    """

    def __init__(self, value: int, row: int, col: int, screen: pygame.Surface) -> None:
        """Initialize a cell with the given value, row, column, and screen."""
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched_value: int = 0
        self.CELL_WIDTH: float = (self.screen.get_width() / NUM_SQUARES ** 2)
        self.CELL_HEIGHT: float = ((self.screen.get_height() - MARGIN) / NUM_SQUARES ** 2)
        self.number_pressed: bool = False
        self.is_editable: bool = value == 0

    def set_cell_value(self, value: int) -> None:
        """Set the value of the cell if it is editable."""
        if self.is_editable:
            self.value = value

    def set_sketched_value(self, value: int) -> None:
        """Set the sketched value in the cell."""
        self.sketched_value = value

    def draw(self) -> None:
        """Draw the cell on the screen."""
        # Create a rectangle representing the cell
        self.cell_rect = pygame.Rect(self.col * self.CELL_WIDTH, self.row * self.CELL_HEIGHT,
                                     self.CELL_WIDTH + 1, self.CELL_HEIGHT + 1)
        pygame.draw.rect(self.screen, 'Black', self.cell_rect, 1)

        # Draw the value or sketched value in the cell
        if self.value != 0:
            if self.is_editable:
                self.draw_number('Orange', self.CELL_HEIGHT / 2, self.CELL_WIDTH / 4)
            else:
                self.draw_number('Black', self.CELL_HEIGHT / 2, self.CELL_WIDTH / 4)
        elif self.sketched_value != 0:
            self.draw_number('Gray', self.CELL_HEIGHT / 10, self.CELL_WIDTH / 10)

    def draw_number(self, color: str, height_offset: float, width_offset: float) -> None:
        """Draw the number or sketched number with the specified color and offsets."""
        num_surf = NUM_FONT.render(str(self.value if self.value != 0 else self.sketched_value),
                                   False, color)
        self.screen.blit(num_surf, (self.cell_rect.x + height_offset, self.cell_rect.y + width_offset))
        self.number_pressed = True
