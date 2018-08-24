import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps, Pose
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes
import asyncio
import time
import math

Transportliste = None
Feedback = None




def getCube(robot,cube):

    robot.set_head_angle(degrees(7)).wait_for_completed()
    robot.pickup_object(cube, num_retries=3).wait_for_completed()
    print("cozmo hat Cube aufgeladen")

def Transport(robot, Auftrag, cube):

    MA1_Anfahrpunkt = cozmo.util.Pose(300, 300, 0, angle_z=degrees(180))
    MA2_Anfahrpunkt = cozmo.util.Pose(300, 700, 0, angle_z=degrees(180))
    MA3_Anfahrpunkt = cozmo.util.Pose(380, 700, 0, angle_z=degrees(90))
    MA4_Anfahrpunkt = cozmo.util.Pose(500, 700, 0, angle_z=degrees(0))
    MA5_Anfahrpunkt = cozmo.util.Pose(500, 300, 0, angle_z=degrees(0))
    LagerAnfahrpunkt = cozmo.util.Pose(500, 200, 0, angle_z=degrees(270))
            

    Anfahrpunkt = None
    Maschine = None
    Object = None
    print("Transportauftrag: " +str(Auftrag[2])+ "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    if Auftrag[2] == 1:
        #MA1_Schweissen = robot.world.define_custom_cube(CustomObjectTypes.CustomType00,CustomObjectMarkers.Circles2, 50, 50, 50, True)
        Object = robot.world.define_custom_cube(CustomObjectTypes.CustomType00,CustomObjectMarkers.Circles2, 50, 50, 50, True)
        Anfahrpunkt = MA1_Anfahrpunkt
        robot.go_to_pose(MA1_Anfahrpunkt).wait_for_completed()

    elif Auftrag[2] == 2:
        #MA2_Montieren = robot.world.define_custom_cube(CustomObjectTypes.CustomType01,CustomObjectMarkers.Circles3, 50, 50, 50, True)
        Object = robot.world.define_custom_cube(CustomObjectTypes.CustomType01,CustomObjectMarkers.Circles3, 50, 50, 50, True)
        Anfahrpunkt = MA2_Anfahrpunkt
        robot.go_to_pose(MA2_Anfahrpunkt).wait_for_completed()

    elif Auftrag[2] == 3:
        #MA3_Kalibrieren = robot.world.define_custom_cube(CustomObjectTypes.CustomType02,CustomObjectMarkers.Circles4, 50, 50, 50, True)
        Object = robot.world.define_custom_cube(CustomObjectTypes.CustomType02,CustomObjectMarkers.Circles4, 50, 50, 50, True)
        Anfahrpunkt = MA3_Anfahrpunkt
        robot.go_to_pose(MA3_Anfahrpunkt).wait_for_completed()

    elif Auftrag[2] == 4:
        #MA4_Pruefen = robot.world.define_custom_cube(CustomObjectTypes.CustomType03,CustomObjectMarkers.Circles5, 50, 50, 50, True)
        Object = robot.world.define_custom_cube(CustomObjectTypes.CustomType03,CustomObjectMarkers.Circles5, 50, 50, 50, True)
        Anfahrpunkt = MA4_Anfahrpunkt
        robot.go_to_pose(MA4_Anfahrpunkt).wait_for_completed()

    elif Auftrag[2] == 5:
        #MA5_Verpacken = robot.world.define_custom_cube(CustomObjectTypes.CustomType04,CustomObjectMarkers.Diamonds2, 50, 50, 50, True)
        Object = robot.world.define_custom_cube(CustomObjectTypes.CustomType04,CustomObjectMarkers.Diamonds2, 50, 50, 50, True)
        Anfahrpunkt = MA5_Anfahrpunkt
        robot.go_to_pose(MA5_Anfahrpunkt).wait_for_completed()
    elif Auftrag[2] == 6:
        #MA5_Verpacken = robot.world.define_custom_cube(CustomObjectTypes.CustomType04,CustomObjectMarkers.Diamonds2, 50, 50, 50, True)
        Object = robot.world.define_custom_cube(CustomObjectTypes.CustomType05,CustomObjectMarkers.Diamonds3, 50, 50, 50, True)
        Anfahrpunkt = LagerAnfahrpunkt
        robot.go_to_pose(MA5_Anfahrpunkt).wait_for_completed()
     
        
    offset = 180
    
    print("Cozmo staht am anfahrpunkt")

    my_object_instance = None

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

    robot.place_object_on_ground_here(cube, num_retries=1).wait_for_completed()
    cube.set_lights(cozmo.lights.off_light)
       
    
    Feedback.put(" Cozmo hat Produkt {} nach {} gebracht".format(Auftrag[0], Auftrag[1]))

def standby(robot: cozmo.robot.Robot):

    global Transportliste
    global Feedback

    #MA1_fixed_object = robot.world.create_custom_fixed_object(Pose(0, 300, 0, angle_z=degrees(0)), 50, 100, 60, relative_to_robot=False)
    #MA2_fixed_object = robot.world.create_custom_fixed_object(Pose(0, 700, 0, angle_z=degrees(0)), 50, 100, 60, relative_to_robot=False)
    #MA3_fixed_object = robot.world.create_custom_fixed_object(Pose(400, 1000, 0, angle_z=degrees(0)), 50, 100, 60, relative_to_robot=False)
    #MA4_fixed_object = robot.world.create_custom_fixed_object(Pose(800, 700, 0, angle_z=degrees(0)), 50, 100, 60, relative_to_robot=False)
    #MA5_fixed_object = robot.world.create_custom_fixed_object(Pose(800, 300, 0, angle_z=degrees(0)), 50, 100, 60, relative_to_robot=False)
                
    cube1 = robot.world.get_light_cube(LightCube1Id)  
    cube2 = robot.world.get_light_cube(LightCube2Id)  
    cube3 = robot.world.get_light_cube(LightCube3Id)
   
    while True:

        if Transportliste.empty() is False:
            robot.set_all_backpack_lights(cozmo.lights.green_light)
            Auftrag = Transportliste.get()
            
            print("cozmo transportiert Produkt {0} nach {1}".format(str(Auftrag[0]),str(Auftrag[1])))
            cube = None

            if Auftrag[0] == 1:
                cube = cube1
            elif Auftrag[0] == 2:
                cube = cube2
            elif Auftrag[0] == 3:
                cube = cube3


            cube.set_lights(cozmo.lights.blue_light)
            getCube(robot,cube)
            Transport(robot, Auftrag, cube) 
            robot.set_all_backpack_lights(cozmo.lights.red_light)
        else:            
            time.sleep(0.5)


def runCozmo(TransList, Fdback):
    global Transportliste
    global Feedback
    Transportliste = TransList
    Feedback = Fdback
    cozmo.run_program(standby, use_viewer=False ,use_3d_viewer=True)