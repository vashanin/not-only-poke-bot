import json

from langfuse.langchain import CallbackHandler

from .graph import Graph


class Controller:
    def __init__(self, answer_key: str, answer_example: str):
        self.graph = Graph(answer_key=answer_key, answer_example=answer_example).compile()
        self.langfuse_handler = CallbackHandler()

    async def chat(self, human_message: str) -> dict:
        result = await self.graph.ainvoke(
            {
                "messages": [("user", human_message)],
            },
            # Maximum number of steps to take in the graph
            config={"callbacks": [self.langfuse_handler]},
        )

        response = json.loads(result["messages"][-1].content)

        return response

    async def battle(self, pokemon1: str, pokemon2: str):
        return await self.chat(f"Who would win in a battle between {pokemon1} and {pokemon2}?")
