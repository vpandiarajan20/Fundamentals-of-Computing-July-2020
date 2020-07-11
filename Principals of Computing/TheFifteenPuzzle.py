"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # replace with your code
        if(self.get_number(target_row, target_col) != 0):
            return False
        dummy_row = target_row
        while dummy_row < self.get_height():
            dummy_col = 0
            if(dummy_row == target_row):
                dummy_col = target_col + 1
            while dummy_col < self.get_width():
                if(self.get_number(dummy_row, dummy_col) != self.get_width() * dummy_row + dummy_col):
                    return False
                dummy_col += 1
            dummy_row += 1
        return True
    
    def position_tile(self, location_row, location_column, destination_row, destination_column):
        """
        move tile from location_row, location_column to destination_row, destination_column
        """
        move = ""
        # If tile is directly above
        if(location_column == destination_column):
            for dummy_index in range(destination_row - location_row):
                move += "u"
            for dummy_index in range(destination_row - location_row-1):    
                move += "lddru"
            move += "ld"
            self.update_puzzle(move)
            return move
        
        # If tile is directly to the left
        if(location_column != destination_column and location_row == destination_row):
            for dummy_index in range(destination_column - location_column):
                move += "l"
            for dummy_index in range(destination_column - location_column-1):
                move += "urrdl"
            self.update_puzzle(move)
            return move
        
        # If tile is above and to the left
        if(location_column < destination_column):
            for dummy_index in range(destination_row - location_row):
                move += "u"
            for dummy_index in range(destination_column - location_column):
                move += "l"
            for dummy_index in range(destination_column - location_column-1):
                if(location_row == 0):
                    move += "drrul"
                else:
                    move += "urrdl"
            move += "dru"
            for dummy_index in range(destination_row - location_row-1):    
                move += "lddru"
            move += "ld"
            self.update_puzzle(move)
            return move
        
        # If tile is above and to the right
        if(location_column > destination_column):
            for dummy_index in range(destination_row - location_row):
                move += "u"
            for dummy_index in range(location_column - destination_column):
                move += "r"
            for dummy_index in range(location_column - destination_column-1):
                if(location_row == 0):
                    move += "dllur"
                else:
                    move += "ulldr"
            if(location_row == 0):
                move += "dlu"
            else:
                move += "ullddru"
            for dummy_index in range(destination_row - location_row-1): 
                move += "lddru"
            move += "ld"
            print move
            self.update_puzzle(move)
            return move
        return move
    
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """       
        assert self.lower_row_invariant(target_row, target_col)
        correct_tile_row, correct_tile_column  = self.current_position(target_row, target_col)
        return self.position_tile(correct_tile_row, correct_tile_column, target_row, target_col)

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0)
        self.update_puzzle('ur')
        if(self.current_position(target_row, 0) == (target_row, 0)):
            returnvalue = 'ur'
        else:
            tile_row, tile_col = self.current_position(target_row, 0)
            returnvalue = self.position_tile(tile_row, tile_col, target_row-1, 1)
            algorithim = "ruldrdlurdluurddlur"
            self.update_puzzle(algorithim)
            returnvalue = 'ur' + returnvalue + algorithim
        move = ""
        for dummy_index in range(self.get_width() - self.current_position(0, 0)[1] - 1):
            move += "r"
        self.update_puzzle(move)
        return returnvalue + move
            
    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if(self.get_number(0, target_col) != 0):
            return False
        dummy_row = 0
        while dummy_row < self.get_height():
            dummy_col = 0
            if(dummy_row == 0):
                dummy_col = target_col + 1
            if(dummy_row == 1):
                dummy_col = target_col
            while dummy_col < self.get_width():
                if(self.get_number(dummy_row, dummy_col) != self.get_width() * dummy_row + dummy_col):
                    return False
                dummy_col += 1
            dummy_row += 1
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if(self.get_number(1, target_col) != 0):
            return False
        dummy_row = 1
        while dummy_row < self.get_height():
            dummy_col = 0
            if(dummy_row == 1):
                dummy_col = target_col + 1
            while dummy_col < self.get_width():
                if(self.get_number(dummy_row, dummy_col) != self.get_width() * dummy_row + dummy_col):
                    return False
                dummy_col += 1
            dummy_row += 1
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        self.update_puzzle('ld')
        if(self.current_position(0, target_col) == (0, target_col)):
            returnvalue = 'ld'
        else:
            tile_row, tile_col = self.current_position(0, target_col)
            returnvalue = self.position_tile(tile_row, tile_col, 1, target_col-1)
            algorithim = "urdlurrdluldrruld"
            self.update_puzzle(algorithim)
            returnvalue = 'ld' + returnvalue + algorithim
        return returnvalue       

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col)
        tile_location = self.current_position(1, target_col)
        returnvalue = self.position_tile(tile_location[0], tile_location[1], 1, target_col)
        returnvalue += "ur"
        self.update_puzzle("ur")
        assert self.row0_invariant(target_col)
        return returnvalue

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        self.update_puzzle("ul")
        
        # if one is top right
        if(self.current_position(0, 1) == (0,1)):
            return "ul"
        
        # if one is bottom left
        if(self.current_position(0, 1) == (1,0)):
            self.update_puzzle("drul")
            return "uldrul"
        
        # if one is bottom right
        if(self.current_position(0, 1) == (1,1)):
            self.update_puzzle("rdlu")
            return "ulrdlu"
        
        return ""

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        returnvalue = ""
        
        # move zero to bottom right
        for dummy_index in range(self.get_width()- 1 - self.current_position(0,0)[1]):
            returnvalue += "r"
        for dummy_index in range(self.get_height()- 1 - self.current_position(0,0)[0]):
            returnvalue += "d"
        self.update_puzzle(returnvalue)
        
        # loop through puzzle, right to left, bottom to top until top two rows
        for dummy_row in range(self.get_height() - 1, 1, -1):
            for dummy_col in range(self.get_width() - 1, -1, -1):
                assert self.lower_row_invariant(dummy_row,dummy_col)
                if(dummy_col == 0):
                    returnvalue += self.solve_col0_tile(dummy_row)
                else:
                    returnvalue += self.solve_interior_tile(dummy_row,dummy_col)
                    
        # loop through all elements except two by two box
        for dummy_col in range(self.get_width() - 1, 1, -1):
            assert self.row1_invariant(dummy_col)
            returnvalue += self.solve_row1_tile(dummy_col)
            assert self.row0_invariant(dummy_col)
            returnvalue += self.solve_row0_tile(dummy_col)
            
        # loop through 2x2 box
        returnvalue += self.solve_2x2()
        
        return returnvalue

# Start interactive simulation
#obj = Puzzle(3, 3, [[0, 5, 4], [1, 3, 2], [6, 7, 8]])
#poc_fifteen_gui.FifteenGUI(Puzzle(2,2,[[0,1], [3,1]]))
#print test_puzzle.lower_row_invariant(3,3)
#print test_puzzle.find_tile_of_value(17)
#print test_puzzle.solve_col0_tile(3)
#print test_puzzle
#print obj.solve_puzzle()
#print obj

#obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#obj.solve_puzzle()
#print obj
