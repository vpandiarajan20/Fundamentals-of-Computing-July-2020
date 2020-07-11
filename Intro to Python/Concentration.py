# implementation of card game - Memory

import simplegui
import random
deckOfCards = range(0,8)
deckOfCards.extend(range(0,8))
random.shuffle(deckOfCards)
state = 0
firstCard = 0
secondCard = 0
turns = 0
exposed = [False, False, False, False, False, False, False, False, False, False, False, False,False, False, False, False]

# helper function to initialize globals
def new_game():
    global deckOfCards, state, firstCard, secondCard, turns, exposed
    random.shuffle(deckOfCards)
    state = 0
    firstCard = 0
    secondCard = 0
    turns = 0
    exposed = [False, False, False, False, False, False, False, False, False, False, False, False,False, False, False, False]
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, firstCard, secondCard, turns
    count = 0
    for x in deckOfCards:
        iterator = 50 * count
        if(pos[0] < 50 + iterator and pos[0] > iterator):
            if(exposed[count] == True):
                return None
            exposed[count] = True
            if state == 0:
                state = 1
                firstCard = count
            elif state == 1:
                state = 2
                secondCard = count
                turns += 1
            else:
                if(deckOfCards[firstCard] != deckOfCards[secondCard]):
                    exposed[firstCard], exposed[secondCard] = False, False
                state = 1
                firstCard = count
        count += 1    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    count = 0
    for x in deckOfCards:
        iterator = 50 * count
        if(exposed[count]):
            canvas.draw_text(str(x), (25 + iterator, 50), 20, 'White')
        else:
            canvas.draw_polygon([(iterator,0),(iterator, 100), (50 + iterator, 100), (50 + iterator, 0)], 12, "Black", "Green")
        count = count + 1
    label.set_text("Turns = " + str(turns))


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric