import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
import time


def Batterycheck(robot: cozmo.robot.Robot):
    robot.set_head_angle(degrees(7)).wait_for_completed()
    print("Battery Cozmo: " + str(round(robot.battery_voltage,2)) + "Volt")

    cube1 = robot.world.get_light_cube(LightCube1Id)
    cube2 = robot.world.get_light_cube(LightCube2Id)
    cube3 = robot.world.get_light_cube(LightCube3Id)
    cubes = [cube1, cube2, cube3]
    
    for c in cubes:
        while c.battery_str == "Unknown":
            time.sleep(0.5)
        print("Cube "+ str(c.cube_id) + " " +c.battery_str)
        
        if c.battery_str > str(60):
            c.set_lights(cozmo.lights.blue_light)
        elif c.battery_str > str(40):
            c.set_lights(cozmo.lights.green_light)
        else:
            c.set_lights(cozmo.lights.red_light)

    while True:
       time.sleep(1)
    quit()

cozmo.robot.Robot.drive_off_charger_on_connect = False       
cozmo.run_program(Batterycheck)