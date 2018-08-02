import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps, Pose
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes
import asyncio
import time



def workloop(robot: cozmo.robot.Robot):
    robot.set_head_angle(degrees(7)).wait_for_completed()
    MyObjectArchetype = robot.world.define_custom_cube(CustomObjectTypes.CustomType00,CustomObjectMarkers.Circles2, 50, 50, 50, True)
    my_object_instance = None
    newpose=  cozmo.util.Pose(120, 0,0,0,0,0,0)
    newpose2 = cozmo.util.Pose(0, 0,0,0,0,0,0)
    # wait until we see a custom object
    while my_object_instance is None:
        evt = robot.wait_for(cozmo.objects.EvtObjectObserved, timeout=None)
        if isinstance(evt.obj, CustomObject):
            my_object_instance = evt.obj
            
            newpose2 = my_object_instance.pose - newpose
            
    robot.go_to_pose(newpose2).wait_for_completed()



cozmo.run_program(workloop)