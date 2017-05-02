class TILE():
	def __init__(self):
		self.tileType = TileType.Void
		self.rightWall = Wall.Unknown
		self.bottomWall = Wall.Unknown
		self.ramp = False

class TileType:
	Void = 0
	White = 1
	Black = 2
	Starting = 3

class Wall:
	Unknown = 0
	No = 1
	Yes = 2

class Direction:
	Up = 0
	Right = 1
	Bottom = 2
	Left = 3

	@staticmethod
	def rotateLeft(direction):
		if direction > Direction.Up:
			direction -= 1
		else:
			direction = Direction.Left

		return direction

	@staticmethod
	def rotateRight(direction):
		if direction < Direction.Left:
			direction += 1
		else:
			direction = Direction.Up

		return direction

class NextVoidTiles():
	VoidTiles = 0
	def __init__(self, left, right, up, down):
		self.Left = left
		self.Right = right
		self.Up = up
		self.Down = down

		if left:
			self.VoidTiles += 1

		if right:
			self.VoidTiles += 1

		if up:
			self.VoidTiles += 1
		
		if down:
			self.VoidTiles += 1

class FloodFill():
	def __init__(self, Width, Height):
		self.LastTileNumber = 0
		self.id = 0
		self.tile = [[None for i in xrange(Width)] for i in xrange(Height)]
 
	def AddTile(self, x, y, i, ParentID):
		for row in self.tile:
			for floodTile in row:
				if floodTile != None:
					if floodTile.x == x and floodTile.y == y:
						print "Tile Already Exists"
						return

		if i > self.LastTileNumber:
			self.LastTileNumber = i
		self.id += 1
		self.tile[x][y] = FloodTile(x, y, i, ParentID, self.id)
		
 
	def GetFloodAt(self, i):
		floodTiles = []
	   
		for row in self.tile:
			for floodTile in row:
				if floodTile != None:
					if floodTile.i == i:
						floodTiles.append(floodTile)
		return floodTiles
 
	def GetLastTileNumber(self):
		return self._LastTileNumber
 
class FloodTile():
	def __init__(self, X, Y, I, ParentID, ID):
		self.x = X
		self.y = Y
		self.i = I
		self.parentID = ParentID
		self.id = ID