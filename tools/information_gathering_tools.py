from pydantic_ai import RunContext
from datastructure.descriptors import TripDescriptor, PerformanceDescriptor
from datastructure.dependencies import MyDeps


def ask_to_the_user(question: str) -> str:
    """A tool to ask question to the user and get their answare
    Args:
        question (str): The question to ask the user
    Returns:
        str: The user's answare to the question
    Usage:
        ask_to_the_user("Hi, can you tell me about the trip you are planning ?")
        ask_to_the_user("Perfect, are there some other informations you what to give me ?")
    """
    assert isinstance(question, str), "In ask_to_the_user\nInput to ask_to_the_user must be a string"
    user_response = input(f"{question}\n")
    return user_response

def fill_trip_description(ctx: RunContext[MyDeps], gathered_informations: dict):
    """A tool to fill the trip description
    Args:
        gathered_informations (dict): contain the collected informations about the trip. They are structured as a dictionary, with as key the name of the field of the trip descriptor and as values the information/s to put in the trip descriptor.
    Returns:
        Nothing
    Usage:
        fill_trip_descriptor({ride_type: "ONE_WAY", bicycle_profile: "GRAVEL"})
        fill_trip_descriptor({locations: ["Pordenone", "Palmanova", "Trieste"], number_of_days: 4})
    """
    assert isinstance(ctx.deps.trip, TripDescriptor), "In fill_trip_description\nAgent context deps.trip should be of type TripDescriptor"
    ctx.deps.trip.fill(gathered_informations)

def fill_performance_description(ctx: RunContext[MyDeps], gathered_informations: dict):
    """A tool to fill the performance description
    Args:
        gathered_informations (dict): contain the collected informations about the performance of the user. They are structured as a dictionary, with as key the name of the field of the performance descriptor and as values the information/s to put in the performance descriptor.
    Returns:
        Nothing
    Usage:
        fill_performance_description({kilometer_per_day: 100})
        fill_performance_description({difference_in_height_per_day: 100, kilomenter_per_day: 40})
    """
    assert isinstance(ctx.deps.performance, PerformanceDescriptor), "In fill_performance_description\nAgent context deps.performance should be of type PerformanceDescriptor"
    ctx.deps.performance.fill(gathered_informations)