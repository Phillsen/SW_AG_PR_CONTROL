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
x_coordinate = 100
y_coordinate = 50

Maschine1visible = False
Maschine2visible = False
Maschine3visible = False
Maschine4visible = False
Maschine5visible = False

Zielmaschine = 1
ZielMaschineVisible = False
ZielmaschVar = None



def configMaschVar(M1,M2,M3,M4,M5, Target = Zielmaschine):
    global ZielmaschVar
    if Target == 1:
        ZielmaschVar = M1
        
    elif Target == 2:
        ZielmaschVar = M2
        
    elif Target == 3:
        ZielmaschVar = M3
        
    elif Target == 4:
        ZielmaschVar = M4
        
    elif Target == 5:
        ZielmaschVar = M5
        



def ZielMaschineSichtbar(Target=Zielmaschine):
    global ZielMaschineVisible
    if Target == 1:
        ZielMaschineVisible = Maschine1visible
        print("Zielmaschinevisible = " + str(Maschine1visible))
    elif Target == 2:
        ZielMaschineVisible = Maschine2visible
        print("Zielmaschinevisible = " + str(Maschine2visible))
    elif Target == 3:
        ZielMaschineVisible = Maschine3visible
        print("Zielmaschinevisible = " + str(Maschine3visible))
    elif Target == 4:
        ZielMaschineVisible = Maschine4visible
        print("Zielmaschinevisible = " + str(Maschine4visible))
    elif Target == 5:
        ZielMaschineVisible = Maschine5visible
        print("Zielmaschinevisible = " + str(Maschine5visible))
    


def MachineVisible(machine):
    global Maschine1visible
    global Maschine2visible
    global Maschine3visible
    global Maschine4visible
    global Maschine5visible

    print("Cozmo started seeing a %s" % str(machine.object_type))
    if machine.object_type == CustomObjectTypes.CustomType00:
        Maschine1visible = True
    if machine.object_type == CustomObjectTypes.CustomType01:
        Maschine2visible = True
    if machine.object_type == CustomObjectTypes.CustomType02:
        Maschine3visible = True
    if machine.object_type == CustomObjectTypes.CustomType03:
        Maschine4visible = True
    if machine.object_type == CustomObjectTypes.CustomType04:
        Maschine5visible = True
    ZielMaschineSichtbar()

    

        
def MachineInvisible(machine):
    global Maschine1visible
    global Maschine2visible
    global Maschine3visible
    global Maschine4visible
    global Maschine5visible

    print("Cozmo stopped seeing a %s" % str(machine.object_type))
    if machine.object_type == CustomObjectTypes.CustomType00:
        Maschine1visible = False
    if machine.object_type == CustomObjectTypes.CustomType01:
        Maschine2visible = False
    if machine.object_type == CustomObjectTypes.CustomType02:
        Maschine3visible = False
    if machine.object_type == CustomObjectTypes.CustomType03:
        Maschine4visible = False
    if machine.object_type == CustomObjectTypes.CustomType04:
        Maschine5visible = False
    ZielMaschineSichtbar()



   

def handle_object_appeared(evt, **kw):
    # This will be called whenever an EvtObjectAppeared is dispatched -
    # whenever an Object comes into view.
    if isinstance(evt.obj, CustomObject):
        MachineVisible(evt.obj)

def handle_object_disappeared(evt, **kw):
    # This will be called whenever an EvtObjectDisappeared is dispatched -
    # whenever an Object goes out of view.
    if isinstance(evt.obj, CustomObject):
        MachineInvisible(evt.obj)

def go_to_coordinate(robot):
    global x_coordinate
    global y_coordinate
    global angledegrees
    robot.go_to_pose(Pose(x_coordinate, y_coordinate, 0, angle_z=degrees(angledegrees)), relative_to_robot=True).wait_for_completed()

def drive_straight(robot):
    global distance
    global speed
    robot.drive_straight(distance_mm(distance), speed_mmps(speed)).wait_for_completed()


def lookForMachine(robot):
    global ZielMaschineVisible
    while ZielMaschineVisible == False:
        robot.turn_in_place(degrees(10)).wait_for_completed()
       
    

        

    

def workloop(robot: cozmo.robot.Robot):
    global ZielmaschVar
    robot.add_event_handler(cozmo.objects.EvtObjectAppeared, handle_object_appeared)
    robot.add_event_handler(cozmo.objects.EvtObjectDisappeared, handle_object_disappeared)
    
    Maschine1 = robot.world.define_custom_cube(CustomObjectTypes.CustomType00,CustomObjectMarkers.Circles2, 50, 50, 50, True)
    Maschine2 = robot.world.define_custom_cube(CustomObjectTypes.CustomType01,CustomObjectMarkers.Circles3, 50, 50, 50, True)
    Maschine3 = robot.world.define_custom_cube(CustomObjectTypes.CustomType02,CustomObjectMarkers.Circles4, 50, 50, 50, True)
    Maschine4 = robot.world.define_custom_cube(CustomObjectTypes.CustomType03,CustomObjectMarkers.Circles5, 50, 50, 50, True)
    Maschine5 = robot.world.define_custom_cube(CustomObjectTypes.CustomType04,CustomObjectMarkers.Diamonds2, 50, 50, 50, True)

    Maschine1.objectID = 99
    Maschine2.objectID = 98
    Maschine3.objectID = 97
    Maschine4.objectID = 96
    Maschine5.objectID = 95



    robot.set_head_angle(degrees(8)).wait_for_completed()
    
    
    # dreh dich und such nach der maschine
    lookForMachine(robot)

    # positioniere dich zur maschine - 15cm Abstand
    configMaschVar(Maschine1,Maschine2,Maschine3,Maschine4,Maschine5)

    
    action = robot.go_to_object(99, distance_mm(70.0))

    action.wait_for_completed()
    # such den würfel

    # lade den Würfel auf

    # fahr zutrück zur Mitte

    # dreh und scanne nach der nächsten maschine

    # positioniere dich zur maschine

    # lad den würfel ab

    while True:
        time.sleep(0.5)
    
    

    # in die Mitte fahren
    #robot.drive_straight(distance_mm(distance), speed_mmps(speed)).wait_for_completed()

    #anfangen zu suchen
    #for n in range(0,24):
    #    robot.turn_in_place(degrees(30)).wait_for_completed()
      
cozmo.robot.Robot.drive_off_charger_on_connect = False 
cozmo.run_program(workloop)