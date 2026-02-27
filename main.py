# Built-ins
import sys
import asyncio
 
# External
import pygame
from pygame.locals import *

# Internal
from scenes import *

class Game:
    def __init__(self, screen_size, fps):
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(screen_size, FULLSCREEN | SCALED)
        self.clock = pygame.time.Clock()
        self.fps = fps

        self.scene_manager = SceneManager()
        self.scene_manager.register_scene(TitleScreen(), "Title")
        self.scene_manager.set_scene("Title")

        pygame.display.set_caption("Winter Jam 2026")

    async def start(self):
        self.is_running = True

        while self.is_running:
            # Get delta time
            delta_time = self.clock.tick(self.fps) / 1000
            await asyncio.sleep(0)

            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    self.is_running = False

            self.scene_manager.handle_events(events)

            # Update frame
            self.scene_manager.update(delta_time)

            # Draw frame
            self.screen.fill((0, 0, 0))
            self.scene_manager.draw(self.screen)

            # Flip display
            pygame.display.flip()

        self.stop()

    def stop(self):
        pygame.quit()
        sys.exit()

# Entry point
if __name__ == "__main__":
    game = Game(
        screen_size=(640, 360),
        fps=0
    )

    asyncio.run(game.start())