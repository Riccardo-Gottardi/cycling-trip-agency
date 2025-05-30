from pydantic_ai import RunContext
from datastructures.descriptors import TripDescriptor, PerformanceDescriptor, PreferencesDescriptor
from datastructures.dependencies import MyDeps


def ask_to_the_user(question: str) -> str:
    """A tool to ask question to the user and get their answare
    Args:
        question (str): The question to ask the user
    Returns:
        str: The user's answare to the question
    Exaples:
        ```python
        ask_to_the_user("Hi, can you tell me about the trip you are planning ?")
        ask_to_the_user("Perfect, are there some other informations you what to give me ?")
        ```
    """
    assert isinstance(question, str), "In ask_to_the_user\nInput to ask_to_the_user must be a string"
    user_response = input(f"{question}\n")
    return user_response