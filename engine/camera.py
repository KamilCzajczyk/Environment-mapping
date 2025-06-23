import math
import pygame
from OpenGL.GL import *

import config

class Camera:
    def __init__(self, position=[0.0, 0.0, 8.0]):
        self.position = list(position)
        self.rotation_x = 0  
        self.rotation_y = 0  
    
    def apply_transform(self):
       
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)
        glTranslatef(-self.position[0], -self.position[1], -self.position[2])

    def handle_input(self, keys, mouse_buttons, mouse_rel):
        if mouse_buttons[0]:
            self.rotation_y += mouse_rel[0] * config.MOUSE_SENSITIVITY
            self.rotation_x += mouse_rel[1] * config.MOUSE_SENSITIVITY
            self.rotation_x = max(-config.CAMERA_PITCH_LIMIT, min(config.CAMERA_PITCH_LIMIT, self.rotation_x))


        yaw_rad = math.radians(self.rotation_y)
        pitch_rad = math.radians(self.rotation_x)

        forward_x = math.sin(yaw_rad) * math.cos(pitch_rad)
        forward_y = -math.sin(pitch_rad)
        forward_z = -math.cos(yaw_rad) * math.cos(pitch_rad)

        right_x = math.cos(yaw_rad)
        right_z = math.sin(yaw_rad)
        
        speed = config.CAMERA_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.position[0] += forward_x * speed
            self.position[1] += forward_y * speed
            self.position[2] += forward_z * speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.position[0] -= forward_x * speed
            self.position[1] -= forward_y * speed
            self.position[2] -= forward_z * speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.position[0] -= right_x * speed
            self.position[2] -= right_z * speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.position[0] += right_x * speed
            self.position[2] += right_z * speed
        if keys[pygame.K_SPACE]:
            self.position[1] += speed
        if keys[pygame.K_LSHIFT] or keys[pygame.K_c]:
            self.position[1] -= speed