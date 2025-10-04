from dotenv import load_dotenv
import logfire, yaml
from pydantic_ai import Agent, Tool
from datastructures.FinalResults import Itinerary
from tools.route_planner_tools import approximate_itinerary_length

load_dotenv()

with open("./crew/crew.yaml", "r") as crew_conf:
    try:
        agent_info = yaml.safe_load(crew_conf).get("route_planner")
    except yaml.YAMLError as e:
        logfire.log("error", f"Error loading crew.yaml: {e}")
        raise e

with open(f"./crew/{agent_info.get("prompt_file")}", "r", encoding="utf-8") as prom:
    try:
        prompt = prom.read()
    except Exception as e:
        logfire.log("error", f"Error loading ./crew/{agent_info.get("prompt_file")}: {e}")
        raise e



"""
=== Route Planner ===
Goal: Plan the trip itinerary
    The itinerary will be a collection of places that have to be visited during the trip.
    example: ["Tarvisio", "Gemona", "San Daniele del Friuli", "Udine", "Palmanova", "Aquileia", "Grado"]
"""
logfire.log("info", "Creation of: \troute_planner_agent")
route_planner = Agent[None, str | Itinerary](
    model = agent_info.get("llm"),
    system_prompt = prompt,
    output_type = str | Itinerary,
    tools = [
        Tool(approximate_itinerary_length, docstring_format="google"),
    ]
)

"""
@route_planner.system_prompt
def add_Itinerary_shema() -> str:
    return f"Itinerary class json schema: {Itinerary.model_json_schema()}"
"""