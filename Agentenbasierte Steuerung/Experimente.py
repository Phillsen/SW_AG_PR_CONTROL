import cozmo
from cozmo.util import distance_mm, speed_mmps
import threading
import time


class CozmoBot(threading.Thread):
    def __init__(self, robot):
        threading.Thread.__init__(self)
        print("Eins")
        self.my_robot = robot
        print("Zwei")
        self.distance = 100
        print("Drei")
        self.start()

    def goforward(self):
        self.my_robot.drive_straight(distance_mm(self.distance), speed_mmps(50)).wait_for_completed()
        self.distance = 0
    
    def run(self):
        while True:
            if self.distance != 0:
                self.goforward()
                time.sleep(1)
            time.sleep(1)
            print("beep")

            

#def cozmo_program(robot: cozmo.robot.Robot):
#    my_bot = CozmoBot(robot)
#    my_bot.run()
          
C = CozmoBot(cozmo.robot.Robot)
