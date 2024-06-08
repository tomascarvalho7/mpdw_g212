from TWIZ.example.dialog_factory.dialog_elements import AbstractState, AbstractEvent
from states import StartState
from events import *

class OutOfScopeState (AbstractState):
    def __init__(self):
        self.data = []

    def event_in(self, event) :
        print("Sorry I cannot help you with that")
        return

    def event_out(self, event) :
        return
    
    # define transitions from other states to this state with events
    # last_state --- [event,...] ---> self_state
    @staticmethod
    def register_transitions_in() -> dict:
        return {
            StartState: [OutOfScopeState],
            OutOfScopeState: [OutOfScopeState]
        }
