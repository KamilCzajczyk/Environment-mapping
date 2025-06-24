import math
from OpenGL.GL import *
from . import utils

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 0.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

def draw_skybox(cube_map_id, camera_pos):
    glPushMatrix()
    glDisable(GL_CULL_FACE)
    glDepthMask(GL_FALSE)
    glDepthFunc(GL_LEQUAL)
    glDisable(GL_LIGHTING)
    
    glTranslatef(camera_pos[0], camera_pos[1], camera_pos[2])
    
    glEnable(GL_TEXTURE_CUBE_MAP)
    glBindTexture(GL_TEXTURE_CUBE_MAP, cube_map_id)
    
    s = 100.0
    v = [[-s,-s,s], [s,-s,s], [s,s,s], [-s,s,s], [-s,-s,-s], [s,-s,-s], [s,s,-s], [-s,s,-s]]
    t = [[-1,-1,1], [1,-1,1], [1,1,1], [-1,1,1], [-1,-1,-1], [1,-1,-1], [1,1,-1], [-1,1,-1]]
    
    glBegin(GL_QUADS)
    faces = [(0,1,2,3), (5,4,7,6), (3,2,6,7), (4,5,1,0), (1,5,6,2), (4,0,3,7)]
    for i, face in enumerate(faces):
        for j in face:
            glTexCoord3f(t[j][0], t[j][1], t[j][2])
            glVertex3f(v[j][0], v[j][1], v[j][2])
    glEnd()
    
    glEnable(GL_LIGHTING)
    glDepthFunc(GL_LESS)
    glDepthMask(GL_TRUE)
    glEnable(GL_CULL_FACE)
    
    glPopMatrix()
    
def draw_reflective_cube(cube_map_id, camera_pos):

    glPushMatrix()
    glEnable(GL_TEXTURE_CUBE_MAP)
    glBindTexture(GL_TEXTURE_CUBE_MAP, cube_map_id)

    size = 1.5
    vertices = [
        [[-size, -size, size], [size, -size, size], [size, size, size], [-size, size, size]], 
        [[size, -size, -size], [-size, -size, -size], [-size, size, -size], [size, size, -size]], 
        [[-size, size, size], [size, size, size], [size, size, -size], [-size, size, -size]], 
        [[-size, -size, -size], [size, -size, -size], [size, -size, size], [-size, -size, size]], 
        [[size, -size, size], [size, -size, -size], [size, size, -size], [size, size, size]], 
        [[-size, -size, -size], [-size, -size, size], [-size, size, size], [-size, size, -size]]  
    ]
    normals = [[0,0,1], [0,0,-1], [0,1,0], [0,-1,0], [1,0,0], [-1,0,0]]

    glBegin(GL_QUADS)
    for face_verts, normal in zip(vertices, normals):
        glNormal3fv(normal)
        for vertex in face_verts:
            view_vec = utils.normalize([camera_pos[i] - vertex[i] for i in range(3)])
            refl_vec = utils.reflect([-v for v in view_vec], normal)
            glTexCoord3fv(refl_vec)
            glVertex3fv(vertex)
    glEnd()

    glDisable(GL_TEXTURE_CUBE_MAP)
    glPopMatrix()

def draw_reflective_sphere(cube_map_id, camera_pos):

    glPushMatrix()
    glTranslatef(6, 0, 6)
    
    glEnable(GL_TEXTURE_CUBE_MAP)
    glBindTexture(GL_TEXTURE_CUBE_MAP, cube_map_id)

    radius, slices, stacks = 1.2, 32, 16
    for i in range(stacks):
        lat1 = math.pi * (-0.5 + float(i) / stacks)
        lat2 = math.pi * (-0.5 + float(i + 1) / stacks)
        glBegin(GL_QUAD_STRIP)
        for j in range(slices + 1):
            lng = 2 * math.pi * float(j) / slices
            
            for lat in [lat1, lat2]:
                x = radius * math.cos(lat) * math.cos(lng)
                y = radius * math.sin(lat)
                z = radius * math.cos(lat) * math.sin(lng)
                
                world_pos = [x + 3, y, z]
                normal = utils.normalize([x, y, z])
                view_vec = utils.normalize([camera_pos[k] - world_pos[k] for k in range(3)])
                refl_vec = utils.reflect([-v for v in view_vec], normal)
                
                glNormal3fv(normal)
                glTexCoord3fv(refl_vec)
                glVertex3f(x, y, z)
        glEnd()
    
    glDisable(GL_TEXTURE_CUBE_MAP)
    glPopMatrix()



def draw_reflective_torus(cube_map_id, camera_pos):

    glPushMatrix()
    torus_pos = [-6.0, 0.0, 6.0]
    glTranslatef(torus_pos[0], torus_pos[1], torus_pos[2])

    glEnable(GL_TEXTURE_CUBE_MAP)
    glBindTexture(GL_TEXTURE_CUBE_MAP, cube_map_id)

    major_radius = 1.0
    minor_radius = 0.4
    rings = 40  
    sides = 20 

    for i in range(rings):
        u1 = (i / rings) * 2 * math.pi
        u2 = ((i + 1) / rings) * 2 * math.pi
        glBegin(GL_QUAD_STRIP)
        for j in range(sides + 1):
            v = (j / sides) * 2 * math.pi


            x1 = (major_radius + minor_radius * math.cos(v)) * math.cos(u1)
            y1 = minor_radius * math.sin(v)
            z1 = (major_radius + minor_radius * math.cos(v)) * math.sin(u1)
            

            nx1 = math.cos(v) * math.cos(u1)
            ny1 = math.sin(v)
            nz1 = math.cos(v) * math.sin(u1)
            normal1 = utils.normalize([nx1, ny1, nz1])
            
            world_pos1 = [x1 + torus_pos[0], y1 + torus_pos[1], z1 + torus_pos[2]]
            view_vec1 = utils.normalize([camera_pos[k] - world_pos1[k] for k in range(3)])
            refl_vec1 = utils.reflect([-val for val in view_vec1], normal1)

            glNormal3fv(normal1)
            glTexCoord3fv(refl_vec1)
            glVertex3f(x1, y1, z1)


            x2 = (major_radius + minor_radius * math.cos(v)) * math.cos(u2)
            y2 = minor_radius * math.sin(v)
            z2 = (major_radius + minor_radius * math.cos(v)) * math.sin(u2)


            nx2 = math.cos(v) * math.cos(u2)
            ny2 = math.sin(v)
            nz2 = math.cos(v) * math.sin(u2)
            normal2 = utils.normalize([nx2, ny2, nz2])
            
            world_pos2 = [x2 + torus_pos[0], y2 + torus_pos[1], z2 + torus_pos[2]]
            view_vec2 = utils.normalize([camera_pos[k] - world_pos2[k] for k in range(3)])
            refl_vec2 = utils.reflect([-val for val in view_vec2], normal2)

            glNormal3fv(normal2)
            glTexCoord3fv(refl_vec2)
            glVertex3f(x2, y2, z2)
        glEnd()

    glDisable(GL_TEXTURE_CUBE_MAP)
    glPopMatrix()
