#! /usr/bin/env python
# -*- coding: utf-8 -*-
import populous
import gui
import unittest
import random
import time
import sys, pygame


def test_start(width=10, height=10):
	game = populous.Populous()
	game.world_width = width
	game.world_height = height
	game.startGame()
	return game

def create_objects(game):
	world = game.world
	team1 = game.teams[1]
	team2 = game.teams[2]
	man1 = populous.Native(world, 0, 1, team1)
	home1 = populous.House(world, 0, 0, team1)
	idol1 = populous.Idol(world, 4, 3, team1)
	# Team 2
	man2 = populous.Native(world, world.width-1, world.height-2, team2)
	home2 = populous.House(world, world.width-1, world.height-1, team2)
	idol2 = populous.Idol(world, world.width-5, world.height-3, team2)
	return (man1, home1, idol1) , (man2, home2, idol2)

def print_grid(land):
	for x in land.grid:
		for y in x:
			print y.objects,
		print '\n',

def main():
	populous.set_debug(True)
	clock = pygame.time.Clock()
	game = test_start()
	world = game.world
	window = gui.Gui(game)
	team1 = game.teams[1]
	team2 = game.teams[2]
	create_objects(game)
	print_grid(world)
	team1.goal = 'leader'
	team2.goal = 'leader'

	go_on = True

	while go_on:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
		else:
			# Deal with the mouse:
			#mouse_coords = pygame.mouse.get_pos()
			#print mouse_coords
			#game_coords = game.mouseToGameCoords(mouse_coords[0], mouse_coords[1])
			#print game_coords
			#print world.inspectPos(game_coords[0], game_coords[1])

			time_passed = clock.tick(40)
			time_passed_seconds = time_passed / 1000.0
			for i in world.objects.keys():
				try:
					world.objects[i]
				except KeyError:
					pass
				else:
					try:
						world.objects[i].act()
					except Exception as ex:
						print "Fatel Error: %(error)s" % { 'error': ex}
				if team1.leader and team1.goal != 'build':
					team1.goal = 'build'
				if team2.leader and team2.goal != 'build':
					team2.goal = 'build'
				window.draw(time_passed_seconds)

		winner = game.getWinner()
		if winner:
			print "\n\nTeam \"%(team)s\" has won!\n\n" % {'team':winner}
			sys.exit()

if __name__ == '__main__':
		main()



