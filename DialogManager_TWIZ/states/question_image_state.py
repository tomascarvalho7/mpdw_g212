from typing import Optional, Tuple
from DialogManager_TWIZ.dialog_factory.dialog_elements import AbstractEvent, AbstractState
from DialogManager_TWIZ.dialog_factory.flows import BackboneFlow
from PIL import Image
import requests

class QuestionImageState (AbstractState, BackboneFlow):
    def __init__(self):
        self.data = []

    def event_in(self, event: AbstractEvent, history: list, state_manager: dict) -> Tuple[Optional[AbstractEvent], str]:
        module = state_manager["questionImg"]
        intent = state_manager["userInput"]
        image = Image.open(requests.get(state_manager["screen"], stream=True).raw)
        answer = module.ask(intent, image)
        print(intent)
        print(image)
        
        return None, {"response": "The answer is: " + answer + ". Feel free to ask me more questions."}

    def event_out(self, event: AbstractEvent, history: list, state_manager: dict) -> Optional[AbstractEvent]:
       return
    
    # define transitions from other states to this state with events
    # last_state --- [event,...] ---> self_state
    @staticmethod
    def register_transitions_in() -> dict:
        from DialogManager_TWIZ.states.display_recipe_state import DisplayRecipeState
        from DialogManager_TWIZ.states.conversation_state import ConversationState
        from DialogManager_TWIZ.events.question_image_event import QuestionImageEvent
        from DialogManager_TWIZ.events.next_event import NextEvent
        from DialogManager_TWIZ.events.out_of_scope_event import OutOfScopeEvent
        from DialogManager_TWIZ.events.stop_event import StopEvent

        return {
            DisplayRecipeState: [QuestionImageEvent],
            ConversationState: [QuestionImageEvent],
            QuestionImageState: [QuestionImageEvent, NextEvent, OutOfScopeEvent, StopEvent]
        }
