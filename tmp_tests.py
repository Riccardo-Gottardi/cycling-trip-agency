from datastructures.Place import Place
"""Check the exception handling in Place class
try:
    l = Place(name="louis, pordenone")
    print(l)
except:
    print("exception catched")
"""

udine = Place(name="Udine")
pordenone = Place(name="Pordenone")
sacile = Place(name="Sacile")

"""Check the correcctness of the fcc_distance
from datastructures. import 
dist1 = fcc_distance(pordenone.get_coordinates(), udine.get_coordinates())
dist2 = fcc_distance(pordenone.get_coordinates(), sacile.get_coordinates())
print(dist1, dist2, sep="\n")
"""

import requests

lon_lat_string = f"{udine.get_coordinates()[1]},{udine.get_coordinates()[0]}|{pordenone.get_coordinates()[1]},{pordenone.get_coordinates()[0]}|{sacile.get_coordinates()[1]},{sacile.get_coordinates()[0]}"
url = f"http://localhost:17777/brouter?lonlats={lon_lat_string}&profile=gravel&alternativeidx=0&format=gpx"
response = requests.get(url)
response.raise_for_status()
for l in response.text.split("\n")[:15]:
    print(l)