from pydantic import BaseModel

class Itinerary(BaseModel):
    stages: list[str]

class GPXData(BaseModel):
    gpx: str

class MessageToCustomer(BaseModel):
    message: str