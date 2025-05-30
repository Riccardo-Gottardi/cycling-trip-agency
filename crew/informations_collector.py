import logfire, yaml
from dotenv import load_dotenv
from pydantic_ai import Agent, Tool
from datastructures.dependencies import MyDeps
from tools.information_gathering_tools import ask_to_the_user
from tools.filler import fill_trip_description, fill_user_description


load_dotenv()


with open("./crew/crew.yaml", "r") as file:
    try:
        crew_info = yaml.safe_load(file)
    except yaml.YAMLError as e:
        logfire.log("error", f"Error loading crew.yaml: {e}")
        raise


logfire.log("info", "Creating informations_collector agent")
informations_collector = Agent(
    model=crew_info["informations_collector"]["llm"],
    deps_type=MyDeps,
    system_prompt=crew_info["informations_collector"]["system_prompt"],
    tools=[
        Tool(ask_to_the_user, takes_ctx=False, docstring_format="google", max_retries=3),
        Tool(fill_trip_description, takes_ctx=True, docstring_format="google", max_retries=3),
        Tool(fill_user_description, takes_ctx=True, docstring_format="google", max_retries=3)
    ]
)