from robot import *
from arena.tiles import *
import pdb


class MazeRunners():

	mapWidth = 10
	mapHeight = 10

	startX = mapWidth/2
	startY = mapHeight/2

	x = startX
	y = startY

	direction = Direction.Up

	IsAutonomous = True
	GoInitial = False

	IsDebugging = False


	def __init__(self):
		self.robot = Robot()
		self.map = self.NewMap(self.mapWidth, self.mapHeight)

	def NewMap(self, width, height):
		newMap = {}
		for x in range(width):
			for y in range(height):
				newMap[x, y] = TILE()
		return newMap

	def ScanFirstTile(self):
		self.robot.AlignToWall()

		#Setup Robot Positining Vars
		self.robot.BearOffSet = self.robot.compass.bearing255()
		self.robot.PichOffSet = self.robot.compass.pich()
		self.robot.RollOffSet = self.robot.compass.roll()

		self.RegisterTile()
		self.RotateLeft()
		self.RegisterTile()

	def Start(self):
		self.robot.RedLed.TurnOn()

		while self.robot.Switch2.IsOn() == False:
			self.robot.BlueLed.Blink()

		self.ScanFirstTile()

		while True:
			if self.GoInitial:
				break

			if self.IsAutonomous:
				if self.IsDebugging:
					pdb.set_trace()
				if self.NearVoidTile():
					self.RotateNextTile()
				else:
					self.MovePath(TileType.Void)
				self.RegisterTile()
		print "Moving to initial tile"
		self.MovePath(TileType.Starting)
		print "Maze Solved!"

	def MovePath(self, tileType):

		floodFill = FloodFill(self.mapWidth, self.mapHeight)
		floodFill.AddTile(self.x, self.y, 0, 0)

		TileFound = False

		lastTile = floodFill.GetFloodAt(0)[0]

		i = 0

		while TileFound == False:

			cFlood = floodFill.GetFloodAt(i)

			if len(cFlood) > 0:
				for floodTile in cFlood:

					if (tileType == TileType.Starting and floodTile.x == self.startX and floodTile.y == self.startY) or (self.map[floodTile.x, floodTile.y].tileType == tileType):
						TileFound = True
						lastTile = floodTile
						break

					Left = True if (self.map[floodTile.x - 1, floodTile.y].rightWall == Wall.No and (floodFill.tile[floodTile.x - 1][floodTile.y] == None or floodFill.tile[floodTile.x - 1][floodTile.y].i > i)) else False
					Right = True if (self.map[floodTile.x, floodTile.y].rightWall == Wall.No and (floodFill.tile[floodTile.x + 1][floodTile.y] == None or floodFill.tile[floodTile.x + 1][floodTile.y].i > i)) else False
					Bottom = True if (self.map[floodTile.x, floodTile.y].bottomWall == Wall.No and (floodFill.tile[floodTile.x][floodTile.y + 1] == None or floodFill.tile[floodTile.x][floodTile.y + 1].i > i)) else False
					Top = True if (self.map[floodTile.x, floodTile.y - 1].bottomWall == Wall.No and (floodFill.tile[floodTile.x][floodTile.y - 1] == None or floodFill.tile[floodTile.x][floodTile.y - 1].i > i)) else False
					
					
					if Bottom:
						if self.map[floodTile.x, floodTile.y + 1].tileType != TileType.Black:
							floodFill.AddTile(floodTile.x, floodTile.y + 1, i + 1, floodTile.id)

					if Right:
						if self.map[floodTile.x + 1, floodTile.y].tileType != TileType.Black:
							floodFill.AddTile(floodTile.x + 1, floodTile.y, i + 1, floodTile.id)

					if Left:
						if self.map[floodTile.x - 1, floodTile.y].tileType != TileType.Black:
							floodFill.AddTile(floodTile.x - 1, floodTile.y, i + 1, floodTile.id)

					if Top:
						if self.map[floodTile.x, floodTile.y - 1].tileType != TileType.Black:
							floodFill.AddTile(floodTile.x, floodTile.y - 1, i + 1, floodTile.id)

					lastTile = floodTile

			else:
				self.GoInitial = True
				return

			i += 1
			
		path = []

		originalLastTile = lastTile

		for i in range(1, floodFill.LastTileNumber + 1):

			lastTile = originalLastTile
			
			while lastTile.i > i:

				for floodTile in floodFill.GetFloodAt(lastTile.i - 1):
					if floodTile.id == lastTile.parentID:
						lastTile = floodTile
						break

			path.append(lastTile)


		for floodTile in path:
			self.MoveNextTile(floodTile)

		if tileType == TileType.Starting and self.x == self.startX and self.y == self.startY:
			self.IsAutonomous = False
			self.PrintMap()


	def NearVoidTile(self):
		nextVoidWalls = NextVoidTiles(True if self.map[self.x - 1, self.y].rightWall == Wall.Yes else False, True if self.map[self.x, self.y].rightWall == Wall.Yes else False, True if self.map[self.x, self.y - 1].bottomWall == Wall.Yes else False, True if self.map[self.x, self.y].bottomWall == Wall.Yes else False)
		nextVoidTiles = NextVoidTiles(True if self.map[self.x - 1, self.y].tileType == TileType.Void else False	, True if self.map[self.x + 1, self.y].tileType == TileType.Void else False, True if self.map[self.x, self.y - 1].tileType == TileType.Void else False, True if self.map[self.x, self.y + 1].tileType == TileType.Void else False)

		if (nextVoidWalls.Left == False and nextVoidTiles.Left):
			return True

		if (nextVoidWalls.Right == False and nextVoidTiles.Right):
			return True

		if (nextVoidWalls.Up == False and nextVoidTiles.Up):
			return True

		if (nextVoidWalls.Down == False and nextVoidTiles.Down):
			return True

		return False

	def RotateNextTile(self):
		nextVoidWalls = NextVoidTiles(True if self.map[self.x - 1, self.y].rightWall == Wall.Yes else False, True if self.map[self.x, self.y].rightWall == Wall.Yes else False, True if self.map[self.x, self.y - 1].bottomWall == Wall.Yes else False, True if self.map[self.x, self.y].bottomWall == Wall.Yes else False)
		nextVoidTiles = NextVoidTiles(True if self.map[self.x - 1, self.y].tileType == TileType.Void else False, True if self.map[self.x + 1, self.y].tileType == TileType.Void else False, True if self.map[self.x, self.y - 1].tileType == TileType.Void else False, True if self.map[self.x, self.y + 1].tileType == TileType.Void else False)

		if nextVoidWalls.Down == False and nextVoidTiles.Down:
				if self.direction == Direction.Up:
					self.RotateLeft()

				if self.direction == Direction.Left:
					self.RotateLeft()

				if self.direction == Direction.Right:
					self.RotateRight()

		elif nextVoidWalls.Right == False and nextVoidTiles.Right:
			if self.direction == Direction.Left:
				self.RotateLeft()

			if self.direction == Direction.Bottom:
				self.RotateLeft()

			if self.direction == Direction.Up:
				self.RotateRight()

		elif nextVoidWalls.Left == False and nextVoidTiles.Left:
			if self.direction == Direction.Right:
				self.RotateLeft()

			if self.direction == Direction.Up:
				self.RotateLeft()

			if self.direction == Direction.Bottom:
				self.RotateRight()

		else: #nextVoidWalls.Up == False and nextVoidTiles.Up:
			if self.direction == Direction.Bottom:
				self.RotateLeft()

			if self.direction == Direction.Right:
				self.RotateLeft()

			if self.direction == Direction.Left:
				self.RotateRight()

		self.MoveTile(checkVictims = True)


	def MoveNextTile(self, lastTile):

		if lastTile.x < self.x:

			if self.direction == Direction.Right:
				self.RotateLeft()

			if self.direction == Direction.Up:
				self.RotateLeft()

			if self.direction == Direction.Bottom:
				self.RotateRight()

			self.MoveTile()

		elif lastTile.x > self.x:

			if self.direction == Direction.Left:
				self.RotateLeft()

			if self.direction == Direction.Up:
				self.RotateRight()

			if self.direction == Direction.Bottom:
				self.RotateLeft()

			self.MoveTile()

		elif lastTile.y < self.y:

			if self.direction == Direction.Bottom:
				self.RotateLeft()

			if self.direction == Direction.Left:
				self.RotateRight()

			if self.direction == Direction.Right:
				self.RotateLeft()

			self.MoveTile()

		elif lastTile.y > self.y:

			if self.direction == Direction.Up:
				self.RotateLeft()

			if self.direction == Direction.Left:
				self.RotateLeft()

			if self.direction == Direction.Right:
				self.RotateRight()

			self.MoveTile()

	"""
	### Movement
	"""

	def MoveTile(self, checkVictims = False, ammount = 1):

		self.robot.MoveTile(CheckVictims = checkVictims, Ammount = ammount)

		if self.direction == Direction.Up:
			self.y -= ammount
		elif  self.direction == Direction.Right:
			self.x += ammount
		elif  self.direction == Direction.Bottom:
			self.y += ammount
		else:
			self.x -= ammount

	def RotateLeft(self):
		self.robot.RotateLeft()

		direction = self.direction
		self.direction = Direction.rotateLeft(direction)

		print "Rotated Left!"

	def RotateRight(self):
		self.robot.RotateRight()

		direction = self.direction
		self.direction = Direction.rotateRight(direction)

		print "Rotated Right!"

	"""
	### Tile Information
	"""

	def RegisterTile(self):
		self.RegisterWalls()

		self.map[self.x, self.y].tileType = self.robot.GetTileType()

		if self.map[self.x, self.y].tileType == TileType.Black:
			self.MoveTile(ammount = -1)

	def RegisterWalls(self):

		walls = self.robot.GetWalls()

		if self.direction == Direction.Up:
			self.RegisterWallsFromTop(walls)
		elif self.direction == Direction.Left:
			self.RegisterWallsFromLeft(walls)
		elif self.direction == Direction.Right:
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
		y = 0
		while y < self.mapHeight:
			line = ""
			line2 = ""
			x = 0
			while x < self.mapWidth:
				if self.map[x, y].tileType == TileType.Black:
					tileType = "x"
				elif self.map[x, y].tileType == TileType.Void:
					tileType = ":"
				else:
					tileType = " "
				if x == self.x and y == self.y:
					if self.direction == Direction.Up:
						tileType = "^" + tileType
					elif self.direction == Direction.Right:
						tileType = ">" + tileType
					elif self.direction == Direction.Left:
						tileType = "<" + tileType
					else:
						tileType = "v" + tileType
					tileType = "o" + tileType
				else:
					tileType += tileType + tileType
				line += (tileType)
				line2 += "___" if (self.map[x, y].bottomWall == Wall.Yes and x != 0) else "   "
				if self.map[x, y].rightWall == Wall.Yes and y != 0:
					line += "|"
					line2 += "|"
				else:
					line += " "
					if self.map[x, y].bottomWall == Wall.Yes and x != 0:
						line2 += "_"
					else:
						line2 += " "
				x += 1
			if y > 0:
				print line
			print line2
			y += 1
		print "X: ", self.x, " Y: ", self.y, " sX: ", self.startX, " sY: ", self.startY, " Direction: ", self.direction

	def Exit(self):
		self.robot.Exit()



maze = MazeRunners()

if maze.robot.Switch1.IsOn():
	maze.Start()

maze.Exit()