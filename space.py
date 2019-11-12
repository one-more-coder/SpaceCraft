from turtle import *
from random import *
from base import *

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



class Game:
    def __init__(self):
        self.score = 0
        self.write_score = Turtle(visible = False)

        # initial position of ship
        self.ship_pos = { 'x' : -450 , 'y' : 0 }
        self.ship = vector(-450,0)
        self.gap_bt_pipes = 100


        # initially empty list of bullets
        self.bullets = []
        self.bullet_speed = vector(10,0)

        # initially empty list of enemy bullets
        self.enemy_bullets = []

        # speed of movement of pipes
        self.pipe_mov = vector(-2,0)

        # list of pipes
        self.pipes = [
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
        self.targets = [
            vector(-330,random_target() ),
            #vector(-200,random_pipe()),
            vector(-130,random_target() ),
            #vector(0,random_pipe()),
            vector(70,random_target() ),
            #vector(200,random_pipe()),
            vector(270,random_target() ),
            vector(470,random_target() ),
        ]


        #Setting up screen width,height, starting position (x,y) of the SpaceCraft
        setup( 1100 , 700 , 0 , 0  )
        bgcolor('silver')
        # bgpic('background.jpeg')

        #hiding the turtle
        hideturtle()

        #hiding the making of screen
        tracer(False)

        #setting all the focus of the monitor screen to our game window screen
        listen()

        #setting the controllers for the game
        onkey(lambda:self.changey(10),'Up')
        onkey(lambda:self.changey(-10),'Down')
        onkey(lambda:self.changex(10),'Right')
        onkey(lambda:self.changex(-10),'Left')
        onkey(self.fire,'space')

        self.update_score()
        self.draw()
        done()


    # utility function to check whether a point lies inside the boundary of game
    def inside(self,point):
        if abs(point.x) <= 500 and abs(point.y) < 250:
            return True
        else:
            return False



    # function to update and draw scoree on the screen
    def update_score(self):
        #Clearing the past score.
        self.write_score.undo()
        self.write_score.up()
        self.write_score.goto(350,300)
        self.write_score.color('deep pink')
        style = ('Courier', 30, 'italic')
        self.write_score.write('score = {0}'.format(self.score), font=style, align='center')

        #write_score.write('score = {0}'.format(score))


    # function to draw a rectangle
    def rectangle(self,x,y,width,height):
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
    def boundary(self):

        up()
        goto(500,250)
        down()
        goto(500,-250)
        goto(-500,-250)
        goto(-500,250)
        goto(500,250)
        up()


    # function to draw the ship (our agent)
    def draw_ship(self):
        up()

        #Going to the ship's position and drawing the SpaceCraft(here dot of colour red)
        self.ship.x = self.ship_pos['x']
        self.ship.y = self.ship_pos['y']
        goto( self.ship.x,self.ship.y )
        dot(20,'red')

    # main draw function to show graphics on the screen
    def draw(self):
        #global score
        clear()
        self.boundary()

        # updating the position of all the objects by calling move() at each frame update
        for pipe in self.pipes:
            pipe.move(self.pipe_mov)
        for target in self.targets:
            target.move(self.pipe_mov)
        for bullet in self.bullets:
            bullet.move(self.bullet_speed)
        for enemy_bullet,enemy_bullet_speed in self.enemy_bullets:
            enemy_bullet.move( enemy_bullet_speed )
            #enemy_bullet.move( vector(-10,0) )

        # randomly generating enemy bullets
        for target in self.targets:
            if randrange(1,50) == 1:
                pos = vector(target.x,target.y)
                speed = vector (  random_enemy_bullet() , random_enemy_bullet() )
                self.enemy_bullets.append( (pos,speed)   )

        ''' creating a new pipe at the right end of the screen
         each time a pipe goes out of the left side ofthe screen
         and incrementing score for each pipe passed '''

        if self.pipes[0].x < -495:
            self.pipes.pop(0)
            self.pipes.append(vector(500,random_pipe()))
            self.targets.append( vector(470,random_target())  )
            self.score += 1
            self.update_score()

        # removing targets each time it  moves out of left side of screen
        if len(self.targets) > 0 :
            if self.targets[0].x < -500:
                if target is not None:
                 self.targets.pop(0)

        #remove bullets out of screen
        for bullet in self.bullets:
            if not self.inside(bullet):
                self.bullets.remove(bullet)

        #remove enemy bullets out of screen
        for enemy_bullet,speed in self.enemy_bullets:
            if not self.inside(enemy_bullet):
                self.enemy_bullets.remove( (enemy_bullet,speed) )


        ''' drawing all the components '''

        # drawing pipes
        for pipe in self.pipes :
            self.rectangle( pipe.x , 250 , 30 ,  250 - pipe.y )
            self.rectangle( pipe.x , pipe.y - self.gap_bt_pipes , 30 ,  250 - self.gap_bt_pipes + pipe.y )


        # drawing targets
        for target in self.targets:
            up()
            goto( target.x,target.y )
            dot(30,'blue')
            up()

        # finally drawing the ship
        self.draw_ship()

        # drawing enemy_bullets
        for enemy_bullet,enemy_bullet_speed in self.enemy_bullets:
            up()
            goto(enemy_bullet.x,enemy_bullet.y)
            dot(5,'blue')
            dot(3,'red')
            up()


        # drawing bullets
        for bullet in self.bullets:
            up()
            goto(bullet.x,bullet.y)
            color('green')
            self.rectangle(bullet.x , bullet.y ,5 , 2 )
            color('black')
            #dot(5,'green')
            up()

        ''' all components drawn '''
        ''' checking for collisions between different components '''

        #collision of the ship with a pipe if yes stop the game

        for pipe in self.pipes:
            if pipe.x -10 < self.ship.x <= pipe.x+40  and (self.ship.y + 10 > pipe.y  or self.ship.y - 10 < pipe.y - self.gap_bt_pipes)  :
                self.finish()
                return

        # remove target and bullet on collision
        for bullet in self.bullets:
            for target in self.targets:
                if target.x - 15 < bullet.x < target.x + 15 and  target.y - 15 < bullet.y < target.y+15 :
                    #print('destroyed')
                    self.targets.remove( target )
                    self.bullets.remove( bullet )
                    self.score += 1
                    self.update_score()


        # stop game on ship's collision with enemy bullet
        for enemy_bullet,speed in self.enemy_bullets:
            if self.ship.x - 10 < enemy_bullet.x < self.ship.x + 10 and self.ship.y - 10 < enemy_bullet.y < self.ship.y + 10 :
                self.finish()
                return

        # stop game on collision with targets
        for target in self.targets:
            if self.ship.x - 25 < target.x < self.ship.x + 25 and self.ship.y - 25 < target.y < self.ship.y + 25 :
                self.finish()
                return

        # remove bullets on collision with pipes
        for bullet in self.bullets:
            for pipe in self.pipes:
                if pipe.x  <= bullet.x <= pipe.x+30  and (bullet.y > pipe.y or bullet.y < pipe.y - self.gap_bt_pipes)  :
                    #print('wasted')
                    self.bullets.remove(bullet )

        # take action on collision if enemy bullet with pipes
        for enemy_bullet,speed in self.enemy_bullets:
            for pipe in self.pipes:
                if pipe.x  <= enemy_bullet.x <= pipe.x+30  and (enemy_bullet.y > pipe.y or enemy_bullet.y < pipe.y - self.gap_bt_pipes)  :
                    #remove the bullet
                    self.enemy_bullets.remove( (enemy_bullet,speed) )
                    #uncomment if we want bullet ot reflect back
                    #speed.x = -speed.x

        update()
        ontimer(self.draw,50)


    ''' keyboard control functions '''

    # move ship up/down on pressing up / down
    def changey(self,value):
        if( abs(self.ship_pos['y'] + value) < 250 ):
            self.ship_pos['y'] += value


    # move ship left/right on pressing right/ left
    def changex(self,value):
        if( abs(self.ship_pos['x'] + value) < 500 ):
            self.ship_pos['x'] += value

    # fire a bullet on pressing spacebar
    def fire(self):
        self.bullets.append( vector(self.ship.x,self.ship.y) )

    def finish(self):
        up()
        self.ship.x = self.ship_pos['x']
        self.ship.y = self.ship_pos['y']
        goto( self.ship.x,self.ship.y )
        dot(20,'aquamarine')
        return


g = Game()
