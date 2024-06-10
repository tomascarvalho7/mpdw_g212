from DialogManager_TWIZ.dialog_factory.dialog_elements import AbstractEvent

class NextEvent(AbstractEvent):
    id = "Next"
    description = ""

    def __init__(self):
        pass

    @staticmethod
    def is_valid(state_manager: dict):
        return state_manager["intent"] == NextEvent.id
