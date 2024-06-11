from typing import Optional, Tuple
from DialogManager_TWIZ.dialog_factory.dialog_elements import AbstractEvent, AbstractState
from DialogManager_TWIZ.dialog_factory.flows import BackboneFlow

class StartState (AbstractState, BackboneFlow):
    def __init__(self):
        self.data = []

    def event_in(self, event: AbstractEvent, history: list, state_manager: dict) -> Tuple[Optional[AbstractEvent], str]:
        msg = "Hello, how can I help you search for a recipe?"

        return None, {"response": msg, "screen": ""}
    
    def event_out(self, event: AbstractEvent, history: list, state_manager: dict) -> Optional[AbstractEvent]:
       return

    # define transitions from other states to this state with events
    # last_state --- [event,...] ---> self_state
    @staticmethod
    def register_transitions_in() -> dict:
        from DialogManager_TWIZ.dialog_factory.dialog_manager import LaunchEvent, LaunchState
        from DialogManager_TWIZ.events.stop_event import StopEvent
        from DialogManager_TWIZ.events.out_of_scope_event import OutOfScopeEvent
        from DialogManager_TWIZ.states.display_recipe_state import DisplayRecipeState
    
        return {
            LaunchState: [LaunchEvent],
            StartState: [OutOfScopeEvent],
            DisplayRecipeState: [StopEvent],
        }