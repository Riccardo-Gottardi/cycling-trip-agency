from dataclasses import dataclass
from datastructures.TripDescriptor import TripDescriptor
from datastructures.CustomerDescriptor import CustomerDescriptor
from datastructures.Recommendation import Recommendation


@dataclass
class MyDeps:
    trip: TripDescriptor
    user: CustomerDescriptor
    # recommendation: Recommendation