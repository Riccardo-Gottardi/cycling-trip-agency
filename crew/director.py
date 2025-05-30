import logfire, yaml
from pydantic_ai import Agent, Tool, RunContext
from dotenv import load_dotenv
from datastructures.dependencies import MyDeps
from crew.informations_collector import informations_collector


load_dotenv()


with open("./crew/crew.yaml", "r") as file:
    try:
        crew_info = yaml.safe_load(file)
    except yaml.YAMLError as e:
        logfire.log("error", f"Error loading crew.yaml: {e}")
        raise


logfire.log("info", "Creating director agent") 
director = Agent(
    model=crew_info["director"]["llm"],
    deps_type=MyDeps,
    system_prompt=crew_info["director"]["system_prompt"],
)


# ========== Add context to LLM ===========
@director.system_prompt
def add_context_to_system_prompt(ctx: RunContext[MyDeps]) -> str:
    return f"""The trip is described by the following class:
        {str(ctx.deps.trip.model_json_schema())}
        User's performance is described by the following class:
        {str(ctx.deps.performance.model_json_schema())}
        User's preferences is described by the following class:
        {str(ctx.deps.preferences.model_json_schema())}
        """


# =============== Agents wrappers ===============
# TODO try to understand if would it be better to pass what to collect as part of the system prompt
@director.tool(docstring_format="google", retries=3)
def retrieve_informations_from_user(ctx: RunContext[MyDeps], context: str, what_to_collect: str) -> str:
    """A tool to collect informations from the user
    Args:
        - context (str): explain the context in which the informations are required, and why they are needed. 
        - what_to_collect (str): contain the informations to collect, each one followed by a short description.
    Returns:
        - string containing output of the agent
    Usage:
        - retrieve_informations_from_user("Collecting informations help the user plan a trip", "bicycle_profile: type of bike used, either ROAD, GRAVEL or MTB, number_of_days: the number of days for the trip")
        - retrieve_informations_from_user("Understanding the performance of the user", "kilometer_per_day: the amount of kilomenter the user can achieve in a single day")
        - retrieve_informations_from_user("")
    """
    result = informations_collector.run_sync(
        f"""The information you have to collect are:
        {what_to_collect}
        The context in which they are required is:
        {context}
        The known informations so far are:
        {ctx.deps.trip}
        {ctx.deps.performance}
        """, 
        deps=ctx.deps)

    return result.output 