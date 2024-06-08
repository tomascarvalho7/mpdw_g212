from typing import Type, Optional, List, Dict

from example.dialog_factory.dialog_elements import AbstractEvent, AbstractState, LaunchState, LaunchEvent
from example.dialog_factory.flows import BackboneFlow
from graph_visualizer.graph_visualizer import print_dot


class DialogManager:

    def __init__(self, start_state: AbstractState = LaunchState(), history: List[AbstractState] = []):
        self.states: List[Type[AbstractState]] = AbstractState.__subclasses__()
        self.states_flow: Dict[str, str] = {state.__name__: self.get_state_flow(state) for state in self.states}
        self.events: List[Type[AbstractEvent]] = AbstractEvent.__subclasses__()

        self.transitions: Dict[(Type[AbstractState], Type[AbstractEvent]), Type[AbstractState]] = {}

        self.history: List[AbstractState] = history
        self.checkpoint: List[(str, AbstractState)] = [(BackboneFlow.__name__, start_state)]

        for state in self.states:
            # old_state --- event ---> self_state
            state_transitions = state.register_transitions_in()
            if state_transitions:
                for last_state, events in state_transitions.items():
                    for event in events:
                        if (last_state, event) in self.transitions:
                            print(
                                f"Warning: Transitions conflict ({(last_state, event)})")
                        else:
                            self.transitions[(last_state, event)] = state

            # old_state --- event ---> self_state
            state_transitions = state.register_subflow_transitions_in()
            if state_transitions:
                for accepted_flow, events in state_transitions.items():
                    for event in events:
                        flow_states = accepted_flow.__subclasses__()
                        for last_state in flow_states:
                            if (last_state, event) in self.transitions:
                                print(
                                    f"Warning: Transitions conflict ({(last_state, event)})")
                            else:
                                self.transitions[(last_state, event)] = state

        self.print_status()
        # print_dot(self.states)

        self.trigger(LaunchEvent())

    def trigger(self, event: AbstractEvent, state_manager: dict = {}) -> dict:
        responder_candidates = []

        while event:
            print("## CURRENT STATE:", type(self.checkpoint[-1][1]).__name__, "## EVENT:", type(event).__name__)

            for (flow, state) in reversed(self.checkpoint):
                print("## CANDIDATE", flow, type(state).__name__)
                if (type(state), type(event)) in self.transitions:

                    # Next state returned by previous state or by registered transitions
                    out_event = state.event_out(event, self.history, state_manager)
                    event = out_event if out_event else event

                    # Check transition with current state and deal with any received event
                    next_state = self.transitions[(type(state), type(event))]
                    current_state = next_state()
                    event, responders = current_state.event_in(event, self.history, state_manager)
                    responder_candidates.append(responders)
                    print("## TRANSITION FOUND", type(state).__name__, "->", type(current_state).__name__)

                    # Update checkpoint stack and history
                    while self.checkpoint[-1][0] != flow:
                        self.checkpoint.pop()

                    current_flow = self.states_flow[type(current_state).__name__]
                    if current_flow == flow:
                        self.checkpoint[-1] = (current_flow, current_state)
                    else:
                        self.checkpoint.append((current_flow, current_state))

                    print("## CHECKPOINT:", [(f, type(s).__name__) for (f, s) in self.checkpoint])
                    self.history.append(current_state)
                    break

            if not responder_candidates:
                # do something, re-prompt?
                print("## NO TRANSITION FOUND FOR THIS EVENT, RESPONDING WITH FALLBACK")
                responder_candidates.append({"response": "I'm sorry, I couldn't quite get you, could you please rephrase?"})
                break

        response = ' '.join([r['response'] for r in responder_candidates])
        screen = next((r['screen']for r in responder_candidates if 'screen' in r), None)

        return {'response': response, 'screen': screen}

    def event_type(self, state_manager: dict) -> Optional[Type[AbstractEvent]]:
        for event in self.events:
            if event.is_valid(state_manager):
                for fine_grained_event in event.__subclasses__():
                    if fine_grained_event.is_valid(state_manager):
                        return fine_grained_event
                return event
        raise Exception("No event defined for the detected intent")

    def print_status(self):
        print("## STATES #########################################")
        [print(state.__name__) for state in self.states]
        print("###################################################")

        print("## EVENTS #########################################")
        [print(event.__name__) for event in self.events]
        print("###################################################")
        print()

        print()
        print("## TRANSITIONS ### S-E->S #########################")
        for (a, b), c in self.transitions.items():
            print(a.__name__, "-", b.__name__, " -> ", c.__name__)
        print("###################################################")
        print()

    @staticmethod
    def get_state_flow(state: Type[AbstractState]) -> Optional[str]:
        classes = map(lambda x: x.__name__, state.__bases__)
        flow = list(filter(lambda x: "flow" in x.lower(), classes))
        return flow[0] if flow else None
