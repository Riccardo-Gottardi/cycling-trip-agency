import logfire
from dotenv import load_dotenv

from pydantic_ai import Agent

from datastructures.TripDescriptor import TripDescriptor
from datastructures.UserDescriptor import UserDescriptor
from datastructures.Recommendation import Recommendation
from datastructures.dependencies import MyDeps

load_dotenv()

logfire.configure()
logfire.instrument_pydantic_ai()
Agent.instrument_all()

from crew.route_planner_agent import route_planner


def run_cycling_trip_agency():
    """Main execution function for the director agent"""
    deps = MyDeps(TripDescriptor(), UserDescriptor(), Recommendation())
    route_planner.run_sync(deps=deps)


if __name__ == "__main__":
    run_cycling_trip_agency()