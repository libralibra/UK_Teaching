''' COMP712 Classical Artificial Intelligence Workshop
    Falmouth University, 2023-2024
    Dr Daniel Zhang
    Oct 2023

    This is a simple implementation of the classic Pong game
    Controls are W,S for Player A and Up, Down for Player B

    Tasks: 

    1. Implement collisions with the board's top and bottom, as well as the left and right paddles to make the game complete.
    2. Change the ball's starting speed using the random module.
    3. Adjust the size and moving speed of the paddles.
    4. Add more fun by speeding up the ball after a certain number of catches.
    5. Increase the excitement by adding a 'random' direction change for each collision with the board or paddle.
    6. Implement any other improvements you can imagine!
'''

import turtle as t

##################################
# The global variables
##################################

# player scores
player_a_score = 0
player_b_score = 0

# board size and colour
board_width = 800
board_height = 600
board_bg_colour = 'green'

# paddle parameters
paddle_length = 5
paddle_width = 2
paddle_colour = 'white'
paddle_speed = 50

# ball parameters
ball_colour = 'red'
ball_radius = 10
ball_dx = 0.2
ball_dy = 0.2

##################################
# board creation
##################################

# creating the main board
window = t.Screen()
window.title("The Pong Game")
window.bgcolor(board_bg_colour)
window.setup(width = board_width, height = board_height)
window.tracer(0)

# creating the left paddle
left_paddle = t.Turtle()
left_paddle.speed(0)
left_paddle.shape("square")
left_paddle.color(paddle_colour)
left_paddle.shapesize(stretch_wid=paddle_length, stretch_len=paddle_width)
left_paddle.penup()
left_paddle.goto(-int(board_width/2),0)

# creating the right paddle
right_paddle=t.Turtle()
right_paddle.speed(0)
right_paddle.shape("square")
right_paddle.color(paddle_colour)
right_paddle.shapesize(stretch_wid=paddle_length, stretch_len=paddle_width)
right_paddle.penup()
right_paddle.goto(int(board_width/2)-paddle_width,0)

# creating the ball
ball = t.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color(ball_colour)
ball.penup()
ball.goto(ball_radius, ball_radius)

# creating pen for scorecard update
pen = t.Turtle()
pen.speed(0)
pen.color("Blue")
pen.penup()
pen.hideturtle()
pen.goto(0,0)
pen.write("score",align="center",font=('Arial',24,'normal'))

##################################
# Helper functions
##################################

def left_paddle_up():
    ''' moving the left paddle up '''
    y=left_paddle.ycor()
    y += paddle_speed
    left_paddle.sety(y)

def left_paddle_down():
    ''' moving the left paddle down '''
    y=left_paddle.ycor()
    y -= paddle_speed
    left_paddle.sety(y)

def right_paddle_up():
    ''' moving the right paddle up '''
    y=right_paddle.ycor()
    y += paddle_speed
    right_paddle.sety(y)

def right_paddle_down():
    ''' moving the right paddle down '''
    y=right_paddle.ycor()
    y -= paddle_speed
    right_paddle.sety(y)

def msgbox(msg):
    ''' show a message box for debugging '''
    t.TK.messagebox.showinfo(title="The Turtle says:", message=msg)

def write_text(txt):
    ''' write text '''
    pen.clear()
    pen.write(txt,align="center",font=('Monaco',24,"normal"))

# assign keys to move paddles
window.listen()
window.onkeypress(left_paddle_up,'w')
window.onkeypress(left_paddle_down,'s')
window.onkeypress(right_paddle_up,'Up')
window.onkeypress(right_paddle_down,'Down')

##################################
# The main loop for the game
##################################
while True:
    window.update()

    # moving the ball
    ball.setx(ball.xcor() + ball_dx)
    ball.sety(ball.ycor() + ball_dy)

    # draw the message
    msg = f'Player A: {player_a_score} <=> Player B: {player_b_score}\n'
    write_text(msg)

    # BALL HIT BOARD TOP
    if # BALL HIT BOARD TOP:
        # YOUR CODE HERE
        # msgbox('hit top')

    if # BALL HIT BOARD BOTTOM:
        # YOUR CODE HERE
        # msgbox('HIT bottom')
    
    # collisions with right paddle
    if # BALL HIT THE RIGHT PADDLE:
        # YOUR CODE HERE
        # msgbox('right catches!')

    # collisions with left paddle
    if # BALL HIT THE LEFT PADDLE:
        # YOUR CODE HERE
        # msgbox('left catches!')
    
    # right paddle missed
    if # RIGHT PADDLE MISSED:
        # YOUR CODE HERE
        # msgbox('Player B missed, and Player A scored!')

    # left paddle missed
    if # LEFT PADDLE MISSED:
        # YOUR CODE HERE
        # msgbox('Player A missed, and Player B scored!')