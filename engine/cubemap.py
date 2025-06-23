import os
import numpy as np
from PIL import Image
from OpenGL.GL import *

def _create_fallback_face(face_target, filename):
    fallback_colors = {
        "px.jpg": (255, 100, 100), "nx.jpg": (100, 255, 100),
        "py.jpg": (100, 100, 255), "ny.jpg": (255, 255, 100),
        "pz.jpg": (255, 100, 255), "nz.jpg": (100, 255, 255)
    }
    color = fallback_colors.get(filename, (128, 128, 128))
    size = 256
    texture_data = np.full((size, size, 3), color, dtype=np.uint8)
    
    
    glTexImage2D(face_target, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)

def create_cubemap_from_images(folder, face_files):

    cube_map_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_CUBE_MAP, cube_map_id)
    
    face_targets = [
        GL_TEXTURE_CUBE_MAP_POSITIVE_X, GL_TEXTURE_CUBE_MAP_NEGATIVE_X,
        GL_TEXTURE_CUBE_MAP_POSITIVE_Y, GL_TEXTURE_CUBE_MAP_NEGATIVE_Y,
        GL_TEXTURE_CUBE_MAP_POSITIVE_Z, GL_TEXTURE_CUBE_MAP_NEGATIVE_Z
    ]
    
    for i, filename in enumerate(face_files):
        filepath = os.path.join(folder, filename)
        face_target = face_targets[i]
        try:
            if os.path.exists(filepath):
                image = Image.open(filepath).convert('RGB')
                img_data = np.array(image)
                glTexImage2D(face_target, 0, GL_RGB, image.width, image.height, 0, 
                             GL_RGB, GL_UNSIGNED_BYTE, img_data)
            else:
                _create_fallback_face(face_target, filename)
        except Exception as e:
            print(f"Błąd ładowania {filepath}: {e}.")
            _create_fallback_face(face_target, filename)

    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
    
    return cube_map_id