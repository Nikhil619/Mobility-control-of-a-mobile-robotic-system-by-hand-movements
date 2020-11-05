# -*- coding: utf-8 -*-
"""

@author: Nikhil
"""

"""
function inputs:

linear_velocity = desired linear velocity at that particular time step
angular_velocity = desired angular velocity at that particular time step
err_linear_integral = sum of linear velocity errors till that particular time step
err_angular_integral = sum of angular velocity errors till that particular time step

function outputs:

velocity_left_wheel = velocity of the left wheel
velocity_right_wheel = velocity of the right wheel
err_linear = linear velocity error
err_angular = angular velocity error

"""

def PI_CONTROLLER(linear_velocity, angular_velocity, err_linear_integral, err_angular_integral):
    err_linear_integral = 0
    err_angular_integral = 0

    k_p = 2
    k_i = 1

    linear_velocity_real = "/path to read the real linear velocity of the robot using wheel encoders"
    angular_velocity_real = "/path to read the real angular velocity of the robot using wheel encoders"    
    
    err_linear = linear_velocity - linear_velocity_real
    err_angular = angular_velocity - angular_velocity_real    
    
    linear_t = k_p*err_linear + k_i*err_linear_integral
    angular_t = k_p*err_angular + k_i*err_angular_integral

    linear_velocity_controlled = linear_velocity_real + linear_t
    angular_velocity_controlled = angular_velocity_real + angular_t

    V = linear_velocity_controlled
    A = angular_velocity_controlled

    length_of_robot = "input the length"
    breadth_of_robot = "input the breadth"

    velocity_left_wheel = (2*V - A*length_of_robot)/(2*breadth_of_robot)
    velocity_right_wheel = (2*V + A*length_of_robot)/(2*breadth_of_robot)    


    return velocity_left_wheel, velocity_right_wheel, err_linear, err_angular
    
"""
give the velocity_left_wheel and velocity_right_wheel to the left wheel and right wheel of the robot, respectively.
"""    
    

