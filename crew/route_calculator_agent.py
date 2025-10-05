import yaml, logfire
from dotenv import load_dotenv

from pydantic_ai import Agent, RunContext, Tool

from datastructures.MyDeps import MyDeps
from datastructures.agents_results import GPXData, MessageToCustomer

from tools.route_calculator_tools import generate_gpx_route, approximate_segment_length
from tools.filler import fill_trip_description, fill_pois_preferences, fill_user_performance, fill_user_additional_note


load_dotenv()


with open("./crew/crew.yaml", "r") as crew_conf:
    try:
        agent_info = yaml.safe_load(crew_conf).get("route_calculator")
    except yaml.YAMLError as e:
        logfire.log("error", f"Error loading crew.yaml: {e}")
        raise e

with open(f"./crew/{agent_info.get("prompt_file")}", "r", encoding="utf-8") as prom:
    try:
        prompt = prom.read()
    except Exception as e:
        logfire.log("error", f"Error loading ./crew/{agent_info.get("prompt_file")}: {e}")
        raise e


logfire.log("info", "Creation of: \troute_calculator_agent")
route_calculator = Agent(
    model = agent_info.get("llm"),
    deps_type = MyDeps,
    output_type = MessageToCustomer | GPXData,
    system_prompt = prompt, # pyright: ignore[reportPossiblyUnboundVariable]
    tools = [
        Tool(fill_trip_description, takes_ctx=True, docstring_format="google", max_retries=3),
        Tool(fill_user_performance, takes_ctx=True, docstring_format="google", max_retries=3),
        Tool(approximate_segment_length, docstring_format="google", max_retries=3),
        Tool(generate_gpx_route, takes_ctx=True, docstring_format="google", max_retries=3),
    ]
)

# ========== Add additional context to LLM ===========
@route_calculator.system_prompt()
def add_descriptors_structure_to_system_prompt(ctx: RunContext[MyDeps]) -> str:
    return f"""The trip is described by the following class:\n{str(ctx.deps.trip.get_class_description())}
The user is described by the following class:\n{str(ctx.deps.user.get_class_description())}
"""

@route_calculator.system_prompt(dynamic=True)
def add_current_descriptions_to_system_prompt(ctx: RunContext[MyDeps]) -> str:
    return f"""Current trip informations are: {str(ctx.deps.trip.get_description())}
Current user informations are: {str(ctx.deps.user.get_description())}
"""