#! /usr/bin/env python

import sys, pygame
import populous
import objects
pygame.init()

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
		for i in range(self.game.team_count + 1):
			self.game.teams.append(dict())

	def draw(self, seconds_passed=0):
		self.screen.fill(Gui.black)
		for i in self.world.objects:
			obj = self.world.objects[i]
			image = self.getImage(obj)
			rect = image.get_rect()
			rect.left = obj.x * Gui.square_size[0]
			rect.top = obj.y * Gui.square_size[1]
			self.screen.blit(image, rect)
		pygame.display.flip()

	def getImage(self, obj):
		team_no = obj.team.id
		obj_type = type(obj)
		data_dir = '../images/'
		full_path = data_dir + obj.file_name
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
	game = populous.Populous()
	game.startGame()
	world = game.world
	man = objects.Native(world, 1, 1)
	world.printGrid()
	window = Gui(world)
	window.draw()
	raw_input("Any key to quit.")

