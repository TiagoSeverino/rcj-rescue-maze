from robot import Robot
import time


robot = Robot()

def GetTile(distance):
	tileSize = 30.0
	tile = 0

	print "Distance: ", distance

	while distance >= tileSize:
		tile += 1
		distance -= tileSize
		
	print "Tile: ", tile
		
	return (tile, distance)

def MoveTile(tileNumber):
	while True:
		(tile, distance) = GetTile(robot.GetFrontSonar())

		if tile > 0:
			if tile == tileNumber:
				if distance > 2.5 and distance < 5:
					robot.Break()
					break
				elif distance <= 3:
					robot.Backward()
				else:
					robot.Forward()
		else:
			robot.Backward()

	
robot.RotateRight()

robot.Exit()





