from langgraph.graph import StateGraph, START, END
from src.agent.state import AgentState
from src.agent.nodes.router_node import router_node
from src.agent.nodes.rag_node import rag_node
from src.agent.nodes.customer_node import customer_node
from src.agent.nodes.subscription_node import subscription_node
from src.agent.nodes.transcation_node import transaction_node
from src.agent.nodes.ticket_node import ticket_node


def route_after_classifier(state: AgentState):

    route = state['route']

    destination = []

    if route.requires_knowledge:
        destination.append("rag")

    if route.requires_customer_lookup:
        destination.append("customer")

    if route.requires_subscription_lookup:
        destination.append("subscription")

    if route.requires_transaction_lookup:
        destination.append("transaction")

    if route.requires_ticket_lookup:
        destination.append("ticket")

    return destination

def build_graph():
    graph = StateGraph(AgentState)

    #Nodes
    graph.add_node("router" , router_node)
    graph.add_node("customer", customer_node)
    graph.add_node("rag", rag_node)
    graph.add_node("subscription", subscription_node)
    graph.add_node("transaction", transaction_node)
    graph.add_node("ticket", ticket_node)

    #START
    graph.add_edge(START, "router")

    #router -> required_systems
    graph.add_conditional_edges(
            "router",
            route_after_classifier,
            {
                "rag": "rag",
                "customer": "customer",
                "subscription": "subscription",
                "transaction": "transaction",
                "ticket": "ticket",
            }
        )

    #temp ending
    graph.add_edge("rag", END)
    graph.add_edge("customer", END)
    graph.add_edge("subscription", END)
    graph.add_edge("transaction", END)
    graph.add_edge("ticket", END)

    return graph.compile()