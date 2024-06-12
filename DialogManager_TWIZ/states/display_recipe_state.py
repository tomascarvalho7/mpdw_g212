from typing import Optional, Tuple
from DialogManager_TWIZ.dialog_factory.dialog_elements import AbstractEvent, AbstractState
from DialogManager_TWIZ.dialog_factory.flows import BackboneFlow
from DialogManager_TWIZ.events.choose_type_event import ChooseType
from DialogManager_TWIZ.events.next_event import NextEvent
from modules.SlotFilling import SlotFilling
from modules.Search import Search
import pprint as pp

class DisplayRecipeState (AbstractState, BackboneFlow):
    def __init__(self):
        self.data = []

    def event_in(self, event: AbstractEvent, history: list, state_manager: dict) -> Tuple[Optional[AbstractEvent], str]:
        msg = ""
        if event.id != NextEvent.id:
            recipe = state_manager["slotFilling"].extract_slot(state_manager["userInput"], "What is the recipe?")
            searchedRecipe = state_manager["search"].SearchTitleEmbeddings(recipe)
            state_manager["recipes"] = []
            for hit in searchedRecipe["hits"]["hits"]:
                recipe = {
                    "title": hit["_source"]["title"],
                    "images": hit["_source"]["images"]
                }
                state_manager["recipes"].append(recipe)

            msg += "Here is the top suggested recipe:"

        if event.id == NextEvent.id:
            state_manager["recipeCount"] = state_manager["recipeCount"] + 1
            msg += "Here is the next suggested recipe:"
            # get recipes
        
        recipe = state_manager["recipes"][state_manager["recipeCount"]]
        msg += recipe["title"]
        screen = ""
        if len(recipe["images"]) > 0: screen = recipe["images"][0]["url"]
        msg += ". Feel free to ask for the next recipe."
        return None, {"response": msg, "screen": screen, "planJSON": state_manager["conversationJSON"]}

    def event_out(self, event: AbstractEvent, history: list, state_manager: dict) -> Optional[AbstractEvent]:
       return
    
    # define transitions from other states to this state with events
    # last_state --- [event,...] ---> self_state
    @staticmethod
    def register_transitions_in() -> dict:
        from DialogManager_TWIZ.events.question_event import QuestionEvent
        from DialogManager_TWIZ.states.choose_type_state import ChooseTypeState
        from DialogManager_TWIZ.states.start_state import StartState
        from DialogManager_TWIZ.states.end_state import EndState

        return {
            StartState: [ChooseType, QuestionEvent],
            ChooseTypeState: [ChooseType, QuestionEvent],
            DisplayRecipeState: [ChooseType, NextEvent],
            EndState: [ChooseType, QuestionEvent]
        }
