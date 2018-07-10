import cozmo
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
import time
import asyncio



def Batterycheck(robot: cozmo.robot.Robot):

    cube = None
    lastcube = None
    
    print("")
    print("Akkustand Cozmo: " + str(round(robot.battery_voltage,2)) + "Volt")

    cube1 = robot.world.get_light_cube(LightCube1Id)
    cube2 = robot.world.get_light_cube(LightCube2Id)
    cube3 = robot.world.get_light_cube(LightCube3Id)
    cubes = [cube1, cube2, cube3]
    
    for c in cubes:
        while c.battery_str == "Unknown":
            time.sleep(1)
        print("Cube "+ str(c.cube_id) + " " +c.battery_str)
        if c.battery_str > str(60):
            c.set_lights(cozmo.lights.blue_light)
        elif c.battery_str > str(40):
            c.set_lights(cozmo.lights.green_light)
        else:
            c.set_lights(cozmo.lights.red_light)
    end = False
    while end == False:
        if input("Beenden mit x: ") == "x":
            end = True
          
cozmo.run_program(Batterycheck)