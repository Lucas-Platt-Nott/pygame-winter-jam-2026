# Built-In
import asyncio
import sys

# External
import pygame
from pygame.locals import *

# Internal
from core import SceneManager

# Application Class
class Application:
    def __init__(self, screen_size: tuple[int, int], flags: int = 0, fps: int = 0):
        self.screen_size = screen_size
        self.flags = flags
        self.screen = pygame.display.set_mode(screen_size, FULLSCREEN | SCALED | flags)
        self.clock = pygame.Clock()
        self.fps = fps

        self.is_running = False
        self.is_maximised = True
        self.scene_manager = SceneManager()

    def add_scene(self, scene_type: type, scene_key: str) -> None:
        scene = scene_type(self.scene_manager)
        self.scene_manager.register_scene(scene, scene_key)

    def set_scene(self, scene_key: str) -> None:
        self.scene_manager.set_scene(scene_key)

    async def start(self) -> None:
        # Start the Game
        self.is_running = True

        # Main-Loop
        while self.is_running:
            # Get delta_time
            delta_time = self.clock.tick(self.fps) / 1000
            await asyncio.sleep(0)

            # Produce frame
            self.handle_events()
            self.update(delta_time)
            self.draw()
    
    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                # Close Game
                self.is_running = False

            else:
                if event.type == KEYDOWN and event.key == K_F11:
                    if self.is_maximised:
                        self.screen = pygame.display.set_mode(
                            self.screen_size,
                            self.flags
                        )
                        
                    else:
                        self.screen = pygame.display.set_mode(
                            self.screen_size,
                            self.flags | FULLSCREEN | SCALED
                        )

                    self.is_maximised = not self.is_maximised
                
                self.scene_manager.handle_event(event)

    def update(self, delta_time: float) -> None:
        pygame.display.set_caption(f"{self.clock.get_fps()}")
        self.scene_manager.update(delta_time)

    def draw(self) -> None:
        self.screen.fill((100, 100, 100))
        self.scene_manager.draw(self.screen)

        pygame.display.flip()

    def stop(self) -> None:
        sys.exit(0)
        pygame.quit()