# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []
        # create Hand object

    def __str__(self):
        strings = "Hand contains "
        for i in self.cards:
            strings += str(i) + " "
        return strings
            # return a string representation of a hand

    def add_card(self, card):
        (self.cards).append(card)
        # add a card object to a hand

    def get_value(self):
        sum = 0
        for i in self.cards:
            sum += VALUES.get(i.get_rank())
        for i in self.cards:
             if(i.get_rank() == 'A'):
                if(sum < 11):
                    sum += 10
        return sum
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video 
    def draw(self, canvas, pos):
        count = 0
        for i in self.cards:
            i.draw(canvas,(pos[0] + 80 * count, pos[1]))
            count = count + 1
        # draw a hand on the canvas, use the draw method for cards             
   
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        for i in SUITS:
            for j in RANKS:
                (self.cards).append(Card(i,j))
        pass	# create a Deck object

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)
        pass    # use random.shuffle()

    def deal_card(self):
        return (self.cards).pop()
        pass	# deal a card object from the deck
    
    def __str__(self):
        strings = "Deck contains "
        for i in self.cards:
            strings += str(i) + " "
        return strings        
        pass	# return a string representing the deck        

#more global variables
deckOfCards = Deck()
playerHand = Hand()
dealerHand = Hand()

#define event handlers for buttons
def deal():
    global outcome, in_play, deckOfCards, playerHand, dealerHand, score
    if(in_play):
        score -= 1
        outcome = "You lose, why'd you press deal?"
        in_play = False
    else:
        deckOfCards = Deck()
        deckOfCards.shuffle()
        playerHand = Hand()
        dealerHand = Hand()
        playerHand.add_card(deckOfCards.deal_card())
        dealerHand.add_card(deckOfCards.deal_card())
        playerHand.add_card(deckOfCards.deal_card())
        dealerHand.add_card(deckOfCards.deal_card())
        print "This is the player's hand"
        print playerHand
        print "This is the dealer's hand"
        print (dealerHand)
        outcome = "Hit or Stand?"
        in_play = True

def hit(): 
    # if the hand is in play, hit the player
    global in_play, playerHand, outcome, score
    if(in_play):
        playerHand.add_card(deckOfCards.deal_card())
        outcome = "Hit or Stand?"
    # if busted, assign a message to outcome, update in_play and score
    if(playerHand.get_value() > 21):
        outcome = "You have busted, new deal?"
        score -= 1
        in_play = False
def stand():
    global in_play, dealerHand, outcome, score
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if(in_play):
        while(dealerHand.get_value() < 17):
            dealerHand.add_card(deckOfCards.deal_card())
            print "This is the dealer's hand"
            print dealerHand
        if(dealerHand.get_value() > 21):
            outcome = "You won! Dealer has busted, new deal?"
            score += 1
            in_play = False
            return None
    else:
        outcome = "You have busted"
        return None
    in_play = False
    # assign a message to outcome, update in_play and score
    if(dealerHand.get_value() < playerHand.get_value()):
        outcome = "You won! New deal?"
        score += 1
    else:
        outcome = "You lost! New deal?"
        score -= 1
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    dealerHand.draw(canvas, (50, 125))
    canvas.draw_text("Dealer's Hand", (50,100), 20, 'Black')
    if(in_play):
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (85,173), CARD_BACK_SIZE)
    canvas.draw_text("Player's Hand", (50,450), 20, 'Black')
    playerHand.draw(canvas, (50,500))
    canvas.draw_text("Blackjack", (250, 25), 30, 'Blue')
    canvas.draw_text(outcome, (50, 300), 30, 'Blue')
    canvas.draw_text('Score: ' + str(score), (50,50), 20, 'Black')


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric