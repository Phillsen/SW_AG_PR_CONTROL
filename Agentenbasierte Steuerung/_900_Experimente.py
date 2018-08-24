import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps, Pose
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes
import asyncio
import time
import math


def getCube(robot,cube):

    robot.set_head_angle(degrees(7)).wait_for_completed()
    robot.pickup_object(cube, num_retries=3).wait_for_completed()
    print("cozmo hat Cube aufgeladen")

def Transport(robot,cube):

    MA1_Schweissen = robot.world.define_custom_cube(CustomObjectTypes.CustomType00,CustomObjectMarkers.Circles2, 50, 50, 50, True)
    MA1_Anfahrpunkt = cozmo.util.Pose(300, 300, 0, angle_z=degrees(180))
    print("Stage 2")

    offset = 180
    robot.go_to_pose(MA1_Anfahrpunkt).wait_for_completed()

    my_object_instance = None
    print("Stage 3")
    while my_object_instance is None:
        print("Suche nach Objekt")
        evt = robot.wait_for(cozmo.objects.EvtObjectObserved, timeout=None)
        if isinstance(evt.obj, CustomObject):
            my_object_instance = evt.obj

            # find the vector from the object to the robot
            object_to_robot_vec = robot.pose.position - my_object_instance.pose.position

            # normalize the vector (so it's length 1.0)
            object_to_robot_vec_dist = math.sqrt((object_to_robot_vec.x * object_to_robot_vec.x) + (object_to_robot_vec.y * object_to_robot_vec.y) + (object_to_robot_vec.z * object_to_robot_vec.z))
            normalized_object_to_robot_vec = object_to_robot_vec * (1.0 / object_to_robot_vec_dist)
            # we can now add X times this vector to the objects position and it will push us X mm towards the robot
            # e.g. lets push it 50mm back (about 1 Cozmo length)
            offset_vec = (normalized_object_to_robot_vec * offset)
            target_pos = my_object_instance.pose.position + offset_vec 

            target_pose = my_object_instance.pose
            # change the position (set it to the new target_pos we calculated above)
            target_pose._position = target_pos
                    
    robot.go_to_pose(target_pose).wait_for_completed()
    robot.place_object_on_ground_here(cube1, num_retries=1).wait_for_completed()


def workloop(robot: cozmo.robot.Robot):

    
    cube = robot.world.get_light_cube(LightCube1Id)

    getCube(robot, cube)

    Transport(robot,cube)
    
    
    


cozmo.run_program(workloop, use_3d_viewer = False)