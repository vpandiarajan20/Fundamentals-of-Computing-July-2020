# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import random
secretNumberBound = 100
# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number 
    global numberOfGuessesLeft
    secret_number = random.randrange(0,secretNumberBound)
    if(secretNumberBound == 100):
         numberOfGuessesLeft = 7
    elif(secretNumberBound == 1000):
         numberOfGuessesLeft = 10
    print "You have " + str(numberOfGuessesLeft) + " guesses."
    print ""
    # remove this when you add your code    


# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global secretNumberBound
    secretNumberBound = 100
    print "Maximum secret number changed to 99"
    print ""
    new_game()
    # remove this when you add your code    

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global secretNumberBound
    secretNumberBound = 1000
    print "Maximum secret number changed to 999"
    print ""
    new_game()

def input_guess(guess):
    # main game logic goes here	
    guessAsNumber = float(guess)
    print guessAsNumber
    if(secret_number > guessAsNumber):
        print "Higher"
    elif(secret_number < guessAsNumber):
        print "Lower"
    elif(secret_number == guessAsNumber):
        print "Correct"
        print ""
        new_game()
    global numberOfGuessesLeft
    numberOfGuessesLeft -= 1
    print "You have " + str(numberOfGuessesLeft) + " guesses left."
    print ""
    if(numberOfGuessesLeft == 0 and secret_number != guessAsNumber):
        print "You lose!"
        print ""
        new_game()
    # remove this when you add your code

    
# create frame
frame = simplegui.create_frame('Testing', 200, 200)

# register event handlers for control elements and start frame
inp = frame.add_input('Enter your guess', input_guess, 50)
button1 = frame.add_button('New Game!', new_game)
button2 = frame.add_button("Range is [0,100)", range100)
button3 = frame.add_button("Range is [0,1000)", range1000)

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
