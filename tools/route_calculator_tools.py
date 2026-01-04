from pydantic_ai import RunContext
from datastructures.MyDeps import MyDeps
from utility.DistanceCalculator import DistanceCalculator


def generate_gpx_route(ctx: RunContext[MyDeps]):
    """Generates a GPX route based on the trip description in deps.
    Example:
        ```python
        generate_gpx_route()
        ```
    """
    try:
        ctx.deps.trip.generate_gpx_route()
    except Exception as e:
        return str(e)