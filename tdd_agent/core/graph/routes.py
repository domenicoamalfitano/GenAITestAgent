from tdd_agent.config import RESPONSE_TESTS_ENOUGH, MAX_RETRIES, RESPONSE_ALL_TESTS_PASSED, RESPONSE_REFACTORING_COMPLETE
from tdd_agent.core.graph.state import TDDState
from typing import Literal


def route_after_red(state: TDDState) -> Literal["green", "red", "__end__"]:
    if RESPONSE_TESTS_ENOUGH in state["result_test"]:
        return "__end__"
    if state["attempt_red"] >= MAX_RETRIES:
        return "__end__"
    if not state["result_test"]:
        return "red"
    return "green"


def route_after_green(state: TDDState) -> Literal["refactor", "green"]:
    if RESPONSE_ALL_TESTS_PASSED in state["result_source"]:
        return "refactor"
    if state["attempt_green"] >= MAX_RETRIES:
        return "refactor"
    return "green"


def route_after_refactor(state: TDDState) -> Literal["red", "__end__"]:
    done = (
        RESPONSE_ALL_TESTS_PASSED in state["result_refactor"]
        and RESPONSE_REFACTORING_COMPLETE in state["result_refactor"]
    )
    if done or state["attempt_refactor"] >= MAX_RETRIES:
        
        if state["attempt_red"] >= MAX_RETRIES:
            return "__end__"
        return "red"
    return "refactor"
