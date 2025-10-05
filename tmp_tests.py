from datastructures.Place import Place
"""Check the exception handling in Place class
try:
    l = Place(name="louis, pordenone, italy")
    print(l)
except:
    print("exception catched")
"""

"""
udine = Place(name="Udine, Italy")
pulfero = Place(name="Pulfero, Italy")
stregna = Place(name="Stregna, Italy")
cividale = Place(name="Cividale del Friuli, Italy")
tarvisio = Place(name="Tarvisio, Italy")
san_daniele = Place(name="San Daniele del Friuli, Italy")
maniago = Place(name="Maniago, Italy")
aviano = Place(name="Aviano, Italy")
vittorio_veneto = Place(name="Vittorio Veneto, Italy")
sacile = Place(name="Sacile, Italy")
pordenone = Place(name="Pordenone, Italy")
aquileia = Place(name="Aquileia, Italy")
lignano = Place(name="Lignano Sabbiadoro, Italy")

itinerary = [maniago, aviano, vittorio_veneto, sacile, pordenone, aquileia]
"""

"""Check the correcctness of the fcc_distance
from utility.distance_calculation import fcc_distance
dist1 = fcc_distance(pordenone.get_coordinates(), udine.get_coordinates())
dist2 = fcc_distance(pordenone.get_coordinates(), sacile.get_coordinates())
print(dist1, dist2, sep="\n")
"""

"""check the brouter response in gpx format
import requests
lon_lat_string = f"{udine.get_coordinates()[1]},{udine.get_coordinates()[0]}|{pordenone.get_coordinates()[1]},{pordenone.get_coordinates()[0]}|{sacile.get_coordinates()[1]},{sacile.get_coordinates()[0]}"
url = f"http://localhost:17777/brouter?lonlats={lon_lat_string}&profile=gravel&alternativeidx=0&format=gpx"
response = requests.get(url)
response.raise_for_status()
for l in response.text.split("\n")[:15]:
    print(l)
"""

from tools.route_calculator_tools import approximate_segment_length

segments = [["Pordenone, Italy", "Rivignano Teor, Italy"], ["Rivignano Teor, Italy", "Aquileia, Italy"], ["Pordenone, Italy", "Varmo, Italy"], ["Varmo, Italy", "Aquileia, Italy"], ["Pordenone, Italy", "Morsano al Tagliamento, Italy"], ["Morsano al Tagliamento, Italy", "Aquileia, Italy"]]

for seg in segments:
    print(f"{" -> ".join([p for p in seg])}, length: {approximate_segment_length(seg)} m")
