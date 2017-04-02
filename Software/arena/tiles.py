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