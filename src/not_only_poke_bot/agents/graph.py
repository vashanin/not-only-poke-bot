from typing import Literal

from langfuse import get_client

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.graph import MessagesState, END
from langgraph.types import Command, Checkpointer
from langgraph.checkpoint.redis import RedisSaver

from langgraph.graph import StateGraph, START
from langgraph.graph.state import CompiledStateGraph

from .tools import (
    ask_researcher,
    ask_pokemon_expert,
    get_pokemon_data,
    tavily_tool,
)

from core.settings import settings
from .utils import get_next_node


class Graph:
    llm = ChatOpenAI(model=settings.openai.model, reasoning_effort=settings.openai.reasoning_effort)
    langfuse = get_client()

    def __init__(self, answer_key: str, answer_example: str):
        self.supervisor_agent = create_react_agent(
            self.llm,
            tools=[ask_researcher],
            prompt=self.langfuse.get_prompt("supervisor").compile(),
        )

        self.research_agent = create_react_agent(
            self.llm,
            tools=[get_pokemon_data, ask_pokemon_expert, tavily_tool],
            prompt=self.langfuse.get_prompt("researcher").compile(),
        )

        self.pokemon_expert_agent = create_react_agent(
            self.llm,
            tools=[],
            prompt=self.langfuse.get_prompt("pokemon-expert").compile(
                answer_key=answer_key, answer_example=answer_example
            ),
        )

    def supervisor_node(self, state: MessagesState) -> Command[Literal["researcher", END]]:
        result = self.supervisor_agent.invoke(state)
        goto = get_next_node(result["messages"], default=END)

        return Command(update={"messages": result["messages"]}, goto=goto)

    def researcher_node(self, state: MessagesState) -> Command[Literal["pokemon_expert", END]]:
        result = self.research_agent.invoke(state)
        goto = get_next_node(result["messages"], default=END)

        return Command(update={"messages": result["messages"]}, goto=goto)

    def pokemon_expert_node(self, state: MessagesState) -> Command[Literal[END]]:
        result = self.pokemon_expert_agent.invoke(state)

        return Command(update={"messages": result["messages"]})

    @classmethod
    def get_checkpointer(cls) -> Checkpointer:
        return RedisSaver.from_conn_string(settings.redis.url)

    def compile(self) -> CompiledStateGraph:
        workflow = StateGraph(MessagesState)

        workflow.add_node("supervisor", self.supervisor_node)
        workflow.add_node("researcher", self.researcher_node)
        workflow.add_node("pokemon_expert", self.pokemon_expert_node)

        workflow.add_edge(START, "supervisor")

        return workflow.compile()
