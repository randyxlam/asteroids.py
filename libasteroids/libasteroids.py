#!/usr/bin/env python

from pygame import *
from random import random
from math import fabs,sin,cos,radians
import sys, Image

#make the screen, and background objects.
screen = display.set_mode((1020,600))
display.set_caption('Asteroids')
background = image.load('libasteroids/starback.png')

#define a Sprite class. I'm calling any image that moves around on screen a "Sprite". Sprites are going to have all the basic movement and image loading functions, and my more specific objects like Asteroid() and Ship() will inherit the Sprite class.
class Sprite:
	#when an object of this class is made, python checks to see if the class has an __init__() function and if it does, runs it. It's like constructors from Java. That being said, this __init__() function is going to have to be called by me manually, because I never actually plan on making a plain old Sprite()...only certain types of Sprites :P
	def __init__(self,picture):
		#K, another object oriented programming thing. 'self' refers to any object that's being made out of this. So...outside of this class, in the main program, we can find the x-coordinate of the "playership" object (which is a type of Sprite()) with 'playership.x'. Or the x-coordinate of a particular asteroid can be found with asteroids[0].x. A class is a template with which to make objects. But while we're defining the template, we use the generic 'self'
		self.x = 0
		self.y = 0
		self.angle = 0
		#I decided to use a cartesian system to define the velocity. Just a vector ;)
		self.velocity = [0,0]
		#self.bitmap refers to the actual image that the object looks like...I guess its appearance.
		self.bitmap = image.load('libasteroids/'+picture)
		self.width = Image.open('libasteroids/'+picture).size[0]
		self.height = Image.open('libasteroids/'+picture).size[1]
		#the reason I make this variable, is because we're going to be doing a bunch of crap to self.bitmap...rotating it and shifting it, etc, etc. However, if you perform a bunch of transformations to the same image again and again, the quality will go down quite a bit. (In the earlier versions of this program, when I rotated the ship, it basically melted away, looked kind of cool...but not the goal here :P) So now, every time I perform a transformation I take it on the original image, so it's never distorted more than once.
		self.original = self.bitmap
	#lol..this part makes sure Newton's first law holds. Well, the last two lines do that. The rest of it is to make it come in the other side if it goes offscreen. 
	def drift(self):
		if self.x > 1020:
			self.x = -self.width
			self.y = 600 - self.y
		if self.x < 0-self.width:
			self.x = 1020
			self.y = 600 - self.y
		if self.y < -50 - self.height:
			self.x = 1020 - self.x
			self.y = 600
		if self.y > 600:
			self.x = 1020 - self.x
			self.y = 0 - self.height
		self.x += self.velocity[0]
		self.y -= self.velocity[1]
	#in all reality, this function is a bit silly. It returns the angle that the ship is at. The only reason that it's necessary, is that the rotation function provided by pygame zeroes at 90 degrees instead of 0 degrees in terms of the standard circle. self.angle is in terms of pygame's coordinate system, but I have to do trig in some parts, so it needs to translate self.angle into what the actual angle is, in standard coordinates.
	def get_angle(self):
		angle = self.angle+90
		if angle >= 360:
			angle -= 360
		if angle <= 360:
			angle += 360
		return angle
	def accelerate(self,acceleration):
		#see, here you are :P. The accelerate() function that I made needs to use the angle in terms of standard coordinates, while the spin() function below, needs pygame's retarded coordinate system. 
		angleReal = self.get_angle()
		self.velocity[0] += acceleration*cos(radians(angleReal))
		self.velocity[1] += acceleration*sin(radians(angleReal))
	#the render function. It just makes sure that the object drifts naturally before blitting its image to the screen.
	def render(self):
		self.drift()
		screen.blit(self.bitmap,(self.x,self.y))
	def spin(self,change):
		center = self.bitmap.get_rect().center
		rotate = transform.rotate
		self.angle += change
		if fabs(self.angle) >= 360:
			self.angle = 0
			self.bitmap = self.original
		else:
			#like I said, we're always performing transformations on the original image, so as not to degrade quality
			self.bitmap = rotate(self.original, self.angle)
		#the reason that the next few lines (and the first line) are necessary is kinda complicated...Ehm, so basically images are ALWAYS rectangular right? If they are some other shape, then they're really just rectangles with transparency in some parts. So, when you rotate the ship sideways, the top point of the ship goes outside its original rectangle right? Which means that its rectangle has to extend. Also, when rotating, the anchor point or "location" of the image is based, quite logically, on the upper left hand corner of the image. But as the rectangle is changing size, it would mean that the ship would bounce around a bit while rotating. Grr...I might have to show you this in person, I'm not sure if I would get it if I hadn't seen it. Anyway, what I'm effectively doing is anchoring the image based on its center instead of its corner, which makes it just rotate, not bounce around.
		newcenter = self.bitmap.get_rect().center
		self.x -= newcenter[0]-center[0]
		self.y -= newcenter[1]-center[1]
#K, so here's the Ship class, it inherits the Sprite class because all Ship()s are Sprite()s. Understand? There are very few changes because originally I just had a Ship class, until I realised that the Asteroid()s are really similar and I would end up retyping a lot of code. Basically the only thing that Ship()s do that Sprite()s don't is that the Ship() always starts in the center. So Ship() just gets all the attributes of Sprite() then redefines self.x and self.y
class Ship(Sprite):
	def __init__(self):
		#K, so like I said above, we have to run the Sprite.__init__() function manually, because I never make a plain old Sprite(). When I make a Ship(), this Ship.__init__() function is run automatically, and then I make that go to Sprite.__init__(), so it accomplishes the same thing.
		Sprite.__init__(self,'spaceship.png')
		self.x = 1020/2 - 74/2
		self.y = 600/2 - 102/2
	#now I realise that if I were being really consistent, I should make a Ship.shoot() function, because Ship()s do that too. But I handle that differently, in the main program. I guess I abandoned object oriented programming for a while :'(

#And here's the Asteroid class! :D As you can see, all Asteroid()s are also Sprite()s
class Asteroid(Sprite):
	#K, so the variable speedMultiplier is constant across ALL Asteroid()s...which is why I didn't declare it like "self.speedMultiplier = 3" which would mean that EACH Asteroid() has their own copy. This way, when I want to change it, say, Asteroid.speedMultiplier *= 2, it will change it for all the Asteroid()s at once.
	speedMultiplier = 3
	def __init__(self):
		#so, here we're making a bunch of attributes for asteroids. Most of them are random, because they appear randomly. The random() function returns a random number between 0 and 1
		Sprite.__init__(self,'asteroid.png')
		self.angle = random()*360
		self.angularVelocity = random()*12 - 6
		choice = random()
		#Basically I make it so that Asteroid()s don't appear in the middle 420 pixels. (for the x-coordinate) This means that they won't appear on top of your ship by accident and end the game immediately...which would suck.
		if choice >= 0.5:
			self.x = random()*300
		else:
			self.x = 1020 - random()*300
		self.y = random()*600
		#so, Asteroid.speedMultiplier exists to allow me to ramp up the AVERAGE speed of asteroids when levels get higher. Although, theoretically, it is still possible to get a completely stationary asteroid...just of probability about 10^(-18)...I'll explain how I got that in person
		self.velocity = [random()*2*Asteroid.speedMultiplier - Asteroid.speedMultiplier,random()*2*Asteroid.speedMultiplier - Asteroid.speedMultiplier]
		Sprite.spin(self,0)
	def drift(self):
		#so, the only difference between Asteroid.drift() and Sprite.drift() is that Asteroid()s might also spin randomly, which other Sprite()s don't do.
		Sprite.drift(self)
		self.spin(self.angularVelocity)

#K, so here's the Shot class. Notice that Shot()s are NOT Sprite()s. If I had been thinking ahead, I probably would have made Sprite more general so that Shot could have inherited it, but, by the time I got here...Sprite()s did some things that Shot()s didn't do. Shot()s do not loop around when they go offscreen, they disappear. That's actually the main difference. Also, Shot()s are very simple, so I really didn't need to add lots of code, they never accelerate or anything like that.
class Shot:
	#K, so Shot()s need to know which Ship() they came from, so they can inherit its angle. (A Shot() will go in the direction that its Ship() is pointing, and will start in the same place.)
	def __init__(self,mothership):
		self.speed = 10
		self.angle = mothership.get_angle()
		self.bitmap = image.load('libasteroids/shot.png')
		self.x,self.y = mothership.bitmap.get_rect().center
		self.x += mothership.x
		self.y += mothership.y
		self.velocity = [0,0]
		self.velocity[0] = self.speed*cos(radians(self.angle))
		self.velocity[1] = self.speed*sin(radians(self.angle))
	def update(self):
		self.x += self.velocity[0]
		self.y -= self.velocity[1]			
	def render(self):
		screen.blit(self.bitmap,(self.x,self.y))
#w00t! So here's the intersect() function. I was having some issues with the actual image versus visible image thing again, so basically what happens is that if any part of sprite1 runs into the CENTER of sprite2, then it returns 1 (true). Otherwise it returns 0(false). This was the least image-specific way I could see to do it, and it works pretty well.
def intersect(sprite1,sprite2):
	(center2x,center2y) = sprite2.bitmap.get_rect().center
	center2x += sprite2.x
	center2y += sprite2.y
	if(sprite1.x > center2x - sprite1.width) and (sprite1.x < center2x) and (sprite1.y < center2y) and (sprite1.y > center2y -sprite1.height):
		return 1
	else:
		return 0
#Alright! Here's the increaseLevel function. As you can see, it adds 1 to the level, and, every third level, it adds 1 to the asteroid's speed multiplier...I should probably make that moreso. Also, it deletes all current asteroids(there shouldn't be any anyway, unless the user increased the level manually.) and makes a number of new Asteroid()s equal to the level. Then it sends asteroids and level back to the original program
def increaseLevel(level,asteroids):
	level += 1
	if level % 3 == 0:
		Asteroid.speedMultiplier += 1
	asteroids = []
	#Yea, so this is equivilant to the Java for loop:
	#for(int x = 0;x < level;x++)
	#{
	#	asteroids.append(Asteroid())
	#}
	#Basically, range(level) makes an array to iterate over [0,1,2,...level-1]
	for x in range(level):
		asteroids.append(Asteroid())
	return level,asteroids


