from typing import Optional, Tuple
from DialogManager_TWIZ.dialog_factory.dialog_elements import AbstractEvent, AbstractState
from DialogManager_TWIZ.dialog_factory.flows import BackboneFlow
import pprint as pp

class ConversationState (AbstractState, BackboneFlow):
    def __init__(self):
        self.data = []
        self.recipe = {}
        

    def event_in(self, event: AbstractEvent, history: list, state_manager: dict) -> Tuple[Optional[AbstractEvent], str]:
        pllm = state_manager["pllm"]

        screen = ""
        if(type(history[history.__len__() - 1]).__name__ == "DisplayRecipeState"):
            fullRecipe = state_manager["search"].SearchSingleTitleAndDescriptionTxtInstructions(state_manager["recipes"][state_manager["recipeCount"]]["title"])
            state_manager["instructions"] = fullRecipe["hits"]["hits"][0]["_source"]['instructions']
            state_manager["conversationJSON"] = pllm.generate_base_json(fullRecipe, state_manager["conversationJSON"]["dialog"])

        screen += state_manager["instructions"][state_manager["step"]]['stepImg']
        ai_response = pllm.send_to_planllm(state_manager["conversationJSON"]).replace('"', '')

        state_manager["conversationJSON"] = pllm.add_to_json(state_manager["conversationJSON"], "ai", ai_response, state_manager["step"])

        return None, {"response": ai_response, "screen": screen, "planJSON": state_manager["conversationJSON"], "instructions": self.recipe}
    
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