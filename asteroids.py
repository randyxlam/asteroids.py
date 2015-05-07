#!/usr/bin/env python

from pygame import *
import sys, os
#the next few lines allow this script to find the libasteroids module. As it is not a standard module, it is not stored in the standard directories. In all reality, I'm sure there's an easier way to do this, and the following three lines would not be necessary if I just put libasteroids.py in the same directory as this script...but I'm OCD like that :S
pathname = os.path.dirname(sys.argv[0])
fullpath = os.path.abspath(pathname)
sys.path.append(fullpath+'/libasteroids')
#I made this one
from libasteroids import *

#start the game. The init() function is specific to pygame
init()
#create a Ship() object
playership = Ship()
#create an empty array to hold all of the ship's shots when it fires
shots = []
gameover = 0
#create an array with one Asteroid() object. Unlike the 'playership' object above, this object is unnamed
asteroids = [Asteroid()]
#create two font objects. infofont is the font for the score and level. overfont is for the game over message
infofont = font.Font(None,60)
overfont = font.Font(None, 80)
score = 0
#create three mixer.Sound() objects, crasheffect for when an asteroid hits the ship, hiteffect for when a shot hits an asteroid, and shooteffect for when the ship fires a shot.
crasheffect = mixer.Sound('libasteroids/explosion.wav')
hiteffect = mixer.Sound('libasteroids/hit.wav')
shooteffect = mixer.Sound('libasteroids/laser.wav')
level = 1
maxscore = 0
quit = 0
#these are two variables to keep track of the time in between shots they are used later in the program.
timeold = 0
timenew = 0

#the main game loop. when it exits, so does the game.
while quit == 0:
	#'blitting' is the process of copying one image on top of another. The 'screen' and 'background' objects didn't come out of nowhere, they are defined in the first few lines of libasteroids.py. See them there.
	screen.blit(background,(0,0))
	#this renders the ship on the screen. Ship.render() is a method that I made. It uses the blit() function just like above. It just does some other stuff that I want it to do as well.
	playership.render()
	#for loops in python are different from most other languages. They are like a foreach loop in PERL. 'asteroid' is a loop variable being defined right there. Just like how we always used 'i' to keep track of where we were in Java. asteroids is an array that holds all the Asteroid() objects. So what the next line says is, for every item in the asteroids array, assign its value to 'asteroid' then do the following. Whereas other languages' for loops iterate over a range of numbers, python's for loops iterate over the elements in an array.
	for asteroid in asteroids:
		asteroid.render()
		#intersect() is another function I made in libasteroids.py What it does should be pretty clear :P
		if intersect(playership,asteroid):
			gameover = 1
		#same thing here. 'shot' is the loop variable that's being defined with each iteration. 'shots' is the array that the loop is iterating over.
		for shot in shots:
			if intersect(asteroid,shot):
				asteroids.remove(asteroid)
				shots.remove(shot)
				mixer.Sound.play(hiteffect)
				score += 10
	#The next line means, if there are no asteroids left.
	if asteroids == []:
		#then increase the level of the game. Hmm, the way I did this is not the prettiest though. I think I may change it soon.
		(level,asteroids) = increaseLevel(level,asteroids)
	#make text objects for the level and score. Then blit them onto the screen
	scoretext = infofont.render('Score:'+str(score),True,(255,255,255),(0,0,0))
	screen.blit(scoretext,(5,5))
	leveltext = infofont.render('Level:'+str(level),True,(255,255,255),(0,0,0))
	screen.blit(leveltext,(800,5))

	#key.get_pressed() is a function provided by pygame that makes a dictionary (a dictionary is an array that sorts its elements by words instead of numbers) with all of the keys that are currently being held down. So, if the right arrow is being held, then key.get_pressed()[K_RIGHT] will be true.
	pressed_keys = key.get_pressed()
	#event.get() returns an array of all of the current event objects.
	for ourevent in event.get():
		#the event of type 'QUIT' happens when you close the window, with either the 'x' button, or a hotkey
		if ourevent.type == QUIT:
			quit = 1
		#whenever someone hits a key an event of type 'KEYDOWN' happens. Note, this only happens once, WHEN they press it down, not if it's being held down, which is why the later bit about pressed_keys() and all that is necessary.
		if ourevent.type == KEYDOWN:
			if ourevent.key == K_SPACE:
				#time.get_ticks() is a function from pygame that returns the number of milliseconds since the game started. The next two lines make sure that a second has passed since the last shot was fired. Otherwise the game would be too easy :P
				timenew = time.get_ticks()
				if timenew-timeold >= 1000:
					#When a shot is fired, play the shooteffect sound, and add ("append") a Shot() object to the shots array.
					mixer.Sound.play(shooteffect)
					shots.append(Shot(playership))
					#this effectively resets the timer.
					timeold = time.get_ticks()
			#if someone presses the 'i' key, then increase the level
			if ourevent.key == K_i:
				(level,asteroids) = increaseLevel(level,asteroids)
	if gameover==1:
		overtext = overfont.render('Gameover',True,(255,255,255),(255,0,0))
		screen.blit(overtext,(360,260))
		#update the display to account for all the crap that's been blitted on. Delay for 4 seconds, then quit the game.
		display.update()
		mixer.Sound.play(crasheffect)
		time.delay(4000)
		quit = 1
	#This next bit is pretty English. It's all functions that I made.
	if pressed_keys[K_RIGHT]:
		playership.spin(-4)
	if pressed_keys[K_LEFT]:
		playership.spin(4)
	if pressed_keys[K_UP]:
		playership.accelerate(0.5)
	#hmmm, why is the "if shots" bit there...I don't think it's necessary...meh.
	if shots:
		for shot in shots:
			shot.update()
			#If the shots go too far offscreen remove them from the array. Otherwise they'd keep going on forever...and would suck up a lot of memory.
			if shot.x > 1120 or shot.y > 700 or shot.x < -100 or shot.y < -100:
				shots.remove(shot)
			else:			
				shot.render()
	#update the display with all the stuff that's been blitted during the course of the main loop. Then, delay by 5 milliseconds to make sure that the game doesn't just go as fast as it can and suck up all of your processing power.
	display.update()
	time.delay(5)
