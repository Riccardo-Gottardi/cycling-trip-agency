import logfire
from pydantic_ai import Agent
from datastructures.descriptors import TripDescriptor, UserDescription
from datastructures.dependencies import MyDeps
from crew.director import director


logfire.configure()
logfire.instrument_pydantic_ai()
Agent.instrument_all()


def run_director():
    """Main execution function for the director agent"""
    deps = MyDeps(TripDescriptor(), UserDescription())
    director.run_sync(deps=deps)


if __name__ == "__main__":
    run_director()