## Run Dialog Manaager
from DialogManager_TWIZ.dialog_factory.dialog_manager import DialogManager
from DialogManager_TWIZ.dialog_factory.dialog_elements import LaunchEvent
from DialogManager_TWIZ.events.choose_type_event import ChooseType
from DialogManager_TWIZ.events.next_event import NextEvent
from DialogManager_TWIZ.events.stop_event import StopEvent
from DialogManager_TWIZ.states.start_state import StartState
from DialogManager_TWIZ.states.choose_type_state import ChooseTypeState
from DialogManager_TWIZ.states.display_recipe_state import DisplayRecipeState
from DialogManager_TWIZ.states.conversation_state import ConversationState
from DialogManager_TWIZ.states.end_state import EndState
from DialogManager_TWIZ.events.greetings_event import GreetingsEvent
from DialogManager_TWIZ.events.start_task_event import StartTaskEvent
from DialogManager_TWIZ.events.out_of_scope_event import OutOfScopeEvent
from modules.IntentDetector import IntentDetector
from modules.Search import Search
from modules.SlotFilling import SlotFilling
from modules.PlanLLMUtils import PlanLLMUtils
import json
import pprint as pp


dialog_manager = DialogManager()
intentDetector = IntentDetector()
search = Search()
slotFilling = SlotFilling()
pllm = PlanLLMUtils()

state = {
    "intent": "",
    "userInput": "",
    "recipeCount": 0,
    "step": 0,
    "slotFilling" : slotFilling,
    "search" : search,
    "recipes" : [],
    "conversationJSON" : {"dialog": []},
    "pllm" : pllm
}

def map_intents_to_events(intent):
    intent_event_mapping = {
        # ChooseTypeEvent
        "SelectIntent": ChooseType,
        "IdentifyRestrictionsIntent": ChooseType,
        "AdjustServingsIntent": ChooseType,
        "NoRestrictionsIntent": ChooseType,
        "SubstitutionIntent": ChooseType,
        "IdentifyProcessIntent": ChooseType,
        "HelpIntent": ChooseType,
        
        # GreetingsEvent
        "GreetingIntent": GreetingsEvent,
        "ChitChatIntent": GreetingsEvent,
        
        # NextEvent
        "MoreOptionsIntent": NextEvent,
        "RepeatIntent": NextEvent,
        "GoToStepIntent": NextEvent,
        "PreviousStepIntent": NextEvent,
        "SuggestionsIntent": NextEvent,
        "IngredientsConfirmationIntent": NextEvent,
        "NextStepIntent": NextEvent,
        "YesIntent": NextEvent,
        
        # OutOfScopeEvent
        "GetCuriositiesIntent": OutOfScopeEvent,
        "ProvideUserNameIntent": OutOfScopeEvent,
        "QuestionIntent": OutOfScopeEvent,
        "MoreDetailIntent": OutOfScopeEvent,
        "OutOfScopeIntent": OutOfScopeEvent,
        "FallbackIntent": OutOfScopeEvent,
        "NoneOfTheseIntent": OutOfScopeEvent,
        "InappropriateIntent": OutOfScopeEvent,
        
        # StartTaskEvent
        "ShowStepsIntent": StartTaskEvent,
        "SetTimerIntent": StartTaskEvent,
        "ShoppingIntent": StartTaskEvent,
        "StartStepsIntent": StartTaskEvent,
        "ResumeTaskIntent": StartTaskEvent,
        
        # StopEvent
        "TerminateCurrentTaskIntent": StopEvent,
        "CompleteTaskIntent": StopEvent,
        "PauseIntent": StopEvent,
        "CancelIntent": StopEvent,
        "NoIntent": StopEvent,
        "StopIntent": StopEvent,
    }
    return intent_event_mapping[intent]

def run_dialog_manager():
    response = dialog_manager.trigger(LaunchEvent(), state)
    print(response['response'])

    while True:
        userInput = input("Intent: ")
        state["userInput"] = userInput
        
        intent = intentDetector.detect_intent(userInput)
        state["intent"] = map_intents_to_events(intent).id

        event = dialog_manager.event_type(state)
        currState = dialog_manager.get_state()

        if (currState == "EndState"):
            confirm = input("(yes/no): ")
            if confirm == "yes":
                break
            else:
                state["intent"] = "SelectIntent"

        if (isInConversation(event, currState)):
            state["conversationJSON"] = pllm.add_to_json(state["conversationJSON"], "user", userInput, state["step"])

        response = dialog_manager.trigger(event, state)

        if (isInConversation(event, currState)):
            treated_response = response['response'].replace("'", "\"")
            print(json.loads(treated_response)['dialog'][state["step"]]["system"])
        else:
            print(response['response'])

        if (isInConversation(event, currState)):
            treated_response = response['response'].replace("'", "\"")
            state["conversationJSON"] = json.loads(treated_response)
            state["step"] += 1

def isInConversation(event, state):
    return (event.id != "Stop" and state == "ConversationState") or (event.id == "StartTask" and state == "DisplayRecipeState")

run_dialog_manager() # run !
