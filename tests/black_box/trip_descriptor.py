import os, sys
from datetime import date

current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_script_dir, '..\\..')
sys.path.insert(0, project_root)

from datastructures.TripDescriptor import TripDescriptor
from datastructures.TripDescriptor import Place
from tools.filler import fill_trip_description

t = TripDescriptor()

print("\n\n------------------------------------------------")
print("Description of an empty trip\n")
ret = t.get_description()
if ret == "No trip information available.": print("Correct")
print(f"\n{ret}")



print("\n\n------------------------------------------------")
print("Filling with wrong places\n")
ret = t.fill(places = ["Udine", ""])
if ret == "Error in TripDescriptor.__set_places()\nFor the following places were not found: , ": print("Correct") 
else: print("Failed")
print(f"\n{ret}")

print("\n\n------------------------------------------------")
print("Filling with valid places\n")
ret = t.fill(places = ["Udine", "Tavagnacco"])
if ret == None: print("Correct") 
else: print("Failed")
print(f"\n{ret}")



print("\n\n------------------------------------------------")
print("Filling with invalid bike_type\n")
ret = t.fill(bike_type = "city")
if ret == "Error in TripDescriptor.__set_bike_type()\nThe given bike_type must be one of BikeType type\ncity was provided": print("Correct")
else: print("Failed")
print(f"\n{ret}")

print("\n\n------------------------------------------------")
print("Filling with valid bike_type\n")
ret = t.fill(bike_type = "gravel")
if ret == None: print("Correct")
else: print("Failed")
print(f"\n{ret}")



day = "2003-10-02"
d = date.fromisoformat(day)

print("\n\n------------------------------------------------")
print("Description of an essentially filled trip\n")
print(t.get_description())

print("\n\n------------------------------------------------")
print("Generate the candidate raw routes\n")
tracks = t.get_candidate_raw_routes()
if tracks:
    for idx, track in enumerate(tracks): 
        print(f"track n. : {idx}\n{track[:3]}")

print("\n\n------------------------------------------------")
print("Select the track\n")
track_n = 2
t.fill(selected_raw_route = track_n)
