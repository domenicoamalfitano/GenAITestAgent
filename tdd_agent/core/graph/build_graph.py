from tdd_agent.core.graph.nodes import red_node, green_node, refactor_node
from tdd_agent.core.graph.routes import route_after_red, route_after_green, route_after_refactor
from tdd_agent.core.graph.state import TDDState
from langgraph.graph import StateGraph


def build_tdd_graph() -> StateGraph:
    builder = StateGraph(TDDState)

    builder.add_node("red", red_node)
    builder.add_node("green", green_node)
    builder.add_node("refactor", refactor_node)

    builder.set_entry_point("red")

    builder.add_conditional_edges("red",     route_after_red)
    builder.add_conditional_edges("green",   route_after_green)
    builder.add_conditional_edges("refactor", route_after_refactor)

    return builder.compile()
