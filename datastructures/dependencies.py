from dataclasses import dataclass
from datastructures.TripDescriptor import TripDescriptor
from datastructures.UserDescriptor import UserDescriptor


@dataclass
class MyDeps:
    trip: TripDescriptor
    user: UserDescriptor