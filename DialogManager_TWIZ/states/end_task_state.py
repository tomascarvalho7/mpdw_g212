from typing import Optional, Tuple
from DialogManager_TWIZ.dialog_factory.dialog_elements import AbstractEvent, AbstractState
from DialogManager_TWIZ.dialog_factory.flows import BackboneFlow

class EndTaskState (AbstractState, BackboneFlow):
    def __init__(self):
        self.data = []

    def event_in(self, event: AbstractEvent, history: list, state_manager: dict) -> Tuple[Optional[AbstractEvent], str]:
        msg = "Are you sure you want to stop the task?"

        return None, {"response": msg, "screen": ""}
    
    def event_out(self, event: AbstractEvent, history: list, state_manager: dict) -> Optional[AbstractEvent]:
       return

    @staticmethod
    def register_transitions_in() -> dict:
        from DialogManager_TWIZ.events.stop_event import StopEvent
        from DialogManager_TWIZ.states.conversation_state import ConversationState
    
        return {
            ConversationState: [StopEvent]
        }