from pydantic import BaseModel
import requests
import gpxpy
import gpxpy.gpx
from datastructures.Place import Place


class TripDescriptor(BaseModel):
    """Description of a bicycle trip
    Attributes:
        bike_type (str | None): either road, gravel, mtb. Is the type of bike
        itinerary (list[Place] | None): list of places, the first is the starting point, the last is the ending point
        segmented_itinerary (list[list[Place]] | None): list of segments of the itinerary
        duration (int | None): the number of days the trip will last
        gpx_segments (list[str] | None): list of gpx formatted strings, each one representing a segment of the trip
        gpx_route (str | None): a gpx formatted string representing the whole trip
    Examples:
        ```python
        trip = TripDescriptor()
        trip.fill(
            bike_type = "gravel",
            duration = 4,
        )
        trip.fill(itinerary = ["Udine", "Palmanova", "Trieste"])
        ...
        trip.generate_gpx_route()
        gpx_route = trip.get_gpx_route()
        ```
    """
    bike_type: str | None = None
    itinerary: list[Place] | None = None
    segmented_itinerary: list[list[Place]] | None = None
    duration: int | None = None
    gpx_segments: list[str] | None= None
    gpx_route: str | None = None 
    
    def get_bike_type(self) -> str | None:
        return self.bike_type
    
    def get_itinerary(self) -> list[Place] | None:
        return self.itinerary
    
    def get_segmented_itinerary(self) -> list[list[Place]] | None:
        return self.segmented_itinerary

    def get_duration(self) -> int | None:
        return self.duration
    
    def get_gpx_segments(self) -> list[str] | None:
        return self.gpx_segments

    def get_gpx_route(self) -> str | None:
        return self.gpx_route
    
    @classmethod
    def get_class_description(cls) -> str:
        """Get a description of the class that represent the trip"""
        return """# TripDescriptor:
- bike_type: str | None = None
    - describe the type of bike used for the trip, either road, gravel of mtb
- itinerary: list[Place] | None = None
    - collect the different places that trip have to go through
- segmented_itinerary: list[list[Place]] | None = None
    - collect the different segments of the itinerary, each segment is a list of places
- duration: int | None = None
    - the maximum number of days the user wants to spend on the trip
- gpx_segments: list[str] = []
    - the gpx segments of the trip, each segment is a gpx track in string format
- gpx_route: str = ""
    - the gpx route is the gpx track that represent the whole trip in string format

"""

    def get_description(self) -> str:
        """Get a description of the trip"""
        description = ""
        
        if self.bike_type is not None:
            description += f"\nBicycle type:\n{self.bike_type}.\n"

        if self.duration is not None:
            description += f"\nDuration:\n{self.duration}.\n"

        if self.itinerary is not None and len(self.itinerary) > 0: 
            description += f"\nItinerary:\n"
            description += f"{self.itinerary[0].get_name()}"
            for p in self.itinerary[1:]:
                description += f" -> {p.get_name()}"

        if self.segmented_itinerary is not None and len(self.segmented_itinerary) > 0:
            description += f"\nSegmented itinerary:\n"
            for segment in self.segmented_itinerary:
                description += f"- Segment: "
                description += f"{segment[0].get_name()}"
                for place in segment[1:]:
                    description += f" -> {place.get_name()}"
                description += "\n"

        if self.gpx_segments is not None and len(self.gpx_segments) > 0:
            description += f"\nGPX segments:\n"
            for i, segment in enumerate(self.gpx_segments):
                description += f"- Segment {i+1}: {segment}"

        if self.gpx_route is not None:
            description += f"\nGPX route:\n{self.gpx_route}.\n"

        if description == "":
            description += "No trip information available."
        
        return description
    
    def __set_bike_type(self, bike_type: str):
        if not bike_type in ["road", "gravel", "mtb"]: raise Exception(f"Error in TripDescriptor.__set_bike_type()\nThe given bike_type must be one of BikeType type\n{bike_type} was provided")
        self.bike_type = bike_type

    def __set_itinerary(self, itinerary: list[str]):  
        if not len(itinerary) > 1: raise Exception(f"Error in TripDescriptor.__set_itinerary()\nThe given itinerary must contain at least 2 elements, the starting and ending point of the trip\n{len(itinerary)} were provided")
        self.itinerary = [Place(name=plc) for plc in itinerary]

        not_found = ""
        for place in self.itinerary:
            if place.get_osm_name() == "":
                not_found += f"{place.get_name()}, "
        if not_found != "":
            raise Exception(f"Error in TripDescriptor.__set_itinerary()\nFor the following itinerary were not found: {not_found}")

    def __set_segmented_itinerary(self, segmented_itinerary: list[list[str]]):
        if not len(segmented_itinerary) > 0: raise Exception(f"Error in TripDescriptor.__set_segmented_itinerary()\nThe given segmented_itinerary must contain at least 1 element, the first segment of the trip\n{len(segmented_itinerary)} were provided")

        self.segmented_itinerary = []

        for segment in segmented_itinerary:
            if not len(segment) > 1: raise Exception(f"Error in TripDescriptor.__set_segmented_itinerary()\nEach segment of the segmented_itinerary must contain at least 2 elements, the starting and ending point of the segment\n{len(segment)} were provided")

            self.segmented_itinerary.append([Place(name=plc) for plc in segment])
            not_found = ""
            for place in self.segmented_itinerary[-1]:
                if place.get_osm_name() == "":
                    not_found += f"{place.get_name()}, "
            if not_found != "":
                raise Exception(f"Error in TripDescriptor.__set_segmented_itinerary()\nFor the following segmented_itinerary were not found: {not_found}")

    def __set_duration(self, duration: int):
        if not duration > 0: raise Exception(f"Error in TripDescriptor.__set_duration()\nThe given duration must be greater than 0\n{duration} was provided")
        self.duration = duration

    def fill(self, bike_type: None | str = None, itinerary: None | list[str] = None, segmented_itinerary: None | list[list[str]] = None, duration: None | int = None): 
        """Fill the TripDescriptor with the given info
        Args:
            bike_type (str) | None : is the type to bike, either road, gravel or mtb.
            itinerary (list[str]) | None : list of itinerary, the first is the starting point, the last is the ending point
            segmented_itinerary (list[list[str]]) | None : list of segments of the itinerary
            duration (int) | None : the number of days the trip will last
        Return:
            None: if nothing went wrong
            str: containing an error explanation if something went wrong
        Examples:
            ```python
            trip = TripDescriptor()
            trip.fill(
                bike_type = "gravel",
                duration = 4,
                itinerary = ["Udine", "Palmanova", "Trieste"],
            )
            ...
            trip.fill(dates = ["2023-10-1", "2023-10-5"])
            ```
        """
        if bike_type is not None:
            try:
                self.__set_bike_type(bike_type)
            except Exception as e:
                raise e

        if itinerary is not None:
            try:
                self.__set_itinerary(itinerary) 
            except Exception as e:
                raise e
            
        if segmented_itinerary is not None:
            try:
                self.__set_segmented_itinerary(segmented_itinerary) 
            except Exception as e:
                raise e

        if duration is not None:
            try:
                self.__set_duration(duration) 
            except Exception as e:
                raise e

    def __generate_gpx_segments(self):
        bike_profile = self.bike_type
        if self.bike_type == "road":
            bike_profile = "fastbike"

        self.gpx_segments = []        

        if self.segmented_itinerary is not None:
            for segment in self.segmented_itinerary:
                locations_coordinates = [place.get_coordinates() for place in segment] 
                lon_lat_string = f"{locations_coordinates[0][1]},{locations_coordinates[0][0]}"
                for coord in locations_coordinates:
                    lon_lat_string += f"|{coord[1]},{coord[0]}"

                url = f"http://localhost:17777/brouter?lonlats={lon_lat_string}&profile={bike_profile}&alternativeidx=0&format=gpx"
                response = requests.get(url)
                response.raise_for_status()

                self.gpx_segments.append(response.text)

    def __merge_gpx_segments(self):
        merged = gpxpy.gpx.GPX()
        combined_track = gpxpy.gpx.GPXTrack(name="Combined Segments")

        if self.gpx_segments is not None:
            for segment in self.gpx_segments:
                gpx_segment = gpxpy.parse(segment)

                for seg in gpx_segment.tracks[0].segments:
                    combined_track.segments.append(seg)

        merged.tracks.append(combined_track)
        return merged.to_xml()

    def generate_gpx_route(self):
        """Get a route that goes through the itinerary provided"""
        self.__generate_gpx_segments()
        self.gpx_route = str(self.__merge_gpx_segments())
