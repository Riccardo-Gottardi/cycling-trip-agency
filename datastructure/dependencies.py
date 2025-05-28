from dataclasses import dataclass
from datastructure.descriptors import TripDescriptor, PerformanceDescriptor


@dataclass
class MyDeps:
    trip: TripDescriptor
    performance: PerformanceDescriptor