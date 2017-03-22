from robot import Robot
import time

## VARS ##



robot = Robot()




def GetTile(distance):
	tileSize = 30.0
	tile = 0
	while distance >= tileSize:
		tile += 1
		distance -= tileSize
		
	print "Tile: ", tile, " Distance: ", distance, " Remaining: ", divmod(distance, tileSize)
		
	return tile

GetTile(robot.GetFrontSonar())

robot.Exit()





