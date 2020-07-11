# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 600       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH/2,HEIGHT/2]
ball_vel = [0, 0]
paddle1_pos = HEIGHT/2
paddle2_pos = HEIGHT/2
paddle1_vel = 0
paddle2_vel = 0
player1score = 0
player2score = 0
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2,HEIGHT/2]
    if(direction == 'LEFT'):
        ball_vel = [random.randrange(-4,-2), random.randrange(-5,-2)]
    if(direction == 'RIGHT'):
        ball_vel = [random.randrange(2,4), random.randrange(-5,-2)]        

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos,paddle2_pos = HEIGHT/2, HEIGHT/2
    paddle1_vel, paddle2_vel = 0, 0
    score1, score2 = 0, 0 
    spawn_ball('LEFT')

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]      
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if(paddle1_pos + PAD_HEIGHT + paddle1_vel > HEIGHT or paddle1_pos + paddle1_vel < 0):
        paddle1_vel = 0
    else:
        paddle1_pos += paddle1_vel
        
    if(paddle2_pos + PAD_HEIGHT + paddle2_vel > HEIGHT or paddle2_pos + paddle2_vel < 0):
        paddle2_vel = 0
    else:
        paddle2_pos += paddle2_vel
        
    # draw paddles
    canvas.draw_polygon([(PAD_WIDTH, paddle1_pos), (PAD_WIDTH, paddle1_pos + PAD_HEIGHT), (0, paddle1_pos + PAD_HEIGHT),(0, paddle1_pos) ], 1, 'Green', 'Green')
    canvas.draw_polygon([(WIDTH - PAD_WIDTH, paddle2_pos), (WIDTH - PAD_WIDTH, paddle2_pos + PAD_HEIGHT), (WIDTH, paddle2_pos + PAD_HEIGHT),(WIDTH, paddle2_pos) ], 1, 'Green', 'Green')
    
    # determine whether paddle and ball collide    
    ##if(ball_pos[0] > WIDTH - BALL_RADIUS or ball_pos[0] < BALL_RADIUS):
    ##    ball_vel[0] = -ball_vel[0]
    if(ball_pos[0] > WIDTH - PAD_WIDTH - BALL_RADIUS and ball_pos[1] >= paddle2_pos and ball_pos[1] <= paddle2_pos + PAD_HEIGHT):
        ball_vel[0] = -ball_vel[0]*1.1    
    elif(ball_pos[0] > WIDTH - PAD_WIDTH - BALL_RADIUS):
        spawn_ball('LEFT')
        score1 += 1
        
    if(ball_pos[0] < BALL_RADIUS + PAD_WIDTH and ball_pos[1] >= paddle1_pos and ball_pos[1] <= paddle1_pos + PAD_HEIGHT):
        ball_vel[0] = -ball_vel[0]*1.1
    elif(ball_pos[0] < BALL_RADIUS + PAD_WIDTH):
        spawn_ball('RIGHT')
        score2 += 1
        
    if(ball_pos[1] < BALL_RADIUS or ball_pos[1] > HEIGHT - BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]      
    # draw scores
    canvas.draw_text(str(score1), (150, 40), 30, 'Red')
    canvas.draw_text(str(score2), (450, 40), 30, 'Red')
    
def keydown(key):
    global paddle1_vel, paddle2_vel  
    if(simplegui.KEY_MAP['up'] == key):
        paddle1_vel = -6
    if(simplegui.KEY_MAP['down'] == key):
        paddle1_vel = 6
    if(simplegui.KEY_MAP['w'] == key):
        paddle2_vel = -6
    if(simplegui.KEY_MAP['s'] == key):
        paddle2_vel = 6  
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = 0
    paddle2_vel = 0
    


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
button1 = frame.add_button('Restart', new_game)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
