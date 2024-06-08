from abc import ABC
from typing import Optional, Tuple


class AbstractEvent(ABC):
    id = "AbstractEvent"
    pass

    @staticmethod
    def is_valid(state_manager: dict):
        pass


class AbstractState(ABC):

    # define all events
    def __init__(self):
        # { event: function, ... }
        pass

    # operations done when entering the state
    def event_in(self, event: AbstractEvent, history: list, state_manager: dict) -> Tuple[Optional[AbstractEvent], str]:
        pass

    # operations done when leaving the state
    def event_out(self, event: AbstractEvent, history: list, state_manager: dict) -> Optional[AbstractEvent]:
        pass

    # define transitions from other states to this state with events
    # last_state --- [event,...] ---> self_state
    @staticmethod
    def register_transitions_in() -> dict:
        pass

    # define transitions from other states in a flow to this state with events
    # flow --- [event,...] ---> self_state
    @staticmethod
    def register_subflow_transitions_in() -> dict:
        pass


class LaunchState(AbstractState):
    def __init__(self):
        return

    def event_in(self, event: AbstractEvent, history: list, state_manager: dict) -> Tuple[Optional[AbstractEvent], str]:
        return

    def event_out(self, event: AbstractEvent, history: list, state_manager: dict) -> Optional[AbstractEvent]:
        return

    @staticmethod
    def register_transitions_in() -> dict:
        return

    @staticmethod
    def register_subflow_transitions_in() -> dict:
        return


class LaunchEvent(AbstractEvent):
    pass
