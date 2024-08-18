#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys, pygame
from pathlib import Path
from  pypulous.populous import Populous
import pypulous.objects
pygame.init()

"""
Need a number of panes

1. The world view. Interact with the world here. This is the biggest section.
2. God Controls.  Buttons for each of the possible actions the Player can make on the world
	a. Info Panel - Shows info on a selected native. (the shield)
	b. Miracle commands - These take power to use
	c. Tribe commands - How the God directs his natives.
3. Menu bar - basic game functions
4. Message Bar.
	a. In Single player show status messages, debug statements etc.
	b. Multi-player - can also send and receive messages from other players
5. Power bar ???? ?
6. Debug stats
"""


class Gui():
	square_size = 30, 30
	speed = [1, 1]
	black = 0, 0, 0
	green = 0, 255, 0
	blue = 0, 0, 255
	red = 255, 0, 0

	def __init__(self, game):
		self.game = game
		self.world = game.world
		self.game_size = self.world.width, self.world.height
		self.size = self.square_size[0] * self.game_size[0], self.square_size[1] * self.game_size[1]
		self.screen = pygame.display.set_mode(self.size)
		self.cache = []
		self.teams = []
		for i in range(self.game.team_count + 1):
			self.teams.append(dict())

	def draw(self, seconds_passed=0):
		self.screen.fill(Gui.black)
		for i in self.world.objects:
			obj = self.world.objects[i]
			if (not obj.is_alive):
				continue
			image = self.getImage(obj)
			rect = image.get_rect()
			rect.left = obj.x * Gui.square_size[0]
			rect.top = obj.y * Gui.square_size[1]
			self.screen.blit(image, rect)
		pygame.display.flip()

	def getImage(self, obj):
		runPath = os.path.realpath(__file__)
		full_path = os.path.join('images', obj.file_name)
		if not full_path:
			raise Exception('Cannot find image name')
		image = pygame.image.load(full_path)
		return image

	def getImageFromCache(self, obj):
		pass

	def getImageFromObj(self, obj):
		pass

	def preLoadImages(self):
		# need a struct for each team
		# have a dict for each team
		# key for each object enountered
		# value is the cached image
		pass


if __name__ == '__main__':
	import objects
	game = Populous()
	game.startGame()
	world = game.world
	man = objects.Native(world, 1, 1)
	world.printGrid()
	window = Gui(world)
	window.draw()
	input("Any key to quit.")

