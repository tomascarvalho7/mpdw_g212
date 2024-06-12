from typing import Optional, Tuple
from DialogManager_TWIZ.dialog_factory.dialog_elements import AbstractEvent, AbstractState
from DialogManager_TWIZ.dialog_factory.flows import BackboneFlow

class EndState (AbstractState, BackboneFlow):
    def __init__(self):
        self.data = []

    def event_in(self, event: AbstractEvent, history: list, state_manager: dict) -> Tuple[Optional[AbstractEvent], str]:
        msg = "Are you sure you want to leave?"
        confirm = input("(yes/no): ")
        if confirm == "yes":
                quit()

        return None, {"response": msg, "screen": ""}
    
    def event_out(self, event: AbstractEvent, history: list, state_manager: dict) -> Optional[AbstractEvent]:
       return

    @staticmethod
    def register_transitions_in() -> dict:
        from DialogManager_TWIZ.events.stop_event import StopEvent
        from DialogManager_TWIZ.states.start_state import StartState
        from DialogManager_TWIZ.states.choose_type_state import ChooseTypeState
        from DialogManager_TWIZ.states.display_recipe_state import DisplayRecipeState
        from DialogManager_TWIZ.states.question_image_state import QuestionImageState
        from DialogManager_TWIZ.states.display_recipe_state import DisplayRecipeState
    
        return {
            DisplayRecipeState: [StopEvent],
            ChooseTypeState: [StopEvent],
            QuestionImageState: [StopEvent]
        }