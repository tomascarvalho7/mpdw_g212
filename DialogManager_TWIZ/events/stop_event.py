from DialogManager_TWIZ.dialog_factory.dialog_elements import AbstractEvent

class StopEvent(AbstractEvent):
    id = "Stop"
    description = ""

    def __init__(self):
        pass

    @staticmethod
    def is_valid(state_manager: dict):
        return state_manager["intent"] == StopEvent.id
