from langgraph.prebuilt import ToolNode

from src.agent.tools import ALL_TOOLS


tool_node = ToolNode(
    ALL_TOOLS,
    handle_tool_errors=True,
)