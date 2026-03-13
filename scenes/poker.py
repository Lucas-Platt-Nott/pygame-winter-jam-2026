# External
import pygame
from pygame.locals import *

# Internal
from assets import Images, Sounds
from core import SceneManager, Scene
from config import *
from systems import PokerSystem, PokerRenderer, PokerPlayer, Player, PhaseState

# Poker Class
class Poker(Scene):
    def __init__(self, scene_manager: SceneManager, player: Player) -> None:
        self.scene_manager = scene_manager
        self.player = player

        self.loading = False
        self.system = PokerSystem(self.player, PokerPlayer())
        self.preamble = Images.get_image("intro_text")
        self.renderer = PokerRenderer()

    def start(self) -> None:
        self.loading = True
        self.player.reset()
        self.system = PokerSystem(self.player, PokerPlayer())

        Sounds.get_sound("background_music").play(-1, -1, 5000)
        self.renderer.update_balance_text(self.system)

    def handle_event(self, event: pygame.Event) -> None:
        if self.loading:
            if event.type == KEYDOWN and event.dict["key"] == K_RETURN:
                self.loading = False

            return

        self.system.handle_event(event)

    def update(self, delta_time: float) -> None:
        if self.loading:
            return
        
        if self.system.state["phase"] == PhaseState.BET:
            self.renderer.update_balance_text(self.system)

        self.system.update(delta_time)
        self.renderer.update(delta_time, self.system)

    def draw(self, surface: pygame.Surface) -> None:
        if self.loading:
            surface.blit(self.preamble, (0, 0))
            return

        self.renderer.draw(surface, self.system)