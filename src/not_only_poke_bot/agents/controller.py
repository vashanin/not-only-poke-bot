import json

from langfuse.langchain import CallbackHandler

from .graph import Graph


class Controller:
    def __init__(self, answer_key: str, answer_example: str):
        self.graph = Graph(answer_key=answer_key, answer_example=answer_example).compile()
        self.langfuse_handler = CallbackHandler()

    def chat(self, human_message: str) -> dict:
        result = self.graph.invoke(
            {
                "messages": [("user", human_message)],
            },
            # Maximum number of steps to take in the graph
            config={"callbacks": [self.langfuse_handler]},
        )

        response = json.loads(result['messages'][-1].content)

        return response

    def battle(self, pokemon1: str, pokemon2: str):
        return self.chat(f"Who would win in a battle between {pokemon1} and {pokemon2}?")
