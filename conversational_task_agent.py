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
from DialogManager_TWIZ.states.question_image_state import QuestionImageState
from DialogManager_TWIZ.states.end_state import EndState
from DialogManager_TWIZ.states.end_task_state import EndTaskState
from DialogManager_TWIZ.events.greetings_event import GreetingsEvent
from DialogManager_TWIZ.events.question_event import QuestionEvent
from DialogManager_TWIZ.events.question_image_event import QuestionImageEvent
from DialogManager_TWIZ.events.start_task_event import StartTaskEvent
from DialogManager_TWIZ.events.out_of_scope_event import OutOfScopeEvent
from DialogManager_TWIZ.events.yes_event import YesEvent
from modules.IntentDetector import IntentDetector
from modules.Search import Search
from modules.SlotFilling import SlotFilling
from modules.PlanLLMUtils import PlanLLMUtils
from modules.QuestionImage import QuestionImage
from IPython.display import display
import requests
from PIL import Image
import json
import pprint as pp


dialog_manager = DialogManager()
intentDetector = IntentDetector()
search = Search()
slotFilling = SlotFilling()
pllm = PlanLLMUtils()
questionImg = QuestionImage()

state = {
    "intent": "",
    "userInput": "",
    "screen": "",
    "recipeCount": 0,
    "step": 0,
    "slotFilling" : slotFilling,
    "search" : search,
    "recipes" : [],
    "conversationJSON" : {"dialog": []},
    "pllm" : pllm,
    "questionImg": questionImg
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
        
        # GreetingsEvent
        "GreetingIntent": GreetingsEvent,

        # QuestionEvent
        "ChitChatIntent": QuestionEvent,
        "GetCuriositiesIntent": QuestionEvent,
        "QuestionIntent": QuestionEvent,
        "HelpIntent": QuestionEvent,
        
        # NextEvent
        "MoreOptionsIntent": NextEvent,
        "RepeatIntent": NextEvent,
        "GoToStepIntent": NextEvent,
        "PreviousStepIntent": NextEvent,
        "SuggestionsIntent": NextEvent,
        "IngredientsConfirmationIntent": NextEvent,
        "NextStepIntent": NextEvent,

        # YesEvent
        "YesIntent": YesEvent,
        
        # OutOfScopeEvent
        "ProvideUserNameIntent": OutOfScopeEvent,
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
    print("Doobie Bot:", response['response'])

    while True:
        userInput = input("You: ")
        state["userInput"] = userInput
        
        intent = intentDetector.detect_intent(userInput)
        state["intent"] = map_intents_to_events(intent).id

        event = dialog_manager.event_type(state)
        if (event.id == "Question" and state["screen"] != ""): event = QuestionImageEvent
        currState = dialog_manager.get_state()

        if (isInConversation(event, currState)):
            state["conversationJSON"] = pllm.add_to_json(state["conversationJSON"], "user", userInput, state["step"])

        responseString = "Doobie Bot: "
        response = dialog_manager.trigger(event, state)

        if (response["screen"] != "" and response["screen"] != None): 
            state["screen"] = response["screen"]
            printImage(Image.open(requests.get(state["screen"], stream=True).raw))

        if (isInConversation(event, currState)):
            responseString += response['planJSON']['dialog'][state["step"]]["system"]
            state["conversationJSON"] = response['planJSON']
            state["step"] += 1
        else:
            responseString += response['response']

        print(responseString)
            

def isInConversation(event, state):
    return (event.id != "Stop" and state == "ConversationState") or (event.id == "StartTask" and state == "DisplayRecipeState")

def printImage(img):
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg

    # Display the image
    plt.imshow(img)
    plt.axis('off')  # Hide the axes
    plt.show(block=False)
run_dialog_manager() # run !
