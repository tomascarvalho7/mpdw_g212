from TWIZ.example.dialog_factory.dialog_elements import AbstractState, AbstractEvent
from states import StartState
from events import *

class ChooseTypeState (AbstractState):
    def __init__(self):
        self.data = []

    def event_in(self, event) :
        print("What type of recipe do you want?")
        return

    def event_out(self, event) :
        print("Great option!")
        return
    
    # define transitions from other states to this state with events
    # last_state --- [event,...] ---> self_state
    @staticmethod
    def register_transitions_in() -> dict:
        return {
            StartState: [ChooseTypeState]
        }
