from turtle import *
from random import *
from base import *


# for keeping score

score = 0
write_score = Turtle(visible = False)

# initial position of ship
ship_pos = { 'x' : -450 , 'y' : 0 }
ship = vector(-450,0)
gap_bt_pipes = 100

# initially empty list of bullets
bullets = []
bullet_speed = vector(10,0)

# initially empty list of enemy bullets
enemy_bullets = []

# speed of movement of pipes
pipe_mov = vector(-2,0)



# functions for genetating the random positions for pipe , targets and random bullet direction
def random_pipe():
    value = randrange(-150,250)
    return value

def random_target():
    value = randrange( -150,150  )
    return value

def random_enemy_bullet():
    value = choice( [randrange(-5,-3) ,randrange(3 , 5)]  )
    return value



# list of pipes
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
    vector(-330,random_target()),
    #vector(-200,random_pipe()),
    vector(-130,random_target() ),
    #vector(0,random_pipe()),
    vector(70,random_target() ),
    #vector(200,random_pipe()),
    vector(270,random_target() ),
    vector(470,random_target() ),


]


# utility function to check whether a point lies inside the boundary of game
def inside(point):
    if abs(point.x) <= 500 and abs(point.y) < 250:
        return True
    else:
        return False



# function to update and draw scoree on the screen
def update_score():
    #Clearing the past score.
    write_score.undo()
    write_score.up()
    write_score.goto(350,300)
    write_score.color('deep pink')
    style = ('Courier', 30, 'italic')
    write_score.write('score = {0}'.format(score), font=style, align='center')

    #write_score.write('score = {0}'.format(score))


# function to draw a rectangle
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


# function to draw boundary of game
def boundary():

    up()
    goto(500,250)
    down()
    goto(500,-250)
    goto(-500,-250)
    goto(-500,250)
    goto(500,250)
    up()


# function to draw the ship (our agent)
def draw_ship():
    up()

    #Going to the ship's position and drawing the SpaceCraft(here dot of colour red)
    ship.x = ship_pos['x']
    ship.y = ship_pos['y']
    goto( ship.x,ship.y )
    dot(20,'red')


# main draw function to show graphics on the screen
def draw():
    global score
    clear()
    boundary()


    # updating the position of all the objects by calling move() at each frame update
    for pipe in pipes:
        pipe.move(pipe_mov)
    for target in targets:
        target.move(pipe_mov)
    for bullet in bullets:
        bullet.move(bullet_speed)
    for enemy_bullet,enemy_bullet_speed in enemy_bullets:
        enemy_bullet.move( enemy_bullet_speed )
        #enemy_bullet.move( vector(-10,0) )




    # radonly generating enemy bullets
    for target in targets:
        if randrange(1,50) == 1:
            pos = vector(target.x,target.y)
            speed = vector (  random_enemy_bullet() , random_enemy_bullet() )
            enemy_bullets.append( (pos,speed)   )



    ''' creating a new pipe at the right end of the screen
     each time a pipe goes out of the left side ofthe screen
     and incrementing score for each pipe passed '''

    if pipes[0].x < -495:
        pipes.pop(0)
        pipes.append(vector(500,random_pipe()))
        targets.append( vector(470,random_target())  )
        score += 1
        update_score()

    # removing targets each time it  moves out of left side of screen
    if len(targets) > 0 :
        if targets[0].x < -500:
            if target is not None:
             targets.pop(0)

    #remove bullets out of screen
    for bullet in bullets:
        if not inside(bullet):
            bullets.remove(bullet)

    #remove enemy bullets out of screen
    for enemy_bullet,speed in enemy_bullets:
        if not inside(enemy_bullet):
            enemy_bullets.remove( (enemy_bullet,speed) )



    ''' drawing all the components '''

    # drawing pipes
    for pipe in pipes :
        rectangle( pipe.x , 250 , 30 ,  250 - pipe.y )
        rectangle( pipe.x , pipe.y - gap_bt_pipes , 30 ,  250 - gap_bt_pipes + pipe.y )


    # drawing targets
    for target in targets:
        up()
        goto( target.x,target.y )
        dot(30,'blue')
        up()

    # finally drawing the ship
    draw_ship()

    # drawing enemy_bullets
    for enemy_bullet,enemy_bullet_speed in enemy_bullets:
        up()
        goto(enemy_bullet.x,enemy_bullet.y)
        dot(5,'blue')
        dot(3,'red')
        up()


    # drawing bullets
    for bullet in bullets:
        up()
        goto(bullet.x,bullet.y)
        color('green')
        rectangle(bullet.x , bullet.y ,5 , 2 )
        color('black')
        #dot(5,'green')
        up()

    ''' all components drawn '''


    ''' checking for collisions between different components '''

    #collision of the ship with a pipe if yes stop the game

    for pipe in pipes:
        if pipe.x -10 < ship.x <= pipe.x+40  and (ship.y + 10 > pipe.y  or ship.y - 10 < pipe.y - gap_bt_pipes)  :
            finish()
            return



    # remove target and bullet on collision

    for bullet in bullets:
        for target in targets:
            if target.x - 15 < bullet.x < target.x + 15 and  target.y - 15 < bullet.y < target.y+15 :
                #print('destroyed')
                targets.remove( target )
                bullets.remove( bullet )
                score += 1
                update_score()


    # stop game on ship's collision with enemy bullet

    for enemy_bullet,speed in enemy_bullets:
        if ship.x - 10 < enemy_bullet.x < ship.x + 10 and ship.y - 10 < enemy_bullet.y < ship.y + 10 :
            finish()
            return

    # stop game on collision with targets
    for target in targets:
        if ship.x - 25 < target.x < ship.x + 25 and ship.y - 25 < target.y < ship.y + 25 :
            finish()
            return

    # remove bullets on collision with pipes
    for bullet in bullets:
        for pipe in pipes:
            if pipe.x  <= bullet.x <= pipe.x+30  and (bullet.y > pipe.y or bullet.y < pipe.y - gap_bt_pipes)  :
                #print('wasted')
                bullets.remove(bullet )

    # take action on collision if enemy bullet with pipes
    for enemy_bullet,speed in enemy_bullets:
        for pipe in pipes:
            if pipe.x  <= enemy_bullet.x <= pipe.x+30  and (enemy_bullet.y > pipe.y or enemy_bullet.y < pipe.y - gap_bt_pipes)  :
                #remove the bullet
                enemy_bullets.remove( (enemy_bullet,speed) )
                #uncomment if we want bullet ot reflect back
                #speed.x = -speed.x

    update()
    ontimer(draw,50)


''' keyboard control functions '''

# move ship up/down on pressing up / down
def changey(value):
    if( abs(ship_pos['y'] + value) < 250 ):
        ship_pos['y'] += value


# move ship left/right on pressing right/ left
def changex(value):
    if( abs(ship_pos['x'] + value) < 500 ):
        ship_pos['x'] += value

# fire a bullet on pressing spacebar
def fire():
    bullets.append( vector(ship.x,ship.y) )

def finish():
    up()
    ship.x = ship_pos['x']
    ship.y = ship_pos['y']
    goto( ship.x,ship.y )
    dot(20,'aquamarine')
    return

#Setting up screen width,height, starting position (x,y) of the SpaceCraft
setup( 1100 , 700 , 0 , 0  )
bgcolor('silver')
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
