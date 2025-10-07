from pydantic import BaseModel

class Itinerary(BaseModel):
    stages: list[str]

class GPXDataIsReady(BaseModel):
    message: str

class MessageToCustomer(BaseModel):
    message: str

class Reasoning(BaseModel):
    thought: str
    next_actions_planning: str