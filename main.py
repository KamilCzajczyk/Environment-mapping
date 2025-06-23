import pygame
from engine.renderer import CubeMapRenderer

def main():
    try:
        renderer = CubeMapRenderer()
        renderer.run()
    except Exception as e:
        print(f"Błąd {e}")
        pygame.quit()

if __name__ == "__main__":
    main()