import pytest
import requests
from unittest.mock import Mock, patch, MagicMock
from datetime import date, timedelta
from datastructures.TripDescriptor import Place, TripDescriptor
from datastructures.UserDescriptor import PerformanceDescriptor, PreferencesDescriptor, UserDescriptor


class TestPlace:
    """Test completi per la classe Place"""
    
    @patch('requests.get')
    def test_place_creation_successful(self, mock_get):
        """Test creazione Place con successo"""
        # Mock della risposta di Nominatim
        mock_response = Mock()
        mock_response.json.return_value = [{
            "display_name": "Udine, Friuli-Venezia Giulia, Italia",
            "lat": "46.0747793",
            "lon": "13.2345678"
        }]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        place = Place(name="Udine")
        
        assert place.name == "Udine"
        assert place.osm_name == "Udine, Friuli-Venezia Giulia, Italia"
        assert place.lat == 46.0747793
        assert place.lon == 13.2345678
        assert place.elv is None
        
        # Verifica chiamata API
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert "nominatim.openstreetmap.org" in args[0]
        assert kwargs['params']['q'] == "Udine"
        assert kwargs['params']['format'] == "json"

    @patch('requests.get')
    def test_place_creation_with_coordinates(self, mock_get):
        """Test creazione Place con coordinate preimpostate"""
        mock_response = Mock()
        mock_response.json.return_value = [{
            "display_name": "Test Place",
            "lat": "45.0",
            "lon": "12.0"
        }]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        place = Place(name="Test", lat=46.0, lon=13.0, elv=100.0)
        
        # Le coordinate dovrebbero essere aggiornate dalla API
        assert place.lat == 45.0  # Aggiornato dalla API
        assert place.lon == 12.0  # Aggiornato dalla API
        assert place.elv == 100.0  # Mantiene il valore originale

    @patch('requests.get')
    def test_place_not_found(self, mock_get):
        """Test gestione luogo non trovato"""
        mock_response = Mock()
        mock_response.json.return_value = []  # Nessun risultato
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Dovrebbe restituire un errore dalla funzione __set_coordinates
        place = Place(name="LuogoInesistente")
        # La funzione __set_coordinates dovrebbe gestire il caso di lista vuota
        
    @patch('requests.get')
    def test_place_api_error(self, mock_get):
        """Test gestione errore API"""
        mock_get.side_effect = requests.exceptions.RequestException("API Error")
        
        with pytest.raises(requests.exceptions.RequestException):
            Place(name="Test")

    def test_get_name(self):
        """Test metodo get_name"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = [{
                "display_name": "Udine, Italia",
                "lat": "46.0",
                "lon": "13.0"
            }]
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            place = Place(name="Udine")
            assert place.get_name() == "Udine, Italia"

    def test_get_coordinates_with_elevation(self):
        """Test get_coordinates con elevazione"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = [{
                "display_name": "Test",
                "lat": "46.0",
                "lon": "13.0"
            }]
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            place = Place(name="Test", elv=500.0)
            coords = place.get_coordinates()
            assert coords == (46.0, 13.0, 500.0)

    def test_get_coordinates_without_elevation(self):
        """Test get_coordinates senza elevazione"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = [{
                "display_name": "Test",
                "lat": "46.0",
                "lon": "13.0"
            }]
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            place = Place(name="Test")
            coords = place.get_coordinates()
            assert coords == (46.0, 13.0, 0.0)


class TestTripDescriptor:
    """Test completi per la classe TripDescriptor"""
    
    def test_trip_descriptor_initialization(self):
        """Test inizializzazione TripDescriptor"""
        trip = TripDescriptor()
        
        assert trip.bike_type == ""
        assert trip.places == []
        assert trip.number_of_days is None
        assert trip.dates is None
        assert trip.candidate_raw_routes is None
        assert trip.selected_raw_route is None
        assert trip.stepped_route is None
        assert trip.length is None

    def test_fill_bike_type_valid(self):
        """Test fill con bike_type valido"""
        trip = TripDescriptor()
        
        result = trip.fill(bike_type="gravel")
        assert result is None  # Nessun errore
        assert trip.bike_type == "gravel"
        
        result = trip.fill(bike_type="road")
        assert result is None
        assert trip.bike_type == "road"
        
        result = trip.fill(bike_type="mtb")
        assert result is None
        assert trip.bike_type == "mtb"

    def test_fill_bike_type_invalid(self):
        """Test fill con bike_type non valido"""
        trip = TripDescriptor()
        
        result = trip.fill(bike_type="invalid")
        assert result is not None
        assert "bike_type must be one of" in result
        assert trip.bike_type == ""  # Non dovrebbe essere cambiato

    @patch('datastructures.TripDescriptor.Place')
    def test_fill_places_valid(self, mock_place):
        """Test fill con places validi"""
        trip = TripDescriptor()
        
        # Mock della creazione di Place
        mock_place_instance = Mock()
        mock_place.return_value = mock_place_instance
        
        result = trip.fill(places=["Udine", "Trieste"])
        assert result is None
        assert len(trip.places) == 2
        assert mock_place.call_count == 2

    def test_fill_places_invalid(self):
        """Test fill con places non validi"""
        trip = TripDescriptor()
        
        # Solo un luogo (serve almeno 2)
        result = trip.fill(places=["Udine"])
        assert result is not None
        assert "at least 2 elements" in result

    def test_fill_number_of_days_valid(self):
        """Test fill con number_of_days valido"""
        trip = TripDescriptor()
        
        result = trip.fill(number_of_days=5)
        assert result is None
        assert trip.number_of_days == 5

    def test_fill_number_of_days_invalid(self):
        """Test fill con number_of_days non valido"""
        trip = TripDescriptor()
        
        result = trip.fill(number_of_days=0)
        assert result is not None
        assert "must be greater than 0" in result
        
        result = trip.fill(number_of_days=-1)
        assert result is not None
        assert "must be greater than 0" in result

    def test_fill_dates_valid(self):
        """Test fill con dates valide"""
        trip = TripDescriptor()
        
        result = trip.fill(dates=("2023-10-01", "2023-10-05"))
        assert result is None
        assert len(trip.dates) == 2
        assert trip.dates[0] == date(2023, 10, 1)
        assert trip.dates[1] == date(2023, 10, 5)

    def test_fill_dates_invalid_format(self):
        """Test fill con formato date non valido"""
        trip = TripDescriptor()
        
        with pytest.raises(ValueError):
            trip.fill(dates=("invalid-date", "2023-10-05"))

    def test_date_consistency_correction(self):
        """Test correzione automatica inconsistenza date/giorni"""
        trip = TripDescriptor()
        
        # Imposta prima le date
        trip.fill(dates=("2023-10-01", "2023-10-05"))  # 5 giorni
        # Poi cambia il numero di giorni
        trip.fill(number_of_days=3)
        
        # La data finale dovrebbe essere corretta automaticamente
        assert trip.dates[1] == date(2023, 10, 3)  # 3 giorni da 2023-10-01

    @patch('datastructures.TripDescriptor.TripDescriptor.plan_candidate_raw_routes')
    @patch('datastructures.TripDescriptor.Place')
    def test_fill_places_triggers_route_planning(self, mock_place, mock_plan_routes):
        """Test che il fill places attivi la pianificazione route"""
        trip = TripDescriptor()
        trip.bike_type = "gravel"  # Necessario per la pianificazione
        
        mock_plan_routes.return_value = None
        mock_place.return_value = Mock()
        
        result = trip.fill(places=["Udine", "Trieste"])
        
        mock_plan_routes.assert_called_once()

    @patch('requests.get')
    def test_plan_candidate_raw_routes_success(self, mock_get):
        """Test pianificazione route con successo"""
        trip = TripDescriptor()
        trip.bike_type = "gravel"
        
        # Mock della risposta BRouter
        mock_response = Mock()
        mock_response.json.return_value = {
            "features": [{"geometry": {"coordinates": [[13.0, 46.0], [13.1, 46.1]]}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Mock dei luoghi
        place1 = Mock()
        place1.get_coordinates.return_value = (46.0, 13.0, 0.0)
        place2 = Mock()
        place2.get_coordinates.return_value = (46.1, 13.1, 0.0)
        trip.places = [place1, place2]
        
        result = trip.plan_candidate_raw_routes()
        
        assert result is None
        assert trip.candidate_raw_routes is not None
        assert len(trip.candidate_raw_routes) > 0

    def test_plan_candidate_raw_routes_no_places(self):
        """Test pianificazione route senza luoghi"""
        trip = TripDescriptor()
        
        result = trip.plan_candidate_raw_routes()
        assert result is not None
        assert "places are not set" in result

    def test_plan_candidate_raw_routes_no_bike_type(self):
        """Test pianificazione route senza bike_type"""
        trip = TripDescriptor()
        trip.places = [Mock(), Mock()]
        
        result = trip.plan_candidate_raw_routes()
        assert result is not None
        assert "bike_type is not set" in result

    def test_fill_selected_raw_route_valid(self):
        """Test selezione route valida"""
        trip = TripDescriptor()
        trip.candidate_raw_routes = [[[13.0, 46.0]], [[13.1, 46.1]]]
        
        with patch.object(trip, '_TripDescriptor__plan_steps', return_value=None):
            result = trip.fill(selected_raw_route=0)
            assert result is None
            assert trip.selected_raw_route == 0

    def test_fill_selected_raw_route_invalid(self):
        """Test selezione route non valida"""
        trip = TripDescriptor()
        
        # Nessuna route candidata
        result = trip.fill(selected_raw_route=0)
        assert result is not None
        assert "candidate routes" in result
        
        # Indice fuori range
        trip.candidate_raw_routes = [[[13.0, 46.0]]]
        result = trip.fill(selected_raw_route=5)
        assert result is not None
        assert "must be between 0 and" in result

    def test_geopoint_distance(self):
        """Test calcolo distanza tra punti geografici"""
        trip = TripDescriptor()
        
        # Test con punti noti (distanza approssimativa)
        point1 = [46.0747793, 13.2345678, 0]  # Udine
        point2 = [45.6495264, 13.7606721, 0]  # Trieste
        
        distance = trip._TripDescriptor__geopoint_distance(point1, point2)
        
        # La distanza dovrebbe essere circa 60-70 km
        assert 50 < distance < 80

    def test_plan_steps_success(self):
        """Test pianificazione step con successo"""
        trip = TripDescriptor()
        trip.candidate_raw_routes = [[[13.0, 46.0, 0], [13.1, 46.1, 0], [13.2, 46.2, 0]]]
        trip.selected_raw_route = 0
        
        result = trip._TripDescriptor__plan_steps(max_distance=50.0)
        
        assert result is None
        assert trip.stepped_route is not None
        assert trip.length is not None

    def test_plan_steps_no_routes(self):
        """Test pianificazione step senza route"""
        trip = TripDescriptor()
        
        result = trip._TripDescriptor__plan_steps()
        assert result is not None
        assert "candidate_raw_routes is None" in result

    def test_plan_steps_no_selected_route(self):
        """Test pianificazione step senza route selezionata"""
        trip = TripDescriptor()
        trip.candidate_raw_routes = [[[13.0, 46.0]]]
        
        result = trip._TripDescriptor__plan_steps()
        assert result is not None
        assert "selected_raw_route" in result

    def test_getter_methods(self):
        """Test tutti i metodi getter"""
        trip = TripDescriptor()
        trip.bike_type = "gravel"
        trip.number_of_days = 5
        trip.dates = [date(2023, 10, 1), date(2023, 10, 5)]
        trip.places = [Mock()]
        trip.candidate_raw_routes = [[[13.0, 46.0]]]
        trip.selected_raw_route = 0
        trip.stepped_route = [[[13.0, 46.0]]]
        trip.length = 100.0
        
        assert trip.get_bike_type() == "gravel"
        assert trip.get_number_of_days() == 5
        assert trip.get_dates() == [date(2023, 10, 1), date(2023, 10, 5)]
        assert trip.get_places() == [Mock()]
        assert trip.get_candidate_raw_routes() == [[[13.0, 46.0]]]
        assert trip.get_selected_raw_route() == 0
        assert trip.get_stepped_route() == [[[13.0, 46.0]]]
        assert trip.get_length() == 100.0

    def test_get_description_empty(self):
        """Test descrizione trip vuoto"""
        trip = TripDescriptor()
        description = trip.get_description()
        assert description == "No trip information available."

    def test_get_description_full(self):
        """Test descrizione trip completo"""
        trip = TripDescriptor()
        trip.bike_type = "gravel"
        trip.number_of_days = 3
        
        place1 = Mock()
        place1.get_name.return_value = "Udine"
        place2 = Mock()
        place2.get_name.return_value = "Trieste"
        trip.places = [place1, place2]
        
        trip.dates = [date(2023, 10, 1), date(2023, 10, 3)]
        trip.candidate_raw_routes = [[[13.0, 46.0]], [[13.1, 46.1]]]
        trip.selected_raw_route = 0
        trip.stepped_route = [[[13.0, 46.0]]]
        trip.length = 150.5
        
        description = trip.get_description()
        
        assert "gravel" in description
        assert "3" in description
        assert "Udine" in description
        assert "Trieste" in description
        assert "2023-10-01" in description
        assert "2023-10-03" in description
        assert "2" in description  # candidate routes
        assert "0" in description  # selected route
        assert "1" in description  # steps
        assert "150.5" in description  # length

    def test_get_class_description(self):
        """Test descrizione della classe"""
        trip = TripDescriptor()
        description = trip.get_class_description()
        
        assert "TripDescriptor" in description
        assert "bike_type" in description
        assert "places" in description
        assert "number_of_days" in description


class TestPerformanceDescriptor:
    """Test completi per la classe PerformanceDescriptor"""
    
    def test_performance_descriptor_initialization(self):
        """Test inizializzazione PerformanceDescriptor"""
        perf = PerformanceDescriptor()
        
        assert perf.kilometer_per_day == 0
        assert perf.difference_in_height_per_day == 0

    def test_performance_descriptor_with_values(self):
        """Test inizializzazione con valori"""
        perf = PerformanceDescriptor(kilometer_per_day=100, difference_in_height_per_day=1000)
        
        assert perf.kilometer_per_day == 100
        assert perf.difference_in_height_per_day == 1000

    def test_fill_valid_values(self):
        """Test fill con valori validi"""
        perf = PerformanceDescriptor()
        
        perf.fill({"kilometer_per_day": 80})
        assert perf.kilometer_per_day == 80
        
        perf.fill({"difference_in_height_per_day": 500})
        assert perf.difference_in_height_per_day == 500
        
        perf.fill({"kilometer_per_day": 120, "difference_in_height_per_day": 800})
        assert perf.kilometer_per_day == 120
        assert perf.difference_in_height_per_day == 800

    def test_fill_invalid_types(self):
        """Test fill con tipi non validi"""
        perf = PerformanceDescriptor()
        
        with pytest.raises(TypeError):
            perf.fill({"kilometer_per_day": "100"})  # Stringa invece di int
            
        with pytest.raises(TypeError):
            perf.fill({"difference_in_height_per_day": 100.5})  # Float invece di int

    def test_fill_unknown_key(self):
        """Test fill con chiave sconosciuta"""
        perf = PerformanceDescriptor()
        
        # Non dovrebbe sollevare eccezioni, ma stampare warning
        perf.fill({"unknown_key": 100})

    def test_getter_methods(self):
        """Test metodi getter"""
        perf = PerformanceDescriptor(kilometer_per_day=90, difference_in_height_per_day=600)
        
        assert perf.get_kilometer_per_day() == 90
        assert perf.get_difference_in_height_per_day() == 600

    def test_get_description_empty(self):
        """Test descrizione performance vuota"""
        perf = PerformanceDescriptor()
        description = perf.get_description()
        assert description == "No performance set."

    def test_get_description_partial(self):
        """Test descrizione performance parziale"""
        perf = PerformanceDescriptor(kilometer_per_day=100)
        description = perf.get_description()
        assert "Kilometers per day: 100" in description
        assert "Difference in height" not in description

    def test_get_description_full(self):
        """Test descrizione performance completa"""
        perf = PerformanceDescriptor(kilometer_per_day=80, difference_in_height_per_day=500)
        description = perf.get_description()
        assert "Kilometers per day: 80" in description
        assert "Difference in height per day: 500" in description


class TestPreferencesDescriptor:
    """Test completi per la classe PreferencesDescriptor"""
    
    def test_preferences_descriptor_initialization(self):
        """Test inizializzazione PreferencesDescriptor"""
        pref = PreferencesDescriptor()
        
        assert pref.amenity is None
        assert pref.turism is None
        assert pref.historic is None
        assert pref.building is None
        assert pref.natural is None
        assert pref.water is None
        assert pref.leisure is None
        assert pref.man_made is None

    def test_preferences_descriptor_with_values(self):
        """Test inizializzazione con valori"""
        pref = PreferencesDescriptor(
            amenity=["restaurant", "cafe"],
            natural=["beach", "forest"]
        )
        
        assert pref.amenity == ["restaurant", "cafe"]
        assert pref.natural == ["beach", "forest"]

    def test_fill_valid_categories(self):
        """Test fill con categorie valide"""
        pref = PreferencesDescriptor()
        
        pref.fill({"amenity": ["restaurant", "bar"]})
        assert pref.amenity == ["restaurant", "bar"]
        
        pref.fill({"turism": ["museum"]})
        assert pref.turism == ["museum"]
        
        pref.fill({"historic": ["castle", "monument"]})
        assert pref.historic == ["castle", "monument"]
        
        pref.fill({"building": ["cathedral"]})
        assert pref.building == ["cathedral"]
        
        pref.fill({"natural": ["peak", "waterfall"]})
        assert pref.natural == ["peak", "waterfall"]
        
        pref.fill({"water": ["lake", "river"]})
        assert pref.water == ["lake", "river"]
        
        pref.fill({"leisure": ["park", "garden"]})
        assert pref.leisure == ["park", "garden"]
        
        pref.fill({"man_made": ["lighthouse", "bridge"]})
        assert pref.man_made == ["lighthouse", "bridge"]

    def test_fill_multiple_categories(self):
        """Test fill con multiple categorie"""
        pref = PreferencesDescriptor()
        
        pref.fill({
            "amenity": ["restaurant", "cafe"],
            "natural": ["beach", "forest"],
            "historic": ["castle"]
        })
        
        assert pref.amenity == ["restaurant", "cafe"]
        assert pref.natural == ["beach", "forest"]
        assert pref.historic == ["castle"]

    def test_fill_invalid_types(self):
        """Test fill con tipi non validi"""
        pref = PreferencesDescriptor()
        
        with pytest.raises(TypeError):
            pref.fill({"amenity": "restaurant"})  # Stringa invece di lista
            
        with pytest.raises(TypeError):
            pref.fill({"natural": 123})  # Numero invece di lista

    def test_fill_invalid_key(self):
        """Test fill con chiave non valida"""
        pref = PreferencesDescriptor()
        
        with pytest.raises(ValueError):
            pref.fill({"invalid_category": ["test"]})

    def test_get_description_empty(self):
        """Test descrizione preferenze vuote"""
        pref = PreferencesDescriptor()
        description = pref.get_description()
        assert description == "No preferences set."

    def test_get_description_single_category(self):
        """Test descrizione con singola categoria"""
        pref = PreferencesDescriptor(amenity=["restaurant", "cafe"])
        description = pref.get_description()
        assert "Amenities: restaurant, cafe" in description

    def test_get_description_multiple_categories(self):
        """Test descrizione con multiple categorie"""
        pref = PreferencesDescriptor(
            amenity=["restaurant"],
            natural=["beach", "forest"],
            historic=["castle"]
        )
        description = pref.get_description()
        
        assert "Amenities: restaurant" in description
        assert "Natural: beach, forest" in description
        assert "Historic: castle" in description

    def test_to_one_hot_encoding_empty(self):
        """Test conversione one-hot con preferenze vuote"""
        pref = PreferencesDescriptor()
        one_hot = pref.to_one_hot_encoding()
        assert one_hot == set()

    def test_to_one_hot_encoding_single_category(self):
        """Test conversione one-hot con singola categoria"""
        pref = PreferencesDescriptor(amenity=["restaurant", "cafe"])
        one_hot = pref.to_one_hot_encoding()
        assert one_hot == {"restaurant", "cafe"}

    def test_to_one_hot_encoding_multiple_categories(self):
        """Test conversione one-hot con multiple categorie"""
        pref = PreferencesDescriptor(
            amenity=["restaurant", "cafe"],
            natural=["beach"],
            historic=["castle", "monument"]
        )
        one_hot = pref.to_one_hot_encoding()
        expected = {"restaurant", "cafe", "beach", "castle", "monument"}
        assert one_hot == expected

    def test_to_one_hot_encoding_with_duplicates(self):
        """Test conversione one-hot con duplicati"""
        pref = PreferencesDescriptor(
            amenity=["restaurant"],
            turism=["restaurant"]  # Stesso valore in categorie diverse
        )
        one_hot = pref.to_one_hot_encoding()
        assert one_hot == {"restaurant"}  # Set elimina duplicati


class TestUserDescriptor:
    """Test completi per la classe UserDescriptor"""
    
    def test_user_descriptor_initialization(self):
        """Test inizializzazione UserDescriptor"""
        user = UserDescriptor()
        
        assert isinstance(user.performance, PerformanceDescriptor)
        assert isinstance(user.preferences, PreferencesDescriptor)

    def test_user_descriptor_with_values(self):
        """Test inizializzazione con valori"""
        perf = PerformanceDescriptor(kilometer_per_day=100)
        pref = PreferencesDescriptor(amenity=["restaurant"])
        
        user = UserDescriptor(performance=perf, preferences=pref)
        
        assert user.performance == perf
        assert user.preferences == pref

    def test_getter_methods(self):
        """Test metodi getter"""
        user = UserDescriptor()
        
        performance = user.get_performance()
        preferences = user.get_preferences()
        
        assert isinstance(performance, PerformanceDescriptor)
        assert isinstance(preferences, PreferencesDescriptor)

    def test_fill_performance_only(self):
        """Test fill solo performance"""
        user = UserDescriptor()
        
        user.fill({
            "performance": {
                "kilometer_per_day": 80,
                "difference_in_height_per_day": 600
            }
        })
        
        assert user.performance.kilometer_per_day == 80
        assert user.performance.difference_in_height_per_day == 600

    def test_fill_preferences_only(self):
        """Test fill solo preferenze"""
        user = UserDescriptor()
        
        user.fill({
            "preferences": {
                "amenity": ["restaurant", "cafe"],
                "natural": ["beach"]
            }
        })
        
        assert user.preferences.amenity == ["restaurant", "cafe"]
        assert user.preferences.natural == ["beach"]

    def test_fill_complete(self):
        """Test fill completo"""
        user = UserDescriptor()
        
        user.fill({
            "performance": {
                "kilometer_per_day": 120,
                "difference_in_height_per_day": 800
            },
            "preferences": {
                "amenity": ["restaurant", "pub"],
                "historic": ["castle", "monument"],
                "natural": ["beach", "forest"]
            }
        })
        
        # Verifica performance
        assert user.performance.kilometer_per_day == 120
        assert user.performance.difference_in_height_per_day == 800
        
        # Verifica preferenze
        assert user.preferences.amenity == ["restaurant", "pub"]
        assert user.preferences.historic == ["castle", "monument"]
        assert user.preferences.natural == ["beach", "forest"]

    def test_fill_invalid_key(self):
        """Test fill con chiave non valida"""
        user = UserDescriptor()
        
        with pytest.raises(ValueError):
            user.fill({"invalid_key": {"test": "value"}})

    def test_get_description_empty(self):
        """Test descrizione utente vuoto"""
        user = UserDescriptor()
        description = user.get_description()
        
        assert "No performance set" in description
        assert "No preferences set" in description

    def test_get_description_full(self):
        """Test descrizione utente completo"""
        user = UserDescriptor()
        user.fill({
            "performance": {
                "kilometer_per_day": 90,
                "difference_in_height_per_day": 500
            },
            "preferences": {
                "amenity": ["restaurant"],
                "natural": ["beach"]
            }
        })
        
        description = user.get_description()
        
        assert "Kilometers per day: 90" in description
        assert "Difference in height per day: 500" in description
        assert "Amenities: restaurant" in description
        assert "Natural: beach" in description


class TestIntegration:
    """Test di integrazione tra le classi"""
    
    @patch('requests.get')
    def test_complete_trip_planning_workflow(self, mock_get):
        """Test workflow completo di pianificazione viaggio"""
        
        # Mock API responses
        nominatim_response = Mock()
        nominatim_response.json.return_value = [{
            "display_name": "Test Location",
            "lat": "46.0",
            "lon": "13.0"
        }]
        nominatim_response.raise_for_status.return_value = None
        
        brouter_response = Mock()
        brouter_response.json.return_value = {
            "features": [{"geometry": {"coordinates": [[13.0, 46.0], [13.1, 46.1]]}}]
        }
        brouter_response.raise_for_status.return_value = None
        
        mock_get.side_effect = [
            nominatim_response, nominatim_response,  # Per i due luoghi
            brouter_response, brouter_response, brouter_response, brouter_response  # Per le 4 route
        ]
        
        # Crea trip descriptor
        trip = TripDescriptor()
        
        # Riempi gradualmente
        result = trip.fill(bike_type="gravel")
        assert result is None
        
        result = trip.fill(places=["Udine", "Trieste"])
        assert result is None
        
        result = trip.fill(number_of_days=3)
        assert result is None
        
        result = trip.fill(dates=("2023-10-01", "2023-10-03"))
        assert result is None
        
        result = trip.fill(selected_raw_route=0)
        assert result is None
        
        # Verifica stato finale
        assert trip.bike_type == "gravel"
        assert len(trip.places) == 2
        assert trip.number_of_days == 3
        assert len(trip.dates) == 2
        assert trip.candidate_raw_routes is not None
        assert trip.selected_raw_route == 0
        assert trip.stepped_route is not None

    def test_user_complete_setup(self):
        """Test setup completo utente"""
        user = UserDescriptor()
        
        user.fill({
            "performance": {
                "kilometer_per_day": 100,
                "difference_in_height_per_day": 1000
            },
            "preferences": {
                "amenity": ["restaurant", "cafe", "pub"],
                "natural": ["beach", "forest", "peak"],
                "historic": ["castle", "monument"],
                "leisure": ["park", "garden"]
            }
        })
        
        # Verifica che tutto sia stato impostato correttamente
        assert user.performance.kilometer_per_day == 100
        assert user.performance.difference_in_height_per_day == 1000
        
        one_hot = user.preferences.to_one_hot_encoding()
        expected_preferences = {
            "restaurant", "cafe", "pub", "beach", "forest", 
            "peak", "castle", "monument", "park", "garden"
        }
        assert one_hot == expected_preferences
        
        description = user.get_description()
        assert "100" in description
        assert "1000" in description
        assert "restaurant" in description


# Parametrized tests per casi edge
@pytest.mark.parametrize("bike_type,expected", [
    ("road", True),
    ("gravel", True), 
    ("mtb", True),
    ("hybrid", False),
    ("electric", False),
    ("", False),
    (None, False)
])
def test_bike_type_validation(bike_type, expected):
    """Test parametrizzato per validazione bike_type"""
    trip = TripDescriptor()
    result = trip.fill(bike_type=bike_type)
    
    if expected:
        assert result is None
        assert trip.bike_type == bike_type
    else:
        assert result is not None


@pytest.mark.parametrize("days,expected", [
    (1, True),
    (7, True),
    (30, True),
    (0, False),
    (-1, False),
    (-10, False)
])
def test_number_of_days_validation(days, expected):
    """Test parametrizzato per validazione number_of_days"""
    trip = TripDescriptor()
    result = trip.fill(number_of_days=days)
    
    if expected:
        assert result is None
        assert trip.number_of_days == days
    else:
        assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])