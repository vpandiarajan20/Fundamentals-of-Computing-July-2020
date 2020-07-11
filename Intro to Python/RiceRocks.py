# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
angular_acceleration = 0.1
acceleration = 0.2
friction = 0.97
vectors = [0,0]
started = False
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if(self.thrust):
            #135 is center of ship image w/ thrusters
            self.image_center[0] = 135 
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            #45 is center of ship image w/o thrusters
            self.image_center[0] = 45
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def keydown(self,key):
        if(started):
            if(key == simplegui.KEY_MAP["left"]):
                self.angle_vel -= angular_acceleration
            if(key == simplegui.KEY_MAP["right"]):
                self.angle_vel += angular_acceleration
            if(key == simplegui.KEY_MAP["left"] and key == simplegui.KEY_MAP["right"]):
                return None
            if(key == simplegui.KEY_MAP["up"]):
                self.thrust = True
                ship_thrust_sound.play()
            
    def keyup(self,key):
        if(key == simplegui.KEY_MAP["up"]):
            self.thrust = False
            ship_thrust_sound.rewind()
        if(key == simplegui.KEY_MAP["left"]):
            self.angle_vel = 0
        if(key == simplegui.KEY_MAP["right"]):
            self.angle_vel = 0
        if(key == simplegui.KEY_MAP["left"] and key == simplegui.KEY_MAP["right"]):
            return None
        if(key == simplegui.KEY_MAP["space"]):
            self.shoot()

    def update(self):
        global vectors
        vectors = angle_to_vector(self.angle)
        if(self.thrust):
            self.vel[0] += vectors[0] * acceleration
            self.vel[1] += vectors[1] * acceleration
        if(not self.vel[0] == 0):
            self.vel[0] *= friction
        if(not self.vel[1] == 0):
            self.vel[1] *= friction
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT 
        self.angle += self.angle_vel
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius       
    
    def shoot(self):
        global missile_group
        missile_group.add(Sprite([self.pos[0] + vectors[0]*self.image_size[0]/2, self.pos[1] + vectors[1]*self.image_size[1]/2], [self.vel[0] + 15*acceleration*vectors[0], self.vel[1] + 15*acceleration*vectors[1]], self.angle, 0, missile_image, missile_info, missile_sound))
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT 
        self.angle += self.angle_vel
        self.age += 1
        if(self.age >= self.lifespan):
            return True
        return False
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def collide(self,other_object):
        if(dist(self.get_position(),other_object.get_position()) <= self.get_radius() + other_object.get_radius()):
            return True
        return False

#resetting after bringing up splash screen
def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        time = 0
        score = 0
        lives = 3
        soundtrack.rewind()
        soundtrack.play()

def group_collide(group, other_object):
    for x in set(group):
        if(x.collide(other_object)):
            group.remove(x)
            return True
    return False
def group_group_collide(group, other_group):
    count = 0
    for x in set(group):
        if(group_collide(other_group,x)):
            group.discard(x)
            count += 1
    return count

def draw(canvas):
    global time, lives, score, started
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    if (not started):
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], splash_info.get_size())
    else:
        canvas.draw_text("Your score is " + str(score), (550, 100), 20, 'White')
        canvas.draw_text("You have " + str(lives) + " lives left", (100, 100), 20, 'White')
        # draw ship and sprites
        my_ship.draw(canvas)
        process_sprite_group(missile_group, canvas)
        process_sprite_group(rock_group, canvas)
        if(group_collide(rock_group, my_ship)):
            lives -= 1
        if(lives <= 0):
            started = False
            soundtrack.rewind()
        group_collide(rock_group, my_ship)
        score += group_group_collide(missile_group, rock_group)
        # update ship and sprites
        my_ship.update()

    
# helper function for processing sprite groups
def process_sprite_group(group,canvas):
    for sprite in set(group):
        if(sprite.update()):
            group.remove(sprite)
            return None
        sprite.draw(canvas)
        sprite.update()
        
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    if(not started):
        rock_group = set()
    elif(len(rock_group) < 12):
        x = Sprite([random.randint(0, WIDTH), random.randint(0, HEIGHT)], [random.randint(-1, 1), random.randint(-1, 1)], 0, random.randint(-10, 10)*0.02, asteroid_image, asteroid_info)
        if(dist(x.get_position(),my_ship.get_position()) < x.get_radius() + my_ship.get_radius() + 4):
            return None
        rock_group.add(x)
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set()
missile_group = set()

# register handlers
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(click)
frame.set_keydown_handler(my_ship.keydown)
frame.set_keyup_handler(my_ship.keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)
# get things rolling
timer.start()
frame.start()