"""
Clone of 2048 game.
"""

#import poc_2048_gui
import random
# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


def slideover(line):
    """
    Helper function for merge: slideover' a line, meaning to shift all nonzeros to the left and move zeros to the right
    """
    #transferring nonzero entities, then appending 0 'numberofzeros' number of times
    numberofzeros = 0
    slidover = []
    for index in line:
        if(index == 0):
            numberofzeros += 1
        else:
            slidover.append(index)
    for dummy_index in range(0,numberofzeros):
        slidover.append(0)
    return slidover

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    # step 1
    slidover = slideover(line)
    
    # step 2 merging by comparing number to the immediately previous number
        #if true, pop last number, append double the current number and 0
        #if false, append current number, lastnumber equal to current number
    combined = []
    lastnumber = None
    for index in range(0, len(slidover)):
        if(lastnumber == slidover[index]):
            combined.pop(index-1)
            combined.append(slidover[index]*2)
            combined.append(0)
            lastnumber = None
        else:
            combined.append(slidover[index])
            lastnumber = slidover[index]  
            
    # step 2b sliding over again
    slidoverandcombined = slideover(combined)
    return slidoverandcombined


def traverse_grid(start_cell, direction, num_steps):
    """
    Taken from sample code given by instructors
    
    Function that iterates through the cells in a grid
    in a linear direction
    
    Both start_cell is a tuple(row, col) denoting the
    starting cell
    
    direction is a tuple that contains difference between
    consecutive cells in the traversal
    
    returns the whole sequence
    """
    new_list = []
    for step in range(num_steps):
        row = start_cell[0] + step * direction[0]
        col = start_cell[1] + step * direction[1]
        new_list.append([row,col])
    return new_list
    
class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        "Store grid height and width"
        self._grid_height = grid_height
        self._grid_width = grid_width
        self.reset()
        self._initial_tiles = {}
        
        #creating dictionary of initial tile coordinates
        
        #top and bottom rows
        toprowcoordinates = []
        bottomrowcoordinates = []
        for col in range(self._grid_width):
            toprowcoordinates.append([0,col])
            bottomrowcoordinates.append([self._grid_height-1,col])
        self._initial_tiles[UP] = toprowcoordinates
        self._initial_tiles[DOWN] = bottomrowcoordinates
        
        #first and last columns
        firstcolumncoordinates = []
        lastcolumncoordinates = []
        for row in range(self._grid_height):
            firstcolumncoordinates.append([row,0])
            lastcolumncoordinates.append([row,self._grid_width-1])
        self._initial_tiles[LEFT] = firstcolumncoordinates
        self._initial_tiles[RIGHT] = lastcolumncoordinates
                    
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._gameboard = [[0 for dummy_index in range(self._grid_width)]
                           for dummy_index2 in range(self._grid_height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        for row in range(self._grid_height):
            print self._gameboard[row]
        # replace with your code
        return ""

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        tile_changed = False
        #create complete grid of coordinates going in direction based on variable direction
        coordinategrid = []
        if(direction == UP or direction == DOWN):
            for coordinates in self._initial_tiles[direction]:
                coordinategrid.append(traverse_grid(coordinates,OFFSETS[direction],self._grid_height))
        else:
            for coordinates in self._initial_tiles[direction]:
                coordinategrid.append(traverse_grid(coordinates,OFFSETS[direction],self._grid_width))
        #use grid of coordinates to make grid of values, then merge each column/row of grid of values depending on variable direction
        mergedvaluegrid = []
        for rowcolumns in coordinategrid:
            valuegrid = []
            for coordinates in rowcolumns:
                valuegrid.append(self.get_tile(coordinates[0], coordinates[1]))
            mergedvaluegrid.append(merge(valuegrid))
        #use mergedvaluegrid and coordinategrid to reassign values for the complete board    
        for index in range(len(mergedvaluegrid)):
            for subindex in range(len(mergedvaluegrid[index])):
                if(mergedvaluegrid[index][subindex] !=
                self.get_tile(coordinategrid[index][subindex][0], coordinategrid[index][subindex][1])):
                    tile_changed = True
                self.set_tile(coordinategrid[index][subindex][0], coordinategrid[index][subindex][1], mergedvaluegrid[index][subindex])
        if(tile_changed):
            self.new_tile()
            
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        row = random.randrange(0, self._grid_height)
        column = random.randrange(0, self._grid_width)
        while(self._gameboard[row][column] != 0):
            row = random.randrange(0, self._grid_height)
            column = random.randrange(0, self._grid_width)
        chancer = random.randrange(1,11)
        if(chancer < 10):
            self._gameboard[row][column] = 2
        else:
            self._gameboard[row][column] = 4

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._gameboard[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._gameboard[row][col]
    
#poc_2048_gui.run_gui(TwentyFortyEight(4, 4))