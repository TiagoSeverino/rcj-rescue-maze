from robot import Robot
import time

robot = Robot()

while True:
        (leftCM, frontCM, rightCM) = robot.GetSonar()
        (tile, exactPosition) = robot.GetTile(frontCM)

        print frontCM, " ", tile, " ", exactPosition

        if tile>1:
            robot.Forward()
        else:
            if exactPosition:
                robot.Break()
                break
            else:
                robot.Backward()

robot.Break()
robot.Exit()
