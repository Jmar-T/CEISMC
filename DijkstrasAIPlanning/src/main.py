# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       jmar                                                         #
# 	Created:      4/8/2026, 12:27:55 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

brain.screen.print("Hello V5")

# Brain should be defined by default
brain=Brain()

# Robot configuration code
left_drive_smart = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_drive_smart = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
drivetrain_inertial = Inertial(Ports.PORT19)
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, drivetrain_inertial, 319.19, 320, 40, MM, 1)
# AI Vision Color Descriptions
# AI Vision Code Descriptions
ai_vision_15 = AiVision(Ports.PORT15, AiVision.ALL_TAGS)
ClawMotor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
ArmMotor = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
controller_1 = Controller(PRIMARY)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()

vexcode_initial_drivetrain_calibration_completed = False
def calibrate_drivetrain():
    # Calibrate the Drivetrain Inertial
    global vexcode_initial_drivetrain_calibration_completed
    sleep(200, MSEC)
    brain.screen.print("Calibrating")
    brain.screen.next_row()
    brain.screen.print("Inertial")
    drivetrain_inertial.calibrate()
    while drivetrain_inertial.is_calibrating():
        sleep(25, MSEC)
    vexcode_initial_drivetrain_calibration_completed = True
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)


# Calibrate the Drivetrain
calibrate_drivetrain()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")



# define variables used for controlling motors based on controller inputs
controller_1_left_shoulder_control_motors_stopped = True
controller_1_right_shoulder_control_motors_stopped = True
drivetrain_l_needs_to_be_stopped_controller_1 = False
drivetrain_r_needs_to_be_stopped_controller_1 = False

# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
    global drivetrain_l_needs_to_be_stopped_controller_1, drivetrain_r_needs_to_be_stopped_controller_1, controller_1_left_shoulder_control_motors_stopped, controller_1_right_shoulder_control_motors_stopped, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            # stop the motors if the brain is calibrating
            if drivetrain_inertial.is_calibrating():
                left_drive_smart.stop()
                right_drive_smart.stop()
                while drivetrain_inertial.is_calibrating():
                    sleep(25, MSEC)
            
            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axis3 + axis1
            # right = axis3 - axis1
            drivetrain_left_side_speed = controller_1.axis3.position() + controller_1.axis1.position()
            drivetrain_right_side_speed = controller_1.axis3.position() - controller_1.axis1.position()
            
            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
                # check if the left motor has already been stopped
                if drivetrain_l_needs_to_be_stopped_controller_1:
                    # stop the left drive motor
                    left_drive_smart.stop()
                    # tell the code that the left motor has been stopped
                    drivetrain_l_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the left motor next
                # time the input is in the deadband range
                drivetrain_l_needs_to_be_stopped_controller_1 = True
            # check if the value is inside of the deadband range
            if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
                # check if the right motor has already been stopped
                if drivetrain_r_needs_to_be_stopped_controller_1:
                    # stop the right drive motor
                    right_drive_smart.stop()
                    # tell the code that the right motor has been stopped
                    drivetrain_r_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the right motor next
                # time the input is in the deadband range
                drivetrain_r_needs_to_be_stopped_controller_1 = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_l_needs_to_be_stopped_controller_1:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller_1:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
            # check the buttonL1/buttonL2 status
            # to control ArmMotor
            if controller_1.buttonL1.pressing():
                ArmMotor.spin(FORWARD)
                controller_1_left_shoulder_control_motors_stopped = False
            elif controller_1.buttonL2.pressing():
                ArmMotor.spin(REVERSE)
                controller_1_left_shoulder_control_motors_stopped = False
            elif not controller_1_left_shoulder_control_motors_stopped:
                ArmMotor.stop()
                # set the toggle so that we don't constantly tell the motor to stop when
                # the buttons are released
                controller_1_left_shoulder_control_motors_stopped = True
            # check the buttonR1/buttonR2 status
            # to control ClawMotor
            if controller_1.buttonR1.pressing():
                ClawMotor.spin(FORWARD)
                controller_1_right_shoulder_control_motors_stopped = False
            elif controller_1.buttonR2.pressing():
                ClawMotor.spin(REVERSE)
                controller_1_right_shoulder_control_motors_stopped = False
            elif not controller_1_right_shoulder_control_motors_stopped:
                ClawMotor.stop()
                # set the toggle so that we don't constantly tell the motor to stop when
                # the buttons are released
                controller_1_right_shoulder_control_motors_stopped = True
        # wait before repeating the process
        wait(20, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)

#endregion VEXcode Generated Robot Configuration

###___Global Variables___###
ai_objects = None
my_map = None
start = 0
end = 8
distances = None
paths = None
FINAL_MOVE_DATA = {
    (0, 1): (7, 0),
    (1, 2): (3, 90),
    (1, 3): (8, 270),
    (3, 4): (7, 180),
    (3, 5): (2, 270),
    (5, 6): (5, 0),
    (6, 7): (3, 270),
    (6, 8): (6, 0), 
    (8, 9): (9, 90),
    (9, 10): (3, 0),
    (9, 11): (4, 90),
    (11, 1): (11, 180)
}
###___Global Variables___###



#___OnPressedFuncitons__#
def run_on_A_pressed():
    ("Button A Pressed, taking picture of April Tag")
    global ai_objects
    global my_map
    ai_objects = ai_vision_15.take_snapshot(AiVision.ALL_TAGS)
    if not ai_objects[0].exists:
        print("Tag Not Found -> No Data")
        my_map = None
    elif ai_objects[0].id == 1:
        print("Found Tag Setting Map Data")
         
        my_map = [[(1, 7)], [(0, 7), (2, 3), (3, 8), (11, 11)],
                  [(1, 3)], [(1, 8), (4, 7), (5, 2)], [(3, 7)],
                  [(3, 2), (6, 5)], [(5, 5), (7, 3), (8, 6)], 
                  [(6, 3)], [(6, 6), (9, 9)], [(8, 9), (10, 3), (11, 4)],
                  [(9, 3)], [(9, 4), (1, 11)]]
def dijkstra(graph, start_node):
    """
    Compute Dijkstra's algorithm
    Finds the quickest way to get from a starting 
    node to every other location.
    
    :param graph: A list where each index is a 'current_node" and contains its nieghboring connections.
    :param start_node: The 'current_node' we are starting our journey from.
    :return: A list of shortest distances and the actual paths to take.
    """


    #1 Setup:
    #Assume every current_node has a "infinite" distance between them, until we find a path.
    total_distances = [float("inf")] * len(graph)
    total_distances[start_node] = 0
    
    visited_nodes = set()
    travel_paths = [[] for _ in range(len(graph))]

    #2 The Priority Queue (The 'To-Vsit' List)
    # We store tuples of (current_total_distance, current_node, previous_node)
    # The heapq keeps the smallest distance at the very top.
    unvisited_queue = [(0, start_node, None)]
    def push(x):
        unvisited_queue.append(x)
        unvisited_queue.sort()

    def pop():
        return unvisited_queue.pop(0)
    
    while unvisited_queue:
        #Pick the node with the shortest distanced discovered so far
        current_distance, current_node, parent_node = pop()
        
        #if we've already visited this node, then we have
        #already found a shorter path to it, so we skip it.
        if current_node in visited_nodes:
            continue

        #Mark this node as 'visited' and update the distance
        visited_nodes.add(current_node)
        total_distances[current_node] = current_distance
        #Build the path list (e.g., [0, 2, 3] meants start at 0, go to 2, then to 3)
        if parent_node is None:
            travel_paths[current_node] = [start_node]
        else:
            travel_paths[current_node] = travel_paths[parent_node] + [current_node]

        #3 Check Neighbors:
        # Look at all nodes connected to the current one
        for neighbor, weight in graph[current_node]:
            if neighbor not in visited_nodes:
                #Calculate: "Distance to current_node" + "Distance to neighbor"
                new_distance = current_distance + weight 
                push((new_distance, neighbor, current_node))
        
    return total_distances, travel_paths
def run_on_B_pressed():
    global my_map
    global start
    global distances
    global paths
    
    if my_map == None:
        print("Can't run on an empty map")
        return
    distances,paths = dijkstra(my_map,start)
    #print("just finished dijkstras")
    
    #print("--- Trip Results starting from Node {} ---", start)
    for node_id in range(len(distances)):
        # Convert numbers to strings so we can join them with arrows
        path_as_strings = [str(n) for n in paths[node_id]]
        path_format = " -> ".join(path_as_strings)
        #print("To Node %s: Route: [%s] | Total Cost: %s" % (node_id, path_format, distances[node_id]))
def run_on_Y_pressed():
    #move robot
    global distances, paths, FINAL_MOVE_DATA, end
    
    drivetrain.set_heading(0, DEGREES)
    if paths != None:
        path =paths[end]
    
    for i in range(len(path)-1):
        curr = path[i]
        nextl = path[i+1]
        move_distance, move_direction = (FINAL_MOVE_DATA[(curr, nextl)])
        
        drivetrain.turn_to_heading(move_direction)
        drivetrain.drive_for(FORWARD, move_distance* 8, INCHES,wait=True)
    

    

def when_started1():
    #___Global Variables___
    global myVariable
    pass
controller_1.buttonA.pressed(run_on_A_pressed)
controller_1.buttonB.pressed(run_on_B_pressed)
controller_1.buttonY.pressed(run_on_Y_pressed)

when_started1()
