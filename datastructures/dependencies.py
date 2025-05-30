from dataclasses import dataclass
from datastructures.descriptors import TripDescriptor, UserDescription


@dataclass
class MyDeps:
    trip: TripDescriptor
    user: UserDescription