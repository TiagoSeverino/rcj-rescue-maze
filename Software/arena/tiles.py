class TILE():
	def __init__(self):
		self.tileType = TileType.Void
		self.rightWall = Wall.Unknown
		self.bottomWall = Wall.Unknown

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
		if self.tile[x][y] is None:
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