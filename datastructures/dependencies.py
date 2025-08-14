from dataclasses import dataclass
from datastructures.TripDescriptor import TripDescriptor
from datastructures.UserDescriptor import UserDescriptor
from datastructures.Recommendation import Recommendation


@dataclass
class MyDeps:
    trip: TripDescriptor
    user: UserDescriptor
    recommendation: Recommendation