from langgraph.graph import StateGraph,START,END
from langgraph.prebuilt import ToolNode
from src.agent.state import AgentState
from src.agent.nodes.agent_node import agent_node
from src.agent.nodes.tool_node import tool_node


def should_continue(state):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return END


def build_graph():

    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node(
        "agent",
        agent_node
    )

    graph.add_node(
        "tools",
        tool_node
    )

    # Start
    graph.add_edge(
        START,
        "agent"
    )

    # Agent decides what happens next
    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            END: END
        }
    )

    # Tool results go back to agent
    graph.add_edge(
        "tools",
        "agent"
    )

    return graph.compile()