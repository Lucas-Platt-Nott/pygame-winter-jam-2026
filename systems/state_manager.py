class StateManager:
    def __init__(self, initial_state=""):
        self.state = initial_state

    def set_state(self, new_state):
        self.state = new_state

    def get_state(self):
        return self.state
