
from TWIZ.example.dialog_factory.dialog_elements import AbstractEvent

class OutOfScopeEvent(AbstractEvent):
    id = "OutOfScope"
    description = ""

    def __init__(self):
        pass

    @staticmethod
    def is_valid(state_manager: dict):
        return state_manager["intent"] == OutOfScopeEvent.id