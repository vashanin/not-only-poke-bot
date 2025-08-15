from typing import Literal

from langchain_openai import ChatOpenAI
from langfuse import get_client
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from langgraph.types import Command

from core.settings import settings

from .tools import ask_pokemon_expert, ask_researcher, get_pokemon_data, tavily_tool
from .utils import get_next_node


class Graph:
    llm = ChatOpenAI(
        model=settings.openai.model,
        reasoning_effort=settings.openai.reasoning_effort,
    )
    json_llm = llm.bind(response_format={"type": "json_object"})
    langfuse = get_client()

    def __init__(self, answer_key: str, answer_example: str):
        self.supervisor_agent = create_react_agent(
            self.json_llm,
            tools=[ask_researcher],
            prompt=self.langfuse.get_prompt("supervisor").compile(),
        )

        self.research_agent = create_react_agent(
            self.json_llm,
            tools=[get_pokemon_data, ask_pokemon_expert, tavily_tool],
            prompt=self.langfuse.get_prompt("researcher").compile(),
        )

        self.pokemon_expert_agent = create_react_agent(
            self.json_llm,
            tools=[],
            prompt=self.langfuse.get_prompt("pokemon-expert").compile(
                answer_key=answer_key, answer_example=answer_example
            ),
        )

    async def supervisor_node(self, state: MessagesState) -> Command[Literal["researcher", END]]:
        result = await self.supervisor_agent.ainvoke(state)
        goto = get_next_node(result["messages"], default=END)

        return Command(update={"messages": result["messages"]}, goto=goto)

    async def researcher_node(self, state: MessagesState) -> Command[Literal["pokemon_expert", END]]:
        result = await self.research_agent.ainvoke(state)
        goto = get_next_node(result["messages"], default=END)

        return Command(update={"messages": result["messages"]}, goto=goto)

    async def pokemon_expert_node(self, state: MessagesState) -> Command[Literal[END]]:
        result = await self.pokemon_expert_agent.ainvoke(state)

        return Command(update={"messages": result["messages"]})

    def compile(self) -> CompiledStateGraph:
        workflow = StateGraph(MessagesState)

        workflow.add_node("supervisor", self.supervisor_node)
        workflow.add_node("researcher", self.researcher_node)
        workflow.add_node("pokemon_expert", self.pokemon_expert_node)

        workflow.add_edge(START, "supervisor")

        return workflow.compile()
