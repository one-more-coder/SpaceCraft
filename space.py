from turtle import *
from random import *
from base import *


score = 0

write_score = Turtle(visible = False)

#setting the position of the SpaceCraft( (0,0) is the center of our screen)
ship_pos = { 'x' : -450 , 'y' : 0 }

ship = vector(-450,0)

gap_bt_pipes = 100

def random_pipe():
    value = randrange(-150,250)
    return value

def random_target():
    value = randrange(-200,200)
    return value

def random_enemy_bullet():
    value = choice( [randrange(-5,-3) ,randrange(3 , 5)]  )

#Coordinates of the pipes
pipes = [
    vector(-300,random_pipe()),
    #vector(-200,random_pipe()),
    vector(-100,random_pipe()),
    #vector(0,random_pipe()),
    vector(100,random_pipe()),
    #vector(200,random_pipe()),
    vector(300,random_pipe()),
    vector(500,random_pipe()),

]

#Coordinates of the enemy ships
targets = [
    vector(-330,random_pipe()),
    #vector(-200,random_pipe()),
    vector(-130,random_pipe()),
    #vector(0,random_pipe()),
    vector(70,random_pipe()),
    #vector(200,random_pipe()),
    vector(270,random_pipe()),
    vector(470,random_pipe()),


]

bullets = []
enemy_bullets = []

#speed of bullets ( 10 + j0 m/s)
bullet_speed = vector(10,0)

#speed of pipe( -2 + j0 m/s)
pipe_mov = vector(-2,0)

#Updating the score on the score board
def update_score():
    #Clearing the past score.
    write_score.undo()
    write_score.up()
    #Going to the position on the screen
    write_score.goto(450,300)
    write_score.write('score = {0}'.format(score))

#Drawing pipes and enemy SpaceCraft
def rectangle(x,y,width,height):
    up()
    goto(x,y)
    down()
    begin_fill()
    for count in range(2):
        forward(width)
        right(90)
        forward(height)
        right(90)
    end_fill()

#Function to define the boundary of the game
def boundary():

    up()
    goto(500,250)
    down()
    goto(500,-250)
    goto(-500,-250)
    goto(-500,250)
    goto(500,250)
    up()

def draw():
    global score

    #delete the turtle's drawing from the screen
    clear()

    #drawing the game boundary
    boundary()

    up()

    #Going to the ship's position and drawing the SpaceCraft(here dot of colour red)
    ship.x = ship_pos['x']
    ship.y = ship_pos['y']
    goto( ship.x,ship.y )
    dot(20,'red')

    for pipe in pipes:
        pipe.move(pipe_mov)
    for target in targets:
        target.move(pipe_mov)
    for bullet in bullets:
        bullet.move(bullet_speed)


    for enemy_bullet,enemy_bullet_speed in enemy_bullets:
        enemy_bullet.move(enemy_bullet_speed)



    #
    # for target in targets:
    #     if randrange(1,11) == 1:
    #         enemy_bullets.append( (vector(target.x,target.y) , vector( random_enemy_bullet().random_enemy_bullet() ))  )

    #Removing the pipe and enemy when it goes out of screen and adding it to the coming pipes
    if pipes[0].x < -500:
        pipes.pop(0)
        pipes.append(vector(500,random_pipe()))
        # if targets[0].x < -500:
        #     targets.pop(0)

        targets.append( vector(470,random_target())  )
        score += 1
        update_score()

    #Drawing the bullets
    for bullet in bullets:
        up()
        goto(bullet.x,bullet.y)
        color('green')
        rectangle(bullet.x , bullet.y ,5 , 2 )
        color('black')
        #dot(5,'green')
        up()

    #Colouring the enemy SpaceCrafts
    for target in targets:
        up()
        goto( target.x,target.y )
        dot(30,'blue')
        up()

    #Drawing the pipes onto the screen    
    for pipe in pipes :
        rectangle( pipe.x , 250 , 30 ,  250 - pipe.y )
        rectangle( pipe.x , pipe.y - gap_bt_pipes , 30 ,  250 - gap_bt_pipes + pipe.y )

    for pipe in pipes:
        if pipe.x -10 < ship.x <= pipe.x+40  and (ship.y > pipe.y or ship.y < pipe.y - gap_bt_pipes)  :
            return

    for bullet in bullets:
        for target in targets:
            if target.x - 15 < bullet.x < target.x + 15 and  target.y - 15 < bullet.y < target.y+15 :
                #print('destroyed')
                targets.remove( target )
                bullets.remove( bullet )

    for bullet in bullets:
        for pipe in pipes:
            if pipe.x  <= bullet.x <= pipe.x+30  and (bullet.y > pipe.y or bullet.y < pipe.y - gap_bt_pipes)  :
                #print('wasted')
                bullets.remove(bullet )


    update()
    ontimer(draw,50)

#changing the position of SpaceCraft in y direction on pressing up-down keys
def changey(value):
    if( abs(ship_pos['y'] + value) < 250 ):
        ship_pos['y'] += value

#changing the position of SpaceCraft in x direction on pressing left-right keys
def changex(value):
    ship_pos['x'] += value

#getting the position of the ship so that we can start throwing bullets from that position only
def fire():
    bullets.append( vector(ship.x,ship.y) )


#Setting up screen width,height, starting position (x,y) of the SpaceCraft
setup( 1100 , 700 , 0 , 0  )

#hiding the turtle
hideturtle()

#hiding the making of screen
tracer(False)

#setting all the focus of the monitor screen to our game window screen
listen()

#setting the controllers for the game
onkey(lambda:changey(10),'Up')
onkey(lambda:changey(-10),'Down')
onkey(lambda:changex(10),'Right')
onkey(lambda:changex(-10),'Left')
onkey(fire,'space')

update_score()
draw()
done()
