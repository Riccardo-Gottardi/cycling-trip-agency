import requests


def search_pois_nominatim(location_name, poi_type="restaurant"):
    """
    Search for POIs using Nominatim (free geocoding service)
    """
    base_url = "https://nominatim.openstreetmap.org/search"
    
    params = {
        'q': f"{poi_type} in {location_name}",
        'format': 'json',
        'limit': 10,
        'addressdetails': 1
    }
    
    headers = {'User-Agent': 'POI-Search-Script'}  # Required by Nominatim
    
    response = requests.get(base_url, params=params, headers=headers)
    data = response.json()
    
    pois = []
    for item in data:
        poi = {
            'name': item.get('display_name'),
            'lat': float(item.get('lat')),
            'lon': float(item.get('lon')),
            'type': item.get('type'),
            'importance': item.get('importance')
        }
        pois.append(poi)
    
    return pois


cafes_in_london = search_pois_nominatim("Udine, IT", "cafe")
print(f"\nFound {len(cafes_in_london)} cafes in Udine:")
for cafe in cafes_in_london:
    print(f"- {cafe['name']}")


def get_pois_overpass(lat, lon, radius_meters=1000, amenity_type="restaurant"):
    """
    Get POIs using Overpass API (OpenStreetMap data)
    
    Parameters:
    - lat, lon: coordinates of center point
    - radius_meters: search radius in meters
    - amenity_type: type of POI (restaurant, cafe, hospital, etc.)
    """
    
    # Overpass API query
    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
      node["amenity"="{amenity_type}"](around:{radius_meters},{lat},{lon});
      way["amenity"="{amenity_type}"](around:{radius_meters},{lat},{lon});
      relation["amenity"="{amenity_type}"](around:{radius_meters},{lat},{lon});
    );
    out center;
    """
    
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()
    
    pois = []
    for element in data['elements']:
        poi = {
            'name': element.get('tags', {}).get('name', 'Unknown'),
            'type': element.get('tags', {}).get('amenity', ''),
            'lat': element.get('lat') or element.get('center', {}).get('lat'),
            'lon': element.get('lon') or element.get('center', {}).get('lon'),
            'tags': element.get('tags', {})
        }
        pois.append(poi)
    
    return pois

# Example usage
lat, lon = 46.065943, 13.237780
restaurants = get_pois_overpass(lat, lon, 500, "restaurant")
print(f"Found {len(restaurants)}:")
for restaurant in restaurants:  # Show first 5
    print(f"- {restaurant['name']} at {restaurant['lat']}, {restaurant['lon']}")