# External
import pygame

# State Class
class State:
    def handle_event(self, event: list[pygame.Event]) -> None:
        pass
    
    def update(self, delta_time: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        pass

# State Manager Class
class StateManager:
    def __init__(self):
        self.states: dict[str, State] = {}
        self.state: str = ""

    def add_state(self, new_state: State, state_key: str) -> None:
        self.states[state_key] = new_state

    def handle_event(self, event: list[pygame.Event]) -> None:
        self.states[self.state].handle_event(event)

    def update(self, delta_time: float) -> None:
        self.states[self.state].update(delta_time)

    def draw(self, surface: pygame.Surface) -> None:
        self.states[self.state].draw(surface)