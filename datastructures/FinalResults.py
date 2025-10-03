from pydantic import BaseModel

class PlannerFinalResult(BaseModel):
    itinerary: list[str]

    def set_itinerary(self, itin: list[str]):
        self.itinerary = itin