def ask_to_the_user(question: str) -> str:
    """Ask a question to the user and return the answer.
    Args:
        question (str): The question to ask the user.
    Returns:
        str: The user's answer.
    Examples:
        ```python
        answer = ask_to_the_user("What is your favorite color?")
        ```
    """
    return input(question)


def recommendation_agent() -> str:
    """A tool to add point of intereset to the route.
    Returns:
        - string containing output of the agent
    Examples:
        ```python
        recommender_agent()
        ```
    """
    return "This is a placeholder for the route recommendation logic."