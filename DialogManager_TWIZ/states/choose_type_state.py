from typing import Optional, Tuple
from DialogManager_TWIZ.dialog_factory.dialog_elements import AbstractState, AbstractEvent
from DialogManager_TWIZ.dialog_factory.flows import BackboneFlow

class ChooseTypeState (AbstractState, BackboneFlow):
    def __init__(self):
        self.data = []

    def event_in(self, event: AbstractEvent, history: list, state_manager: dict) -> Tuple[Optional[AbstractEvent], object]:
        msg = "What type of recipe do you want?"
        return None, {"response": msg, "screen": ""}

    def event_out(self, event: AbstractEvent, history: list, state_manager: dict) -> Optional[AbstractEvent]:
        print("Great option!")
        return
    
    # define transitions from other states to this state with events
    # last_state --- [event,...] ---> self_state
    @staticmethod
    def register_transitions_in() -> dict:
        from DialogManager_TWIZ.states.start_state import StartState
        from DialogManager_TWIZ.events.out_of_scope_event import OutOfScopeEvent
        from DialogManager_TWIZ.events.greetings_event import GreetingsEvent
        from DialogManager_TWIZ.events.stop_event import StopEvent
        from DialogManager_TWIZ.events.choose_type_event import ChooseType

        return {
            StartState: [GreetingsEvent, StopEvent, ChooseType]
        }
