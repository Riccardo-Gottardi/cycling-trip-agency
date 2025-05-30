from pydantic_ai import RunContext
from datastructures.dependencies import MyDeps
from datastructures.descriptors import TripDescriptor, PerformanceDescriptor


def print_trip_descriptor(ctx: RunContext[TripDescriptor]): 
    assert isinstance(ctx.deps, TripDescriptor), "context dependency should be of type TripDescriptor"
    print(ctx.deps.debug_dict())


def get_descriptors(ctx: RunContext[MyDeps]) -> str:
    return str(ctx.deps)