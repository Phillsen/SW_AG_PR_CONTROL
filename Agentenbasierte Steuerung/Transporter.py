import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps, Pose
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes
import asyncio
import time

distance =100 
turndegrees = 0
angledegrees = 0
speed = 100
x_coordinate = 0
y_coordinate = 0

Suchobjekt = 1




def handle_object_appeared(evt, **kw):
    # This will be called whenever an EvtObjectAppeared is dispatched -
    # whenever an Object comes into view.
    if isinstance(evt.obj, CustomObject):
        print("Cozmo started seeing a %s" % str(evt.obj.object_type))

def handle_object_disappeared(evt, **kw):
    # This will be called whenever an EvtObjectDisappeared is dispatched -
    # whenever an Object goes out of view.
    if isinstance(evt.obj, CustomObject):
        print("Cozmo stopped seeing a %s" % str(evt.obj.object_type))

def go_to_coordinate(robot: cozmo.robot.Robot):
    global x_coordinate
    global y_coordinate
    global angledegrees
    robot.go_to_pose(Pose(x_coordinate, y_coordinate, 0, angle_z=degrees(angledegrees)), relative_to_robot=True).wait_for_completed()

def drive_straight(robot: cozmo.robot.Robot):
    global distance
    global speed
    robot.drive_straight(distance_mm(distance), speed_mmps(speed)).wait_for_completed()

def gehSuchen(robot: cozmo.robot.Robot):

    robot.add_event_handler(cozmo.objects.EvtObjectAppeared, handle_object_appeared)
    robot.add_event_handler(cozmo.objects.EvtObjectDisappeared, handle_object_disappeared)
    
    Maschine1 = robot.world.define_custom_cube(CustomObjectTypes.CustomType00,CustomObjectMarkers.Circles2, 50, 50, 50, True)
    Maschine2 = robot.world.define_custom_cube(CustomObjectTypes.CustomType01,CustomObjectMarkers.Circles3, 50, 50, 50, True)
    Maschine3 = robot.world.define_custom_cube(CustomObjectTypes.CustomType02,CustomObjectMarkers.Circles4, 50, 50, 50, True)
    Maschine4 = robot.world.define_custom_cube(CustomObjectTypes.CustomType03,CustomObjectMarkers.Circles5, 50, 50, 50, True)
    Maschine5 = robot.world.define_custom_cube(CustomObjectTypes.CustomType04,CustomObjectMarkers.Diamonds2, 50, 50, 50, True)

    robot.set_head_angle(degrees(8)).wait_for_completed()
    
    # dreh dich und such nach der maschine

    # positioniere dich zur maschine - 15cm Abstand

    # such den würfel

    # lade den Würfel auf

    # fahr zutrück zur Mitte

    # dreh und scanne nach der nächsten maschine

    # positioniere dich zur maschine

    # lad den würfel ab

    
    
    

    # in die Mitte fahren
    #robot.drive_straight(distance_mm(distance), speed_mmps(speed)).wait_for_completed()

    #anfangen zu suchen
    for n in range(0,24):
        robot.turn_in_place(degrees(30)).wait_for_completed()
      

cozmo.run_program(gehSuchen, use_3d_viewer=True, use_viewer=True )