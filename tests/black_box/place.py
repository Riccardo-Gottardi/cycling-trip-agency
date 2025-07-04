import os, sys

current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_script_dir, '..\\..')
sys.path.insert(0, project_root)

from datastructures.TripDescriptor import Place

u = Place(name="Udine")
print(f"name: {u.get_name()}\ncoordinates: {u.get_coordinates()}")

t = Place(name="Pizzeria trombone, Udine")
print(f"name: {t.get_name()}\ncoordinates: {t.get_coordinates()}")

c = Place(name="")
print(f"name: {c.get_name()}\ncoordinates: {c.get_coordinates()}")
