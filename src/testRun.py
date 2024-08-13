#! /usr/bin/env python
# -*- coding: utf-8 -*-
import populous
import gui
import unittest
import random
import time
import sys, pygame

class Game:

	config = {}
	pop = None
	clock = None
	time_passed = 0
	total_time_passed = 0
	total_frames = 0
	gui = None
	play = False
	winner = None

	def __init__(self):
		self.loadConfig()
		self.init_game()
		self.clock = pygame.time.Clock()
		self.gui = gui.Gui(self.pop)
		self.populate_world()

	def loadConfig(self):
		self.config = {
			'width': 3,
			'height': 3,
			'teams': 2
			}

	def init_game(self, width=None, height=None):
		self.pop = populous.Populous()
		self.pop.world_width = width or self.config['width']
		self.pop.world_height = height or self.config['height']
		self.pop.startGame()
		self.world = self.pop.world
		return self.pop

	def populate_world(self):
		return self._do_tiny_world()
		game = self.pop
		world = self.pop.world
		team1 = self.pop.teams[1]
		team2 = self.pop.teams[2]
		man1 = populous.Native(world, 0, 1, team1)
		home1 = populous.House(world, 0, 0, team1)
		idol1 = populous.Idol(world, 4, 3, team1)
		# Team 2
		man2 = populous.Native(world, world.width-1, world.height-2, team2)
		home2 = populous.House(world, world.width-1, world.height-1, team2)
		idol2 = populous.Idol(world, world.width-5, world.height-3, team2)
		return (man1, home1, idol1) , (man2, home2, idol2)

	def _do_tiny_world(self):
		game = self.pop
		world = self.pop.world
		team1 = self.pop.teams[1]
		team2 = self.pop.teams[2]
		man1 = populous.Native(world, 1, 0, team1)
		home1 = populous.House(world, 0, 0, team1)
		idol1 = populous.Idol(world, 2, 0, team1)
		# Team 2
		man2 = populous.Native(world, 1, 2, team2)
		home2 = populous.House(world, 0, 2, team2)
		idol2 = populous.Idol(world, 2, 2, team2)
		return (man1, home1, idol1) , (man2, home2, idol2)


	def print_grid(self):
		land = self.pop.world
		for x in land.grid:
			for y in x:
				print(y.objects),
			print('\n'),

	def start(self):
		self.play = True;
		self.loop()
		self.end()

	def loop(self):
		while self.play:
			self.processEvents()
			self.tick()
			self.processWorld()
			self.processObjects()
			self.checkState()
			self.processGUI()

	def processEvents(self):
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.end()

	def processMouseEvents(self):
		# Deal with the mouse:
		#mouse_coords = pygame.mouse.get_pos()
		#print mouse_coords
		#game_coords = game.mouseToGameCoords(mouse_coords[0], mouse_coords[1])
		#print game_coords
		#print world.inspectPos(game_coords[0], game_coords[1])
		pass

	def tick(self):
		time_passed = self.clock.tick(40)
		self.time_passed = time_passed / 1000.0
		self.total_time_passed += self.time_passed
		self.total_frames += 1
		print( "Clock Tick: ",time_passed,"ms, ",self.time_passed,"s")
		print( "FPS: ", (self.total_frames / self.total_time_passed))

	def processWorld(self):
		self.world.checkObjects()
		for t in self.pop.teams:
			if t.id > 0:
				t.checkHasLost()
				t.checkTeamGoal()

	def processObjects(self):
		world = self.pop.world
		for i in world.objects.keys():
			try:
				world.objects[i]
			except KeyError:
				print ("Key error encountered in processObjects. Index: ",i)
			else:
				try:
					world.objects[i].act()
				except Exception as ex:
					print ("<<< Fatal Error: %(error)s >>>" % { 'error': ex})
					print ("Object index:",i)
					self.play = False

	def checkState(self):
		winner = self.pop.getWinner()
		print ("have winner : ", ((winner and 'true') or 'false'))
		if winner:
			self.winner = winner
			self.play = false;

	def processGUI(self):
		self.gui.draw(self.time_passed)

	def end(self):
		print ("\n\n\t\tGAME OVER\n\n")
		print( "\n\nTeam \"%(team)s\" has won!\n\n" % {'team':self.winner})
		if self.winner == None:
			for t in self.pop.teams:
				populous.log(t, "Has: ")
				for i, o in t.objects.items():
					str = "%s %s" % (o, (o.is_alive and 'alive') or 'dead')# TODO
					populous.log(str)



def main():
	populous.set_debug(True)
	game = Game()
	game.start()
	sys.exit()

if __name__ == '__main__':
		main()



