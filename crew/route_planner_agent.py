import yaml, logfire
from dotenv import load_dotenv

from pydantic_ai import Agent, RunContext, Tool

from datastructures.dependencies import MyDeps

from tools.route_planner_tools import say_to_the_user, get_trip_information, get_user_information, plan_the_candidate_routes, plan_the_route_steps, get_route_recommendation
from tools.filler import fill_trip_description, fill_user_preferences, fill_user_performance, fill_user_additional_note


load_dotenv()


with open("./crew/crew.yaml", "r") as file:
    try:
        crew_info = yaml.safe_load(file)
    except yaml.YAMLError as e:
        logfire.log("error", f"Error loading crew.yaml: {e}")
        raise e


logfire.log("info", "Creation of: \troute_planner_agent")
route_planner = Agent(
    model=crew_info["route_planner"]["llm"],
    deps_type=MyDeps,
    system_prompt=crew_info["route_planner"]["system_prompt"],
    tools=[
        Tool(say_to_the_user, takes_ctx=False, docstring_format="google", max_retries=3),
        Tool(fill_trip_description, takes_ctx=True, docstring_format="google", max_retries=3),
        Tool(fill_user_preferences, takes_ctx=True, docstring_format="google", max_retries=3),
        Tool(fill_user_performance, takes_ctx=True, docstring_format="google", max_retries=3),
        Tool(fill_user_additional_note, takes_ctx=True, docstring_format="google", max_retries=3),
        Tool(get_trip_information, takes_ctx=True, docstring_format="google", max_retries=3),
        Tool(get_user_information, takes_ctx=True, docstring_format="google", max_retries=3),
        Tool(plan_the_candidate_routes, takes_ctx=True, docstring_format="google", max_retries=3),
        Tool(plan_the_route_steps, takes_ctx=True, docstring_format="google", max_retries=3),
        # TODO implement it's
        Tool(get_route_recommendation, takes_ctx=False, docstring_format="google", max_retries=3)
    ]
)

# ========== Add additional context to LLM ===========
@route_planner.system_prompt()
def add_descriptors_structure_to_system_prompt(ctx: RunContext[MyDeps]) -> str:
    return f"""The trip is described by the following class:\n{str(ctx.deps.trip.get_class_description())}
The user is described by the following class:\n{str(ctx.deps.user.get_class_description())}
"""


@route_planner.system_prompt(dynamic=True)
def add_current_descriptions_to_system_prompt(ctx: RunContext[MyDeps]) -> str:
    return f"""Current trip informations are: {str(ctx.deps.trip.get_description())}
Current user informations are: {str(ctx.deps.user.get_description())}
"""
