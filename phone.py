import pybullet as p
import time
import tkinter as tk
import math

class Phone:
    # Initialize the object
    def __init__(self, mass, width, depth, height, drop_height, orientation):
        self.mass = mass / 1000  # Convert grams to kilograms
        self.width = width
        self.depth = depth
        self.height = height
        self.drop_height = drop_height
        self.orientation = orientation
        self.phone_id = None
        self.phone_body_id = None

    # Create the phone in the PyBullet simulation
    def create_phone(self):
        
        phone_shape_id = p.createCollisionShape(p.GEOM_BOX, halfExtents=[self.width, self.depth, self.height])
        phone_visual_id = p.createVisualShape(p.GEOM_BOX, halfExtents=[self.width, self.depth, self.height], rgbaColor=[0, 0, 0, 1])
        self.phone_body_id = p.createMultiBody(self.mass, phone_shape_id, phone_visual_id)
        orientation_quaternion = p.getQuaternionFromEuler(self.orientation)
        p.resetBasePositionAndOrientation(self.phone_body_id, [0, 0, self.drop_height], orientation_quaternion)

    # Get the magnitude of the phone's velocity
    def get_velocity_magnitude(self):
        
        phone_velocity, _ = p.getBaseVelocity(self.phone_body_id)
        return math.sqrt(phone_velocity[0] ** 2 + phone_velocity[1] ** 2 + phone_velocity[2] ** 2)
    
    # Check if the phone has come to rest
    def is_resting(self, rest_threshold=0.001):
        
        phone_velocity_magnitude = self.get_velocity_magnitude()
        _, phone_angular_velocity = p.getBaseVelocity(self.phone_body_id)
        return phone_velocity_magnitude < rest_threshold and all(v < 0.01 for v in phone_angular_velocity)