from DialogManager_TWIZ.dialog_factory.dialog_elements import AbstractEvent

class YesEvent(AbstractEvent):
    id = "Yes"
    description = ""

    def __init__(self):
        pass

    @staticmethod
    def is_valid(state_manager: dict):
        return state_manager["intent"] == YesEvent.id
