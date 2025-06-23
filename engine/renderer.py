import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

import config
from . import camera, objects, cubemap

class CubeMapRenderer:
    def __init__(self):

        pygame.init()
        pygame.display.set_mode(
            (config.WINDOW_WIDTH, config.WINDOW_HEIGHT), 
            pygame.DOUBLEBUF | pygame.OPENGL
        )
        pygame.display.set_caption(config.WINDOW_CAPTION)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_CUBE_MAP)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glClearColor(*config.BACKGROUND_COLOR)


        self.camera = camera.Camera()
        objects.setup_lighting()
        self.cubemap_sets = config.CUBEMAP_SETS
        self.current_cubemap_index = 0
        
        
        self._load_current_skybox()

        self.clock = pygame.time.Clock()
        self.is_running = True

    def _load_current_skybox(self):
        folder = self.cubemap_sets[self.current_cubemap_index]
        print(f"Aktualny skybox: {folder}")
        self.cube_map_id = cubemap.create_cubemap_from_images(folder, config.CUBEMAP_FACES)

    def _switch_cubemap(self):

        if hasattr(self, 'cube_map_id') and self.cube_map_id:
            glDeleteTextures(1, [self.cube_map_id])

        self.current_cubemap_index = (self.current_cubemap_index + 1) % len(self.cubemap_sets)
        
        self._load_current_skybox()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    self._switch_cubemap()

        self.camera.handle_input(pygame.key.get_pressed(), pygame.mouse.get_pressed(), pygame.mouse.get_rel())
    
    def _render_frame(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

  
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(config.FOV, config.WINDOW_WIDTH / config.WINDOW_HEIGHT, config.NEAR_CLIP, config.FAR_CLIP)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.camera.apply_transform()

        objects.draw_skybox(self.cube_map_id, self.camera.position)
        objects.draw_reflective_cube(self.cube_map_id, self.camera.position)
        objects.draw_reflective_sphere(self.cube_map_id, self.camera.position)
        objects.draw_reflective_torus(self.cube_map_id, self.camera.position)
        
        
        pygame.display.flip()


    def run(self):
        while self.is_running:
            self._handle_events()
            self._render_frame()
            self.clock.tick(config.FPS_LIMIT)
        
        pygame.quit()