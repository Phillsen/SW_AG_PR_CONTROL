import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps, Pose
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes
import asyncio
import time
import math


Transportliste = None
Feedback = None








def Transport(robot, Aufgabe):

    robot.set_head_angle(degrees(7)).wait_for_completed()
    cube = robot.world.wait_for_observed_light_cube(timeout=30)
    robot.pickup_object(cube, num_retries=3).wait_for_completed()
    robot.turn_in_place(degrees(180)).wait_for_completed()
    robot.drive_straight(distance_mm(100), speed_mmps(200)).wait_for_completed()
    robot.place_object_on_ground_here(cube, num_retries=2).wait_for_completed()
    robot.turn_in_place(degrees(180)).wait_for_completed()
    robot.drive_straight(distance_mm(100), speed_mmps(200)).wait_for_completed()
    robot.turn_in_place(degrees(180)).wait_for_completed()

    Feedback.put(" Cozmo hat Produkt {} nach {} gebracht".format(Aufgabe[0], Aufgabe[1]))

def standby(robot: cozmo.robot.Robot):

    global Transportliste
    global Feedback

    MA1_Schweissen = robot.world.define_custom_cube(CustomObjectTypes.CustomType00,CustomObjectMarkers.Circles2, 50, 50, 50, True)
    MA2_Montieren = robot.world.define_custom_cube(CustomObjectTypes.CustomType00,CustomObjectMarkers.Circles3, 50, 50, 50, True)
    MA3_Kalibrieren = robot.world.define_custom_cube(CustomObjectTypes.CustomType00,CustomObjectMarkers.Circles4, 50, 50, 50, True)
    MA4_Pruefen = robot.world.define_custom_cube(CustomObjectTypes.CustomType00,CustomObjectMarkers.Circles5, 50, 50, 50, True)
    MA5_Verpacken = robot.world.define_custom_cube(CustomObjectTypes.CustomType00,CustomObjectMarkers.Diamonds2, 50, 50, 50, True)
    
    
    while True:

        if Transportliste.empty() is False:
            Auftrag = Transportliste.get()
            
            print("cozmo transportiert Produkt {0} nach {1}".format(str(Auftrag[0]),str(Auftrag[1])))
            Transport(robot, Auftrag)
        else:
            time.sleep(0.5)

            #Test = Transportliste.get()
            #print(Test + "von Cozmo aus der Queue gezogen")
            #Aufgabe = Transportliste.get()
            #Transport(robot, Aufgabe)

       
    #zeroOffset = 80
    #inputOffset = 100
    
    

    ## wait until we see a custom object
    #while True:
    #    offset = zeroOffset + inputOffset
    #    my_object_instance = None

    #    while my_object_instance is None:
    #        evt = robot.wait_for(cozmo.objects.EvtObjectObserved, timeout=None)
    #        if isinstance(evt.obj, CustomObject):
    #            my_object_instance = evt.obj
    #            # find the vector from the object to the robot
    #            object_to_robot_vec = robot.pose.position - my_object_instance.pose.position
    #            # normalize the vector (so it's length 1.0)
    #            object_to_robot_vec_dist = math.sqrt((object_to_robot_vec.x * object_to_robot_vec.x) + (object_to_robot_vec.y * object_to_robot_vec.y) + (object_to_robot_vec.z * object_to_robot_vec.z))
    #            normalized_object_to_robot_vec = object_to_robot_vec * (1.0 / object_to_robot_vec_dist)
    #            # we can now add X times this vector to the objects position and it will push us X mm towards the robot
    #            # e.g. lets push it 50mm back (about 1 Cozmo length)
    #            offset_vec = (normalized_object_to_robot_vec * offset)
    #            target_pos = my_object_instance.pose.position + offset_vec 

    #            target_pose = my_object_instance.pose
    #            # change the position (set it to the new target_pos we calculated above)
    #            target_pose._position = target_pos
                    
    #    robot.go_to_pose(target_pose).wait_for_completed()
    #    time.sleep(0.5)


def runCozmo(TransList, Fdback):
    global Transportliste
    global Feedback
    Transportliste = TransList
    Feedback = Fdback

    cozmo.run_program(standby)