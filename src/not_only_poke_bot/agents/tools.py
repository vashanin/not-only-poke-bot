import requests
from langchain_tavily import TavilySearch

from langchain_core.tools import tool


tool_to_node_mapping = {
    "ask_researcher": "researcher",
    "ask_pokemon_expert": "pokemon_expert",
}


@tool()
def ask_researcher():
    """
    The Researcher's goal is to retrieve information from external sources to help answer user queries.
    You must use it for sure when you need to get information about Pokémon stats and abilities, or when you need to answer questions about current events.
    """
    # We return a tiny acknowledgement so the LLM sees tool output,
    # but routing is handled by the graph (see route_supervisor()).
    return "ask_researcher"


@tool()
def ask_pokemon_expert():
    """
    The Pokémon Expert's goal is to determine the probable winner in a Pokémon battle based on stats and type advantages.
    """
    return "ask_pokemon_expert"


@tool()
def get_pokemon_data(pokemon_name: str) -> dict:
    """Use Poke API to get data about Pokémon abilities, stats and type advantages."""

    try:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}").json()
    except requests.JSONDecodeError:
        response = {
            "type": "error",
            "info": "Failed to get Pokémon data from external sources. "
                    "Check if the Pokémon name is valid and try again."
        }

    return response


tavily_tool = TavilySearch(max_results=5)
