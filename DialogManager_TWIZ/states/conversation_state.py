from typing import Optional, Tuple
from DialogManager_TWIZ.dialog_factory.dialog_elements import AbstractEvent, AbstractState
from DialogManager_TWIZ.dialog_factory.flows import BackboneFlow
import pprint as pp

class ConversationState (AbstractState, BackboneFlow):
    def __init__(self):
        self.data = []

    def event_in(self, event: AbstractEvent, history: list, state_manager: dict) -> Tuple[Optional[AbstractEvent], str]:
        pllm = state_manager["pllm"]
        convo_json = state_manager["conversationJSON"]

        if(type(history[history.__len__() - 1]).__name__ == "DisplayRecipeState"):
            fullRecipe = state_manager["search"].SearchSingleTitleAndDescriptionTxtInstructions(state_manager["recipes"][state_manager["recipeCount"]])
            convo_json = pllm.generate_base_json(fullRecipe, state_manager["conversationJSON"]["dialog"])

        ai_response = pllm.send_to_planllm(convo_json)

        response = pllm.add_to_json(convo_json, "ai", ai_response.replace('"', ''), state_manager["step"])

        return None, {"response": str(response), "screen": ""}
    
    def event_out(self, event: AbstractEvent, history: list, state_manager: dict) -> Optional[AbstractEvent]:
       return

    # define transitions from other states to this state with events
    # last_state --- [event,...] ---> self_state
    @staticmethod
    def register_transitions_in() -> dict:
        from DialogManager_TWIZ.dialog_factory.dialog_manager import LaunchEvent
        from DialogManager_TWIZ.states.display_recipe_state import DisplayRecipeState
        from DialogManager_TWIZ.events.greetings_event import GreetingsEvent
        from DialogManager_TWIZ.events.next_event import NextEvent
        from DialogManager_TWIZ.events.start_task_event import StartTaskEvent
        from DialogManager_TWIZ.events.out_of_scope_event import OutOfScopeEvent

        return {
            ConversationState: [LaunchEvent, GreetingsEvent, NextEvent, StartTaskEvent, OutOfScopeEvent],
            DisplayRecipeState: [StartTaskEvent, LaunchEvent, GreetingsEvent],
        }