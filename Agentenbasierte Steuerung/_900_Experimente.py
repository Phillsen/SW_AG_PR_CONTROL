import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps, Pose
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes
import asyncio
import time
import math




def workloop(robot: cozmo.robot.Robot):

    MA1_fixed_object = robot.world.create_custom_fixed_object(Pose(0, 300, 0, angle_z=degrees(0)), 50, 100, 60, relative_to_robot=False)
    MA2_fixed_object = robot.world.create_custom_fixed_object(Pose(0, 700, 0, angle_z=degrees(0)), 50, 100, 60, relative_to_robot=False)
    MA3_fixed_object = robot.world.create_custom_fixed_object(Pose(400, 1000, 0, angle_z=degrees(90)), 50, 100, 60, relative_to_robot=False)
    MA4_fixed_object = robot.world.create_custom_fixed_object(Pose(800, 700, 0, angle_z=degrees(0)), 50, 100, 60, relative_to_robot=False)
    MA5_fixed_object = robot.world.create_custom_fixed_object(Pose(800, 300, 0, angle_z=degrees(0)), 50, 100, 60, relative_to_robot=False)

    MA1_Anfahrpunkt = cozmo.util.Pose(300, 300, 0, angle_z=degrees(180))
    MA2_Anfahrpunkt = cozmo.util.Pose(300, 700, 0, angle_z=degrees(180))
    MA3_Anfahrpunkt = cozmo.util.Pose(380, 700, 0, angle_z=degrees(90))
    MA4_Anfahrpunkt = cozmo.util.Pose(500, 700, 0, angle_z=degrees(0))
    MA5_Anfahrpunkt = cozmo.util.Pose(500, 300, 0, angle_z=degrees(0))
    X = cozmo.util.Pose(5, 5, 0, angle_z=degrees(0))
    Basis = cozmo.util.Pose(0, 0, 0, angle_z=degrees(0))



    Anfahrpunkte = []
    Anfahrpunkte.append(MA1_Anfahrpunkt)
    Anfahrpunkte.append(MA2_Anfahrpunkt)
    Anfahrpunkte.append(MA3_Anfahrpunkt)
    Anfahrpunkte.append(MA4_Anfahrpunkt)
    Anfahrpunkte.append(MA5_Anfahrpunkt)
    Anfahrpunkte.append(X)

     
    for n in Anfahrpunkte:
        robot.go_to_pose(n, relative_to_robot=False).wait_for_completed()


cozmo.run_program(workloop, use_3d_viewer = False)