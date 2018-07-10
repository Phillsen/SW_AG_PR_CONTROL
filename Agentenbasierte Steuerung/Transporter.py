import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps, Pose
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes
import asyncio


distance = 0 
turndegrees = 0
angledegrees = 0
speed = 100
x_coordinate = 0
y_coordinate = 0



def ObjektGesehen(evt, **kw):
    # This will be called whenever an EvtObjectAppeared is dispatched -
    # whenever an Object comes into view.
    if isinstance(evt.obj, CustomObject):
        print("Cozmo started seeing a %s" % str(evt.obj.object_type))

def got_to_coordinate(robot: cozmo.robot.Robot):
    global x_coordinate
    global y_coordinate
    global angledegrees
    robot.go_to_pose(Pose(x_coordinate, y_coordinate, 0, angle_z=degrees(angledegrees)), relative_to_robot=True).wait_for_completed()

def drive_straight(robot: cozmo.robot.Robot):
    global distance
    global speed
    robot.drive_straight(distance_mm(distance), speed_mmps(speed)).wait_for_completed()

def gehSuchen(robot: cozmo.robot.Robot):

    cube_obj = robot.world.define_custom_cube(CustomObjectTypes.CustomType00,CustomObjectMarkers.Diamonds2, 60, 50, 50, True)
    
    Maschine = None

    # in die Mitte fahren
    robot.drive_straight(distance_mm(distance), speed_mmps(speed)).wait_for_completed()

    #anfangen zu suchen
    look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    
    try:
        Maschine = robot.world.wait_for_observed_light_cube(timeout=30)
        Maschine = robot.world.wa
               

    except asyncio.TimeoutError:
        pass
        # zurücksetzen neu suchen

    finally:
        # whether we find it or not, we want to stop the behavior
        look_around.stop()



