import math,random

class SudokuGenerator:
    """
    Generates a Sudoku board of size row_length x row_length
    """
    def __init__(self, row_length, removed_cells):
        """
        Initializes the board to be a 2D Python list of size row_length x row_length
        
        -----------
        Attributes:
        -----------
        - row_length is the number of rows/columns of the board (always 9 for this project)
        - removed_cells is an integer value - the number of cells to be removed
        - board is a 2D Python list of size row_length x row_length
        - box_length is the length of the box (always 3 for this project)
        
        -------
        Return:
        None
        """
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0] * self.row_length for _ in range(self.row_length)]
        self.box_length = int(math.sqrt(self.row_length))

    def get_board(self):
        return self.board

    def print_board(self):
        """
        Prints the board to the console
        
        Parameters: None
        Return: None
        """
        for row in self.board:
            for col in row:
                print(col, end=" ")
            print()

    def valid_in_row(self, row, num):
        """
        Checks if num is in the specified row of the board
        
        Parameters:
        - row is the index of the row we are checking
        - num is the value we are looking for in the row
        
        Return: boolean
        """
        if num in self.board[row]:
            return False
        return True

    def valid_in_col(self, col, num):
        """
        Checks if num is in the specified column of the board
        
        Parameters:
        - col is the index of the column we are checking
        - num is the value we are looking for in the column
        
        Return: boolean
        """
        for row in range(self.row_length):
            if self.board[row][col] == num:
                return False
        return True

    def valid_in_box(self, row_start, col_start, num):
        """
        Checks if num is in the specified box of the board
        
        Parameters:
        - row_start and col_start are the starting indices of the box to check
        - num is the value we are looking for in the box
        
        Return: boolean
        """
        for row in range(row_start, row_start + self.box_length):
            for col in range(col_start, col_start + self.box_length):
                if self.board[row][col] == num:
                    return False
        return True
    
   
    def is_valid(self, row, col, num):
        """
        Checks if num can be placed in the specified cell of the board
        i.e. if it is valid to place num in the cell at (row, col)
        
        Parameters:
        - row and col are the row index and col index of the cell to check in the board
        - num is the value to test if it is safe to enter in this cell
        
        Return: boolean
        """
        row_valid = self.valid_in_row(row, num)
        col_valid = self.valid_in_col(col, num)
        # Find the starting indices of the box. 0, 3, or 6 for a 9x9 board.
        box_start_row = row - row % self.box_length
        box_start_col = col - col % self.box_length
        box_valid = self.valid_in_box(box_start_row, box_start_col, num)

        if row_valid and col_valid and box_valid:
            return True
        return False

    def fill_box(self, row_start, col_start):
        """
        Fills the specified 3x3 box with values
        For each position, generates a random digit which has not yet been used in the box
        
        Parameters:
        - row_start and col_start are the starting indices of the box to check
        
        Return: None
        """
        nums = list(range(1, self.row_length + 1)) # 1, 2, 3, ..., 9

        for row in range(row_start, row_start + self.box_length):
            for col in range(col_start, col_start + self.box_length):
                # generate a random number from the list of possible numbers
                index = random.randint(0, len(nums) - 1)
                while not self.is_valid(row, col, nums[index]):
                    # If the number is not valid, try another random number
                    index = random.randint(0, len(nums) - 1)
                self.board[row][col] = nums.pop(index) # remove the number from the possible choices

    def fill_diagonal(self):
        """
        Fills the three boxes along the main diagonal of the board
        These are the boxes which start at (0,0), (3,3), and (6,6)
        
        Parameters: None
        Return: None
        """
        for i in range(0, self.row_length, self.box_length):
            self.fill_box(i, i)

    def fill_remaining(self, row, col):
        """
        Fills the remaining cells of the board
        Should be called after the diagonal boxes have been filled
        
        Parameters:
        - row, col specify the coordinates of the first empty (0) cell
        
        Return: boolean (whether or not we could solve the board)
        """
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True
        
        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def fill_values(self):
        """
        Constructs a solution by calling fill_diagonal and fill_remaining
        
        Parameters: None
        Return: None
        """
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    def remove_cells(self):
        """
        Removes the appropriate number of cells from the board
        This is done by setting some values to 0
        Should be called after the entire solution has been constructed
        i.e. after fill_values has been called
        
        Parameters: None
        Return: None
        """
        cells_to_remove = self.removed_cells

        while cells_to_remove > 0:
            row = random.randint(0, self.row_length - 1)
            col = random.randint(0, self.row_length - 1)

            if self.board[row][col] != 0:
                self.board[row][col] = 0
                cells_to_remove -= 1

def generate_sudoku(size, removed):
    """
    Generates a Sudoku board of size size x size
    Removes removed cells from the board
    Returns the board
    
    Parameters:
    - size is the number of rows/columns of the board (9 for this project)
    - removed is the number of cells to clear (set to 0)
    
    Return: list[list] (a 2D Python list to represent the board)
    """
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board
