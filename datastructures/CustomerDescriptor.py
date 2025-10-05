from pydantic import BaseModel
from datastructures.PerformanceDescriptor import PerformanceDescriptor

class CustomerDescriptor(BaseModel):
    """Description of the user
    Attributes:
        performance (PerformanceDescriptor): measure of the user cycling performance of the user

    Examples:
        ```python
        user = CustomerDescriptor()
        user.set_performance(
            kilometre_per_day=100,
            elevatoin_gain_per_day=500
        )
        performance = user.get_performance()
        ```
    """
    performance: PerformanceDescriptor = PerformanceDescriptor() 

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # This is where you would typically load the user data from a persistence system
        # Check if the user exists in the persistence system
        #   If yes, load his/her performance and pois_preferences
        #   If no, do nothing

    def get_performance(self) -> PerformanceDescriptor:
        """Get the performance descriptor of the user"""
        return self.performance
    
    def get_class_description(self) -> str:
        """Get a string description of the class that represent the user"""
        return f"""# CustomerDescriptor:
- performance: PerformanceDescriptor
{self.performance.get_class_description()}
"""

    def get_description(self) -> str:
        """Get a string description of the user"""
        return f"""\nUser performance: 
{self.performance.get_description()}
"""

    def set_performance(self, kilometre_per_day: int | None = None, elevatoin_gain_per_day: int | None = None):
        try:
            self.performance.fill(
                kilometre_per_day=kilometre_per_day,
                elevatoin_gain_per_day=elevatoin_gain_per_day
            )
        except Exception as e:
            return e