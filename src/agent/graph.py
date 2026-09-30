from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END

from src.agent.state import AgentState
from src.agent.nodes.agent_node import agent_node
from src.agent.nodes.tool_node import tool_node


def should_continue(state: AgentState):
    last_message = state["messages"][-1]

    if getattr(last_message, "tool_calls", None):
        return "tools"

    return END


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)

    graph.add_edge(START, "agent")

    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            END: END,
        },
    )

    graph.add_edge("tools", "agent")

    checkpointer = MemorySaver()

    return graph.compile(
        checkpointer=checkpointer
    )