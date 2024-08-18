#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Implimentation notes

# dictionaries of PopObject's should use the object id as the key name

# Native populous imports
from pypulous.World import World
from pypulous.objects import *
from pypulous.team import *
from pypulous.lib.random import getRandom

# External modules

# Define some constants:
GRID_SQUARE_SIZE = 30 # px
FRAMES_PER_SECOND = 30
NATIVE_SPEED = 15 # pixels per second (pps)
# Times in seconds
NATIVE_SQUR_TRAVEL_TIME = GRID_SQUARE_SIZE / NATIVE_SPEED
NATIVE_BUILD_TIME = 1
NATIVE_THINK_TIME = 1
NATIVE_JOIN_TIME = 0

NATIVE_DROWN_TIME_WATER = 15
NATIVE_DROWN_TIME_SWAMP = 15


class Populous:
	def __init__ (self):
		self.update_interval = 25
		self.fps = 25
		# world settings
		self.world_width = 5
		self.world_height = 4
		self.team_count = 2 # not including the neutral team (id:0)
		self.teams = []
		self.world = None
		self.random = getRandom()

	def startGame(self):
		self.world = World(width=self.world_width, height=self.world_height)
		for i in range(self.team_count + 1):
			new_team = Team(i)
			self.teams.append(new_team)
		self.world.generateWorld(self.teams)

	# doLoop. Needs to be in a seperate thread?
	def doLoop(self):
		# Get queued user commands
		# for each object: object.act()
		# update display
		pass

	def getWinner(self):
		team_count = 0
		winner = None
		for t in self.teams:
			if not t.hasLost:
				team_count += 1
				winner = t
		if team_count > 1:
			return False
		else:
			return winner

	def endGame(self):
		pass

	def mouseToGameCoords(self, x, y):
		x -= x % GRID_SQUARE_SIZE
		gx = x / GRID_SQUARE_SIZE
		y -= y % GRID_SQUARE_SIZE
		gy = y / GRID_SQUARE_SIZE
		return (gx, gy)

	def queueCommand(self):
		pass


