from pydantic import BaseModel
from datastructures.PerformanceDescriptor import PerformanceDescriptor
from datastructures.POIsDescriptor import POIsDescriptor

class UserDescriptor(BaseModel):
    """Description of the user
    Attributes:
        performance (PerformanceDescriptor): measure of the user cycling performance of the user
        pois_preferences (POIsDescriptor): pois_preferences of the user for the points of interest
        additional_note (str): a useful additional note about the user, that might fell off from performance and pois_preferences

    Examples:
        ```python
        user = UserDescriptor()
        user.set_performance(
            kilometre_per_day=100,
            positive_height_difference_per_day=500
        )
        user.set_pois_preferences(
            natural={"mountains": 5, "lakes": 4},
            water={"rivers": 4, "seas": 5},
            leisure={"hiking": 5, "biking": 4},
        )
        user.set_additional_note("User prefers scenic routes.")
        performance = user.get_performance()
        ```
    """
    performance: PerformanceDescriptor = PerformanceDescriptor() 
    pois_preferences: POIsDescriptor = POIsDescriptor()
    additional_note: str = ""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # This is where you would typically load the user data from a persistence system
        # Check if the user exists in the persistence system
        #   If yes, load his/her performance and pois_preferences
        #   If no, do nothing

    def get_performance(self) -> PerformanceDescriptor:
        """Get the performance descriptor of the user"""
        return self.performance
    
    def get_pois_preferences(self) -> POIsDescriptor:
        """Get the pois_preferences descriptor of the user"""
        return self.pois_preferences

    def get_additional_note(self) -> str:
        """Get the additional notes about the user"""
        return self.additional_note

    def get_class_description(self) -> str:
        """Get a string description of the class that represent the user"""
        return f"""# UserDescriptor:
- performance: PerformanceDescriptor
- pois_preferences: PreferenceDescriptor
- additional_note: str
{self.performance.get_class_description()}
{self.pois_preferences.get_class_description()}
## Additional note
{self.additional_note}
"""

    def get_description(self) -> str:
        """Get a string description of the user"""
        return f"User performance: {self.performance.get_description()}, User pois_preferences: {self.pois_preferences.get_description()}, Additional note: {self.additional_note}"

    def set_performance(self, kilometre_per_day: int | None = None, positive_height_difference_per_day: int | None = None):
        try:
            self.performance.fill(
                kilometre_per_day=kilometre_per_day,
                positive_height_difference_per_day=positive_height_difference_per_day
            )
        except Exception as e:
            return e

    def set_pois_preferences(self, amenity: dict | None = None, tourism: dict | None = None, historic: dict | None = None, building: dict | None = None, natural: dict | None = None, water: dict | None = None, leisure: dict | None = None, man_made: dict | None = None):
        try:
            self.pois_preferences.fill(
                amenity=amenity,
                tourism=tourism,
                historic=historic,
                building=building,
                natural=natural,
                water=water,
                leisure=leisure,
                man_made=man_made
            )
        except Exception as e:
            return e
        
    def set_additional_note(self, additional_note: str):
        self.additional_note = additional_note
