from TWIZ.example.dialog_factory.dialog_elements import AbstractState, AbstractEvent

class StartState (AbstractState):
    def __init__(self):
        self.data = []

    def event_in(self, event) :
        print("Hello, how can I help you search for a recipe?")
        return
