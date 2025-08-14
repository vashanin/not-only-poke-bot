from langchain_core.messages import ToolMessage
from .tools import tool_to_node_mapping


def get_next_node(messages, default, depth: int = 2):
    for msg in reversed(messages[-depth:]):
        if isinstance(msg, ToolMessage):
            for tool_name, node_name in tool_to_node_mapping.items():
                if msg.name == tool_name:
                    return node_name
            return default

    return default
