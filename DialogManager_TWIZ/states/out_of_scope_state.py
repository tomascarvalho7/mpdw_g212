from DialogManager_TWIZ.dialog_factory.dialog_elements import AbstractState
from DialogManager_TWIZ.dialog_factory.flows import BackboneFlow

class OutOfScopeState (AbstractState, BackboneFlow):
    def __init__(self):
        self.data = []

    def event_in(self, event) :
        print("Sorry I cannot help you with that")
        return

    def event_out(self, event) :
       return
