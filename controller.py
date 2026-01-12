from view_terminal import TerminalView   #nom a changer 
from view_pygame import PygameView

class GameController:
    def __init__(self, game_state):
        self.gs = game_state
        self.mode = "TERMINAL"

    def run(self):
        while True:
            if self.mode == "TERMINAL":
                view = TerminalView(self.gs)
                result = view.run()
                if result == "SWITCH":
                    self.mode = "PYGAME"
                else:
                    break

            elif self.mode == "PYGAME":
                view = PygameView(self.gs)
                result = view.run()
                if result == "SWITCH":
                    self.mode = "TERMINAL"
                else:
                    break