from typing import Optional, Tuple
from DialogManager_TWIZ.dialog_factory.dialog_elements import AbstractEvent, AbstractState
from DialogManager_TWIZ.dialog_factory.flows import BackboneFlow
from DialogManager_TWIZ.events.choose_type_event import ChooseType
from DialogManager_TWIZ.events.next_event import NextEvent

class DisplayRecipeState (AbstractState, BackboneFlow):
    def __init__(self):
        self.data = []

    def event_in(self, event: AbstractEvent, history: list, state_manager: dict) -> Tuple[Optional[AbstractEvent], str]:
        msg = ""
        if isinstance(event, ChooseType):
            msg += "Here is the top suggested recipe:"
            # get recipes

        if isinstance(event, NextEvent):
            msg += "Here is the next suggested recipe:"
            # get recipes

        msg += "\nFeel free to ask for the next recipe."
        return None, {"response": msg, "screen": ""}

    def event_out(self, event: AbstractEvent, history: list, state_manager: dict) -> Optional[AbstractEvent]:
       return
    
    # define transitions from other states to this state with events
    # last_state --- [event,...] ---> self_state
    @staticmethod
    def register_transitions_in() -> dict:
        from DialogManager_TWIZ.events.out_of_scope_event import OutOfScopeEvent
        from DialogManager_TWIZ.states.choose_type_state import ChooseTypeState

        return {
            ChooseTypeState: [ChooseType],
            DisplayRecipeState: [OutOfScopeEvent, NextEvent]
        }
