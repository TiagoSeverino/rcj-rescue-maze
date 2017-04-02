from robot import Robot

from arena.tiles import *

class MazeRunners():

	mapWidth = 10
	mapHeight = 10

	startX = mapWidth/2
	startY = mapHeight/2

	x = startX
	y = startY

	Direction = 1

	def __init__(self):
		self.robot = Robot()
		self.map = self.NewMap(self.mapWidth, self.mapHeight)

	def NewMap(self, width, height):
		newMap = {}
		for x in range(width):
			for y in range(height):
				newMap[x, y] = TILE()
		return newMap

	def Start(self):
		self.RegisterWalls()
		self.RegisterTile()
		self.RotateLeft()
		self.RegisterWalls()

		while True:
			self.MoveNextTile()

	def MoveNextTile(self):
		(wallLeft, wallFront, wallRight) = self.robot.GetWalls()

		if wallLeft == False:
			self.RotateLeft()
			self.MoveTile()
		elif wallFront == False:
			self.MoveTile()
		elif wallRight == False:
			self.RotateRight()
			self.MoveTile()
		elif wallFront:
			self.RotateLeft()

	"""
	### Movement
	"""

	def MoveTile(self):
		self.robot.MoveTile()

		if self.Direction == 0:
			self.y -= 1
		elif  self.Direction == 1:
			self.x += 1
		elif  self.Direction == 2:
			self.y += 1
		else:
			self.x -= 1

		self.RegisterWalls()
		self.RegisterTile()

		print "Moved 1 Tile!"

	def RotateLeft(self):
		self.robot.RotateLeft()

		if self.Direction > 0:
			self.Direction -= 1
		else:
			self.Direction = 3

		print "Rotated Left!"

	def RotateRight(self):
		self.robot.RotateRight()

		if self.Direction < 3:
			self.Direction += 1
		else:
			self.Direction = 0

		print "Rotated Right!"

	"""
	### Tile Information
	"""

	def RegisterTile(self):
		self.map[self.x, self.y].tileType = TileType.White

	def RegisterWalls(self):

		walls = self.robot.GetWalls()

		print walls

		if self.Direction == Direction.Up:
			self.RegisterWallsFromTop(walls)
		elif self.Direction == Direction.Left:
			self.RegisterWallsFromLeft(walls)
		elif self.Direction == Direction.Right:
			self.RegisterWallsFromRight(walls)
		else:
			self.RegisterWallsFromBottom(walls)

		self.PrintMap()

	def RegisterWallsFromTop(self, walls):
		(wallLeft, wallFront, wallRight) = walls

		self.map[self.x - 1, self.y].rightWall = Wall.Yes if wallLeft else Wall.No
		self.map[self.x, self.y - 1].bottomWall = Wall.Yes if wallFront else Wall.No
		self.map[self.x, self.y].rightWall = Wall.Yes if wallRight else Wall.No

	def RegisterWallsFromLeft(self, walls):
		(wallLeft, wallFront, wallRight) = walls

		self.map[self.x, self.y].bottomWall = Wall.Yes if wallLeft else Wall.No
		self.map[self.x - 1, self.y].rightWall = Wall.Yes if wallFront else Wall.No
		self.map[self.x, self.y - 1].bottomWall = Wall.Yes if wallRight else Wall.No

	def RegisterWallsFromRight(self, walls):
		(wallLeft, wallFront, wallRight) = walls

		self.map[self.x, self.y - 1].bottomWall = Wall.Yes if wallLeft else Wall.No
		self.map[self.x, self.y].rightWall = Wall.Yes if wallFront else Wall.No
		self.map[self.x, self.y].bottomWall = Wall.Yes if wallRight else Wall.No

	def RegisterWallsFromBottom(self, walls):
		(wallLeft, wallFront, wallRight) = walls

		self.map[self.x, self.y].rightWall = Wall.Yes if wallLeft else Wall.No
		self.map[self.x, self.y].bottomWall = Wall.Yes if wallFront else Wall.No
		self.map[self.x - 1, self.y].rightWall = Wall.Yes if wallRight else Wall.No

	def PrintMap(self):
		for y in range(self.mapHeight):
			line = ""
			for x in range(self.mapWidth):
				if self.map[x, y].bottomWall == Wall.Yes:
					line += "_"
				else:
					line += " "
				if self.map[x, y].rightWall == Wall.Yes:
					line += "|"
				else:
					line += " "
			print line

	def Exit(self):
		self.robot.Exit()


try:
	maze = MazeRunners()
	maze.Start()
except:
	maze.PrintMap()
	maze.Exit()

	
	