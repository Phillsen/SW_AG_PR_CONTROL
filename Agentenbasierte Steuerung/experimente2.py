import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
import PhysicalTransporter



#def driveToLocation(robot= cozmo.robot.Robot):
#    robot.go_to_pose(Pose(X, Y, 0, angle_z=degrees(45)), relative_to_robot=True).wait_for_completed()

#def cozmo_dreh_rechts(robot: cozmo.robot.Robot):

#    robot.turn_in_place(degrees(180)).wait_for_completed()
    
#    robot.drive_straight(distance_mm(40), speed_mmps(150)).wait_for_completed()

#    look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
#    cube = None

#    try:
#        cube = robot.world.wait_for_observed_light_cube(timeout=30)
#        print("Found cube: %s" % cube)
#    except asyncio.TimeoutError:
#        print("Didn't find a cube")
#    finally:
#        # whether we find it or not, we want to stop the behavior
#        look_around.stop()

#    if cube:
#        # Drive to 70mm away from the cube (much closer and Cozmo
#        # will likely hit the cube) and then stop.
#        action = robot.go_to_object(cube, distance_mm(70.0))
#        action.wait_for_completed()
#        print("Completed action: result = %s" % action)
#        print("Done.")


#def cozmo_dreh_links(robot: cozmo.robot.Robot):

#    robot.turn_in_place(degrees(180)).wait_for_completed()
    
#    robot.drive_straight(distance_mm(40), speed_mmps(150)).wait_for_completed()

#    look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
#    cube = None

#    try:
#        cube = robot.world.wait_for_observed_light_cube(timeout=30)
#        print("Found cube: %s" % cube)
#    except asyncio.TimeoutError:
#        print("Didn't find a cube")
#    finally:
#        # whether we find it or not, we want to stop the behavior
#        look_around.stop()

#    if cube:
#        # Drive to 70mm away from the cube (much closer and Cozmo
#        # will likely hit the cube) and then stop.
#        action = robot.go_to_object(cube, distance_mm(70.0))
#        action.wait_for_completed()
#        print("Completed action: result = %s" % action)
#        print("Done.")


#def Funktionsmanager(Funktion,Parameter1=0,Parameter2=0,Parameter3=0):
#    if Funktion =="DriveToLocation":
#        robot.go_to_pose(Pose(X, Y, 0, angle_z=degrees(45)), relative_to_robot=True).wait_for_completed()




while True:


    Befehl = input("L für links R für Rechts:")

    Befehl.upper()
    
    if Befehl == "L":
        cozmo.run_program(PhysicalTransporter.turn)
    if Befehl == "R":
        cozmo.run_program(PhysicalTransporter.driveToLocation)




