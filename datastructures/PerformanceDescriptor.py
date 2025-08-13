from pydantic import BaseModel


class PerformanceDescriptor(BaseModel):
    """Description of the user cycling performance"""
    kilometer_per_day: int = 0 #Field(default=0, description="the maximum amout of kilometers the user is able to ride in a day")
    positive_height_difference_per_day: int = 0 #Field(default=0, description="the maximum difference of height in meter the user is ablo do in a day")

    def get_kilometer_per_day(self) -> int:
        return self.kilometer_per_day
    
    def get_positive_height_difference_per_day(self) -> int:
        return self.positive_height_difference_per_day

    def get_class_description(self) -> str:
        """Get a string description of the class"""
        return f"""## PerformanceDescriptor:
- kilometer_per_day: int = 0
    - the maximum amount of kilometers the user is able to ride in a day
- positive_height_difference_per_day: int = 0
    - the maximum difference of height in meter the user is able to do in a day
"""

    def get_description(self) -> str:
        description = ""
        
        if self.kilometer_per_day > 0:
            description += f"Kilometers per day: {self.kilometer_per_day}\n"
        if self.positive_height_difference_per_day > 0:
            description += f"Difference in height per day: {self.positive_height_difference_per_day}\n"
            
        if description == "":
            return "No performance set."

        return description
    
    def __set_kilometer_per_day(self, kilometer_per_day: int) -> None | str:
        self.kilometer_per_day = kilometer_per_day

    def __set_positive_height_difference_per_day(self, positive_height_difference_per_day: int) -> None | str:
        self.positive_height_difference_per_day = positive_height_difference_per_day

    def fill(self, kilometer_per_day: None | int = None, positive_height_difference_per_day: None | int = None) -> None | str:
        """Fill the performance descriptor with the given things
        Args:
            - kilometer_per_day (int) | None : the maximum amount of kilometers the user is able to ride in a day
            - positive_height_difference_per_day (int) | None : the maximum difference of height in meter the user is able to do in a day

        Returns:
            - None: if nothing went wrong
            - str: if something went wrong, it will return a string with the error message

        Examples:
            ```python
            performance = PerformanceDescriptor()
            performance.fill(kilometer_per_day=100, positive_height_difference_per_day=500)
            ```
        """
        if kilometer_per_day != None:
            res = self.__set_kilometer_per_day(kilometer_per_day)
            if res != None:
                return res
        
        if positive_height_difference_per_day != None:
            res = self.__set_positive_height_difference_per_day(positive_height_difference_per_day)
            if res != None:
                return res
