"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board,player):
    """
    This function takes a current board and the next player to move. 
    The function should play a game starting with the given player by making random moves, alternating between players. 
    The function should return when the game is over. 
    The modified board will contain the state of the game, so the function does not return anything. 
    In other words, the function should modify the board
    """
    # the entire while loop plays one game
    while(board.check_win() == None):
        # generates a random square for a player to mark
        currentsquare = board.get_empty_squares()[random.randrange(len(board.get_empty_squares()))]
        # makes move at generated random square
        board.move(currentsquare[0], currentsquare[1], player)
        # switch players
        player = provided.switch_player(player)

def mc_update_scores(scores, board, player):
    """
    This function takes a grid of scores (a list of lists) with the same dimensions as the Tic-Tac-Toe board, a board from a completed game, and which player the machine player is.
    The function should score the completed board and update the scores grid.
    As the function updates the scores grid directly, it does not return anything,  
    """
    if(board.check_win() == player):
        valueofplayersquares = SCORE_CURRENT
        valueofcomputersquares = -SCORE_OTHER
    elif(board.check_win() == provided.switch_player(player)):
        valueofplayersquares = -SCORE_CURRENT
        valueofcomputersquares = SCORE_OTHER
    else:
        return None
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if(board.square(row,col) == player):
                scores[row][col] += valueofplayersquares
            elif(board.square(row,col) == provided.switch_player(player)):
                 scores[row][col] += valueofcomputersquares
    return None

def create_score_grid(board):
    """
    initializes empty score array
    """
    scoregrid = []
    for dummy_index in range(board.get_dim()):
        onerow = []
        for dummy_index2 in range(board.get_dim()):
            onerow.append(0)
        scoregrid.append(onerow)
    return scoregrid

def get_best_move(board, scores):
    """
    This function takes a current board and a grid of scores.
    The function should find all of the empty squares with the maximum score and randomly return one of them as a tuple.
    It is an error to call this function with a board that has no empty squares (there is no possible next move), so your function may do whatever it wants in that case.
    The case where the board is full will not be tested.
    """
    if(len(board.get_empty_squares()) == 0):
        return None
    maxscore = float('-inf')
    emptysquares = []
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if((row,col) in board.get_empty_squares()):
                if(scores[row][col] > maxscore):
                    emptysquares = []
                    emptysquares.append((row,col))
                    maxscore = scores[row][col]
                elif(scores[row][col] == maxscore):
                    emptysquares.append((row,col))
    return emptysquares[random.randrange(len(emptysquares))]

def mc_move(board,player,trials):
    """
This function takes a current board, which player the 
machine player is, and the number of trials to run. 
The function should use the Monte Carlo simulation 
described above to return a move for the machine player 
in the form of a (row, column) tuple. Be sure to use the 
other functions you have written!
    """
    scores = create_score_grid(board)
    for dummy_index in range(trials):
        clone_board = board.clone()
        mc_trial(clone_board,player)
        mc_update_scores(scores, clone_board, player)
    print scores    
    return get_best_move(board,scores)


# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
