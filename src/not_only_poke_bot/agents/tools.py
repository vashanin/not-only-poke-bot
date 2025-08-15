import json

import aiohttp
from langchain_core.tools import tool
from langchain_tavily import TavilySearch

tool_to_node_mapping = {
    "ask_researcher": "researcher",
    "ask_pokemon_expert": "pokemon_expert",
}


@tool()
async def ask_researcher():
    """
    The Researcher's goal is to retrieve information from external sources to help answer user queries.
    You must use it for sure when you need to get information about Pokémon stats and abilities, or when you need to answer questions about current events.
    """
    # We return a tiny acknowledgement so the LLM sees tool output,
    # but routing is handled by the graph (see route_supervisor()).
    return "ask_researcher"


@tool()
async def ask_pokemon_expert():
    """
    The Pokémon Expert's goal is to determine the probable winner in a Pokémon battle based on stats and type advantages.
    """
    return "ask_pokemon_expert"


@tool()
async def get_pokemon_data(pokemon_name: str) -> dict:
    """Use Poke API to get data about Pokémon abilities, stats and type advantages."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=15) as resp:
                if resp.status != 200:
                    response = {
                        "type": "error",
                        "info": f"PokeAPI request failed with status {resp.status}. "
                        "Check if the Pokémon name is valid and try again.",
                    }
                else:
                    response = await resp.json()

    except aiohttp.ClientError as e:
        response = {
            "type": "error",
            "info": f"HTTP error from PokeAPI: {e}. Check if the Pokémon name is valid and try again.",
        }
    except json.JSONDecodeError:
        response = {"type": "error", "info": "Failed to parse PokeAPI response. Please try again."}

    return response


tavily_tool = TavilySearch(max_results=5)
