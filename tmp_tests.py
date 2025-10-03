from datastructures.Place import Place

try:
    l = Place(name="louis, pordenone")
    print(l)
except:
    print("exception catched")


from datastructures.DistanceCalculation import DistanceCalculation

udine = Place(name="Udine")
pordenone = Place(name="Pordenone")
sacile = Place(name="Sacile")

dist1 = DistanceCalculation.fcc_distance(pordenone.get_coordinates(), udine.get_coordinates())
dist2 = DistanceCalculation.fcc_distance(pordenone.get_coordinates(), sacile.get_coordinates())
print(dist1, dist2, sep="\n")