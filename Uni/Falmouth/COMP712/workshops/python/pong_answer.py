'''
This is a simple implementation of the pong game
Controls are W,S for Player A and Up, Down for Player B

Tasks:

1. Implement collisions with the board's top and bottom, as well as the left and right paddles to make the game complete.

2. Change the ball's starting speed using the random module.

3. Adjust the size and moving speed of the paddles.

4. Add more fun by speeding up the ball after a certain number of catches.

5. Increase the excitement by adding a 'random' direction change for each collision with the board or paddle.

6. Implement any other improvements you can imagine!

Daniel Zhang @ Falmouth
Oct 2023

reference: https://www.askpython.com/python/examples/easy-games-in-python
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

# Creating the main board
window = t.Screen()
window.title("The Pong Game")
window.bgcolor(board_bg_colour)
window.setup(width = board_width, height = board_height)
window.tracer(0)

# Creating the left paddle
left_paddle = t.Turtle()
left_paddle.speed(0)
left_paddle.shape("square")
left_paddle.color(paddle_colour)
left_paddle.shapesize(stretch_wid=paddle_length, stretch_len=paddle_width)
left_paddle.penup()
left_paddle.goto(-int(board_width/2),0)

# Creating the right paddle
right_paddle=t.Turtle()
right_paddle.speed(0)
right_paddle.shape("square")
right_paddle.color(paddle_colour)
right_paddle.shapesize(stretch_wid=paddle_length, stretch_len=paddle_width)
right_paddle.penup()
right_paddle.goto(int(board_width/2)-paddle_width,0)

# Creating the ball
ball = t.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color(ball_colour)
ball.penup()
ball.goto(ball_radius, ball_radius)

#Code for creating pen for scorecard update
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
    y = min(y,int(board_height/2-paddle_length*10))
    left_paddle.sety(y)

def left_paddle_down():
    ''' moving the left paddle down '''
    y=left_paddle.ycor()
    y -= paddle_speed
    y = max(y,int(-board_height/2+paddle_length*10))
    left_paddle.sety(y)

def right_paddle_up():
    ''' moving the right paddle up '''
    y=right_paddle.ycor()
    y += paddle_speed
    y = min(y,int(board_height/2-paddle_length*10))
    right_paddle.sety(y)

def right_paddle_down():
    ''' moving the right paddle down '''
    y=right_paddle.ycor()
    y -= paddle_speed
    y = max(y,int(-board_height/2+paddle_length*10))
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
    # msg += f'ball({ball.xcor():.0f},{ball.ycor():.0f})\n'
    # msg += f'left({left_paddle.xcor():.0f},{left_paddle.ycor():.0f})\n'
    # msg += f'right({right_paddle.xcor():.0f},{right_paddle.ycor():.0f})'
    write_text(msg)

    # border set up
    if ball.ycor() >= board_height/2 - ball_radius:
        ball.sety(board_height/2 - ball_radius)
        ball_dy *= -1
        # msgbox('tap top')
    if ball.ycor() <= -board_height/2 + 2*ball_radius:
        ball.sety(-board_height/2 + 2*ball_radius)
        ball_dy *= -1
        # msgbox('tap bottom')
    
    # collisions with right paddle
    if (ball.xcor() >= right_paddle.xcor() - 3*ball_radius) and (right_paddle.ycor() - paddle_length*10 < ball.ycor() < right_paddle.ycor() + paddle_length*10):
        ball.setx(right_paddle.xcor() - 3*ball_radius)
        ball_dx *= -1
        # msgbox('right catches!')

    # collisions with left paddle
    if (ball.xcor() < left_paddle.xcor() + 3*ball_radius) and (left_paddle.ycor() - paddle_length*10 < ball.ycor() < left_paddle.ycor() + paddle_length*10):
        ball.setx(left_paddle.xcor() + 3*ball_radius)
        ball_dx *= -1
        # msgbox('left catches!')
    
    # right paddle missed
    if ball.xcor() > board_width/2 - 2*ball_radius:
        ball.goto(0,0)
        ball_dx *= -1
        player_a_score += 1
        msg = f'Player A: {player_a_score} <=> Player B: {player_b_score}\n'
        # msg += f'ball({ball.xcor():.0f},{ball.ycor():.0f})\n'
        # msg += f'left({left_paddle.xcor():.0f},{left_paddle.ycor():.0f})\n'
        # msg += f'right({right_paddle.xcor():.0f},{right_paddle.ycor():.0f})'
        write_text(msg)
        msgbox('Player B missed, and Player A scored!')

    # left paddle missed
    if (ball.xcor()) < -board_width/2 + ball_radius: 
        ball.goto(0,0)
        ball_dx *= -1
        player_b_score += 1
        msg = f'Player A: {player_a_score} <=> Player B: {player_b_score}\n'
        # msg += f'ball({ball.xcor():.0f},{ball.ycor():.0f})\n'
        # msg += f'left({left_paddle.xcor():.0f},{left_paddle.ycor():.0f})\n'
        # msg += f'right({right_paddle.xcor():.0f},{right_paddle.ycor():.0f})'
        write_text(msg)
        msgbox('Player A missed, and Player B scored!')