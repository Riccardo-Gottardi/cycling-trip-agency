from dotenv import load_dotenv
from pydantic_ai import Agent, Tool
from tmp_tools import get_intermediate_city_suggestions
from datastructures.Place import Place
from datastructures.DistanceCalculation import DistanceCalculation

load_dotenv()


def approximate_itinerary_distance(places: list[str]):
    tmp = [Place(name=p) for p in places]
    d = 0

    for i in range(1, len(tmp)):
        d += DistanceCalculation.fcc_distance(tmp[i-1].get_coordinates(), tmp[i].get_coordinates())

    return d


with open("tmp_prompt_ag.md", "r", encoding="utf-8") as f:
    prompt_ag = f.read()

ag = Agent(
    model="openai:gpt-4.1-mini",
    system_prompt=prompt_ag,
    tools=[
        Tool(approximate_itinerary_distance)
    ]
)

resp = ag.run_sync("I'm thinking to start from tarvisio and end in Grado, suggest me 3 route, it is a cycling trip.")

print(resp)

